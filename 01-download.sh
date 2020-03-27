#!/bin/bash

download () {
  echo
  echo "Checking $2"
  echo
  if [ ! -d "$2" ]
  then
    echo
    echo "Cloning $1/$2"
    echo
    git clone -b master git@github.com:$1/$2.git
  fi
}

download "Islandora" "documentation"
download "Islandora" "carapace"
download "Islandora" "islandora"
download "Islandora" "drupal-project"
download "Islandora" "islandora_defaults"
download "Islandora" "controlled_access_terms"
download "Islandora" "Syn"
download "Islandora" "openseadragon"
download "Islandora" "jsonld"
download "Islandora" "migrate_islandora_csv"
download "Islandora" "chullo"
download "Islandora" "Crayfish"
download "Islandora" "Alpaca"
download "Islandora" "Crayfish-Commons"
download "Islandora-Devops" "islandora-playbook"
