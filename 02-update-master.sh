#!/bin/bash

update () {
  echo
  echo "Updating $1"
  echo
  cd $1 #Directory
  git fetch origin
  git checkout master
  git pull origin master
  git pull origin $2 #dev branch name
  git push origin master
  cd -
}

update "carapace" "8.x-3.x"
update "islandora" "8.x-1.x"
update "islandora_defaults" "8.x-1.x"
update "controlled_access_terms" "8.x-1.x"
update "Syn" "dev"
update "openseadragon" "8.x-1.x"
update "jsonld" "8.x-1.x"
update "migrate_islandora_csv" "dev"
update "chullo" "dev"
update "Crayfish" "dev"
update "Alpaca" "dev"
update "Crayfish-Commons" "dev"
update "islandora-playbook" "dev"
