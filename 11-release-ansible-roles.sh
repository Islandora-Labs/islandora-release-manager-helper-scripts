#!/bin/bash

update () {
  echo
  echo "Updating $1"
  echo
  cd $1 #Directory
  git checkout master
  git pull origin master
  git tag "$2"
  git push --tags origin
  cd -
}

update "ansible-role-activemq" "1.0.1"
update "ansible-role-alpaca" "1.0.2"
update "ansible-role-blazegraph" "1.0.2"
update "ansible-role-cantaloupe" "1.0.2"
update "ansible-role-crayfish" "1.0.4"
update "ansible-role-drupal-openseadragon" "1.0.1"
update "ansible-role-fcrepo" "2.0.1"
update "ansible-role-fcrepo-syn" "1.0.1"
update "ansible-role-tomcat8" "1.0.1"
update "ansible-role-fits" "1.1.0"
update "ansible-role-grok" "2.0.1"
update "ansible-role-karaf" "1.0.1"
update "ansible-role-keymaster" "1.1.0"
update "ansible-role-matomo" "1.0.1"
