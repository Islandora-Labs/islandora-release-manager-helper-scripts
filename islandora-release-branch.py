#!/usr/bin/env python

from sys import exit
from os import path
import requests
import argparse
import getpass
import json

'''
  Accepts a message (no whitespace at the end) so a yes or no question can be
  asked.
'''
def yes_or_no(message):
  valid = {
      "yes": True,
      "ye": True,
      "y": True,
      "no": False,
      "n": False,
      }
  while True:
    choice = raw_input(message + " [Y/n] ").lower()
    if choice == '':
      return True
    elif choice in valid:
      return valid[choice]
    else:
      print "Please respond with 'y' or 'n'"

'''
Tries to parse the 'next' page from the Links header entry.
Returns the link if found, or None if there wasn't any.
'''
def parse_next_link(links):
  link_list = links.split(', ')
  for link in link_list:
    link_bits = link.split('; ')
    if link_bits[1] == 'rel="next"':
      return link_bits[0].translate(None, '<>')
  return None

def main():
  # Arguments.
  parser = argparse.ArgumentParser (description="Create a release branch for Islandora repositories.")
  parser.add_argument('branch', help="Name of the new branch to add.")
  parser.add_argument('--source-branch', help="Name of the branch to pull from. If not given, will default to the default branch for each repository.")
  parser.add_argument('--user', help="User to create the branches on. Defaults to Islandora.", default="Islandora")
  parser.add_argument('--api-url', help="URL of the REST API to request. Defaults to https://api.github.com", default="https://api.github.com")
  args = vars(parser.parse_args())

  # Get the credentials.
  username = raw_input('Username: ')
  password = getpass.getpass()
  auth = (username, password)

  # Check creds and see that we have a connection.
  print "Checking connection and credentials ..."
  r = requests.get(args['api_url'], auth=auth)
  if r.status_code == 401:
    print "Failed to authorize"
    exit(1)
  if r.status_code != 200:
    print 'Could not connect to %s' % (args['api_url'])
    exit(1)

  # Get the repositories.
  print "Grabbing repositories ..."
  repos = []
  r = requests.get("%s/users/%s/repos" % (args['api_url'], args['user']), auth=auth)
  if r.status_code != 200:
    error = json.loads(r.text)
    print "Failed to get repositories (Error %s: %s)" % (str(r.status_code), error['message'])
    exit(1)
  repos.extend(json.loads(r.text))

  # Iterate through the rest of the pages.
  more_pages = True
  while more_pages:
    next_link = parse_next_link(r.headers['Links'])
    more_pages = bool(next_link)
    if more_pages:
      r = requests.get(next_link, auth=auth)
      if r.status_code != 200:
        error = json.loads(r.text)
        print "Failed to get repositories (Error %s: %s)" % (str(r.status_code), error['message'])
        exit(1)
      repos.extend(json.loads(r.text))

  if len(repos) == 0:
    print "No repositories found. Exiting ..."
    exit(0)

  # Confirm.
  proceed = yes_or_no("About to create the %s branch on %s repositories owned by %s. Are you sure you wish to proceed?" % (args['branch'], len(repos), args['user']))
  if proceed:
    # Run through the repository list.
    for repo in repos:
      if not args['source_branch']:
        source_branch = repo['default_branch']
      else:
        source_branch = args['source_branch']

      print "Branching %s from HEAD on %s ..." % (repo['name'], source_branch)
      ref_url = "%s/repos/%s/%s/git/refs/heads/%s" % (args['api_url'], args['user'], repo, source_branch)
      r = requests.get(ref_url, auth=auth)
      # 404 almost certainly means the branch doesn't exist in this case.
      if r.status_code == 404:
        select_branch = yes_or_no("Could not find a reference for HEAD on %s. Use a different branch?" % (source_branch))
        if not select_branch:
          break

        branches = requests.get("%s/repos/%s/%s/branches" % (args['api_url'], args['user'], repo['name']), auth=auth)
        branches = json.loads(branches.text)
        branch_list = []
        for branch in branches:
          branch_list.append(branch['name'])
        print "Available branches:"
        for index, branch in enumerate(branch_list):
          print "  %s: %s" % (index, branch)
        selected_branch = raw_input("Choose a number from the list, or leave blank to skip this repository: ")
        if selected_branch == '':
          break
        while int(selected_branch) > len(branch_list):
          selected_branch = raw_input("Choose a number from the list, or leave blank to skip this repository: ")
          if selected_branch == '':
            break
        r = requests.get("%s/repos/%s/%s/git/refs/heads/%s" % (args['api_url'], args['user'], repo['name'], branch_list[selected_branch]))

      elif r.status_code != 200:
        error = json.loads(r.text)
        print "An error occurred trying to find a reference for HEAD on %s (message: %s)." % (args['source_branch'], error['message'])
        break

      # Create a branch from the head referenced.
      head = json.loads(r.text)
      branch_data = {
        'ref': 'refs/heads/%s' % (args['branch']),
        'sha': head['object']['sha']
      }
      r = requests.post('%s/repos/%s/%s/git/refs' % (args['api_url'], args['user'], repo['name']), data=json.dumps(branch_data), auth=auth)
      if r.status_code != 201:
        error = json.loads(r.text)
        print "Unable to create the fork (message: %s)." % (error['message'])
      else:
        print "Branch created."

if __name__ == "__main__":
  main()
