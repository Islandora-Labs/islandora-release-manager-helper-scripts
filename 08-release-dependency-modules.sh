#!/bin/bash

release () {
  echo
  echo "Releasing $1"
  echo

  cd "$1" #Directory
  git tag "$2"
  git tag "$3"
  git push --tags origin
  cd -
}

release "jsonld" "8.x-1.1" "1.1.0"
release "carapace" "8.x-3.0" "3.0.0"
release "openseadragon" "8.x-1.1" "1.1.0"
release "controlled_access_terms" "8.x-1.1" "1.1.0"
release "migrate_islandora_csv" "8.x-1.1" "1.1.0"

#release_islandora "8.x-1.1" "1.1.0" "8.x-1.1"

#tag "islandora" "8.x-1.1"
#update "islandora_defaults" "8.x-1.1"
#update "islandora-playbook" "dev"

