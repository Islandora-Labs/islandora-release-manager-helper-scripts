#!/bin/bash

update_requirement() {
  sed -i "/name: Islandora-Devops.$1/{n;s/.*/  version: $2/}" requirements.yml
}

update_dependency() {
  sed -i "s/\"islandora\/$1:$2\"/\"islandora\/$1:$3\"/" inventory/vagrant/group_vars/webserver/drupal.yml
}

cd islandora-playbook
git checkout master
git pull origin master
git pull origin dev

update_requirement "activemq" "1.0.1"
update_requirement "alpaca" "1.0.2"
update_requirement "blazegraph" "1.0.2"
update_requirement "cantaloupe" "1.0.2"
update_requirement "crayfish" "1.0.4"
update_requirement "drupal-openseadragon" "1.0.1"
update_requirement "fcrepo" "2.0.1"
update_requirement "fcrepo-syn" "1.0.1"
update_requirement "tomcat8" "1.0.1"
update_requirement "fits" "1.1.0"
update_requirement "grok" "2.0.1"
update_requirement "karaf" "1.0.1"
update_requirement "keymaster" "1.1.0"
update_requirement "matomo" "1.0.1"

update_dependency "carapace" "dev-8.x-3.x" "3.0.0"
update_dependency "islandora_defaults" "dev-8.x-1.x" "1.1.0"

git add requirements.yml inventory/vagrant/group_vars/webserver/drupal.yml
git commit -m "Version 1.0.1"
git tag 1.0.1
git push origin master
git push --tags origin
cd -
