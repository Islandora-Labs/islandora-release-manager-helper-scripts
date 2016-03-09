#!/usr/bin/env python

from git import Repo
from sys import exit
from pync import Notifier
from time import sleep
import requests
import argparse
import getpass
import json

class WatchGitHubOrgPRs:

  def __init__(self, api_url, org, creds):
    self.api_url = api_url
    self.org = org
    self.creds = creds
    self.initialize()

  def initialize(self):
    # Get the current PR list.
    print "Getting the current list of pull requests for %s ..." % self.org
    self.prs = self.get_prs()

  def get_prs(self):
    r = requests.get("%s/users/%s/events/orgs/%s" % (self.api_url, username, self.org), auth=(creds['username'], creds['password']))
    if r.status_code != 200:
      print "Failed to get the list of pull requests for %s: error %s (%s)" % (self.org, str(r.status_code), response['message'])
      exit(1)
    events = json.loads(r.text)
    filtered_events = [event for event in events if event['type'] == 'PullRequestEvent']
    return filtered_events


  def cycle(self):
    # Get the new list.
    print "Getting the new list of pull requests for %s ..." % self.org
    new_prs = self.get_prs()

    # Find new things to notify.
    notifications = False
    for new_pr in new_prs:
      is_new = True
      for old_pr in self.prs:
        if old_pr['id'] == new_pr['id']:
          is_new = False
      if is_new:
        self.notify(new_pr)
    if not notifications:
      print "No new pull requests."

    # Overwrite the prs list with the new list.
    self.prs = new_prs

  def notify(self, event):
    print "Notifying of %s PR %s ..." % (self.org, event['id'])
    Notifier.notify('New pull request to %s' % (event['repo']['name']), title="PR Watcher", open=event['payload']['pull_request']['html_url'])

if __name__ == "__main__":
  # Arguments.
  parser = argparse.ArgumentParser (description="Watch and get notifications for the pull requests made to an organization.")
  parser.add_argument('orgs', nargs='+', help="Names of the organizations to watch.")
  parser.add_argument('--api-url', help="URL of the REST API to request. Defaults to https://api.github.com", default="https://api.github.com")
  parser.add_argument('--interval', help="The interval (in seconds) to wait between checking pull requests. Defaults to 900 (15 minutes).", type=int, default=900)
  args = vars(parser.parse_args())

  # Get the credentials.
  username = raw_input('Username: ')
  password = getpass.getpass()

  # Start up the watcher.
  creds = {
    'username': username,
    'password': password,
  }

  # Check creds and see that we have a connection.
  print "Checking connection and credentials ..."
  r = requests.get(args['api_url'], auth=(creds['username'], creds['password']))
  if r.status_code == 401:
    print "Failed to authorize"
    exit(1)
  if r.status_code != 200:
    print 'Could not connect to %s' % self.api_url
    exit(1)

  watchers = []
  for org in args['orgs']:
    watchers.append(WatchGitHubOrgPRs(args['api_url'], org, creds))

  # Start up the loop.
  try:
    while True:
      sleep(args['interval'])
      for watcher in watchers:
        watcher.cycle()
  except (KeyboardInterrupt, SystemExit):
    print "Exiting ..."
    exit(0)
  except:
    exit(1)
