#!/usr/bin/env python

from sys import exit
from datetime import datetime
from pprint import PrettyPrinter
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
  parser = argparse.ArgumentParser (description="Update a tag for repositories.")
  parser.add_argument('tag', help="Name of the tag to update.")
  parser.add_argument('--branch', help="Name of the branch to attempt to get the HEAD commit from to update tags. If not given, will default to the HEAD commit on the default branch for each repository.")
  parser.add_argument('--user', help="User to update the tags on. Defaults to Islandora.", default="Islandora")
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
  repo_json = json.loads(r.text)
  repos.extend(repo_json)

  # Iterate through the rest of the pages.
  more_pages = True
  while more_pages:
    next_link = parse_next_link(r.headers['Link'])
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

  for idx, repo_data in enumerate(repos):
    if repo_data['name'] == 'islandora_ontology':
      del repos[idx]

  # Confirm.
  proceed = yes_or_no("About to update the %s tag on %s repositories owned by %s. Are you sure you wish to proceed?" % (args['tag'], len(repos), args['user']))
  if not proceed:
    exit(0)

  # Get the user info; this is needed to designate the tagger.
  r = requests.get("%s/user" % args['api_url'], auth=auth)
  if r.status_code != 200:
    print "Unable to get the information for the current user. Exiting ..."
    exit(1)
  user = json.loads(r.text)

  # Run through the repository list.
  for repo in repos:
    if not args['branch']:
      source_branch = repo['default_branch']
    else:
      source_branch = args['branch']

    print "Updating %s from HEAD on %s ..." % (repo['name'], source_branch)
    ref_url = "%s/repos/%s/%s/git/refs/heads/%s" % (args['api_url'], args['user'], repo['name'], source_branch)
    r = requests.get(ref_url, auth=auth)
    # 404 almost certainly means the branch doesn't exist in this case.
    if r.status_code == 404:
      select_branch = yes_or_no("Could not find a reference for HEAD on %s. Use a different branch?" % (source_branch))
      if not select_branch:
        continue

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
        continue
      while int(selected_branch) > len(branch_list):
        selected_branch = raw_input("Choose a number from the list, or leave blank to skip this repository: ")
        if selected_branch == '':
          continue
      r = requests.get("%s/repos/%s/%s/git/refs/heads/%s" % (args['api_url'], args['user'], repo['name'], branch_list[selected_branch]))

    elif r.status_code != 200:
      error = json.loads(r.text)
      print "An error occurred trying to find a reference for HEAD on %s (message: %s)." % (args['source_branch'], error['message'])
      continue

    # Create a tag from the head referenced.
    head = json.loads(r.text)
    tag_data = {
      'sha': head['object']['sha'],
    }
    r = requests.patch('%s/repos/%s/%s/git/refs/tags/%s' % (args['api_url'], args['user'], repo['name'], args['tag']), data=json.dumps(tag_data), auth=auth)
    if r.status_code != 200:
      error = json.loads(r.text)
      print "Unable to update the tag object (message: %s)." % error['message']
    else:
      print "Tag %s updated on %s." % (args['tag'], repo['name'])

if __name__ == "__main__":
  main()
