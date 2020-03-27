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

release_islandora() {
  echo
  echo "Releasing islandora"
  echo

  cd islandora

  rm composer.lock
  rm -rf vendor

  sed -i "s/\"islandora\/jsonld\": \"dev-8.x-1.x\"/\"islandora\/jsonld\": \"$1\"/" composer.json
  sed -i "s/\"islandora\/crayfish-commons\": \"dev-dev\"/\"islandora\/crayfish-commons\": \"$2\"/" composer.json

  composer update islandora/crayfish-commons
  git add composer.json composer.lock
  git commit -m "Version $1"
  git tag "$1"

  git push origin master
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

