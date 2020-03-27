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
download "Islandora-Devops" "ansible-role-activemq"
download "Islandora-Devops" "ansible-role-alpaca"
download "Islandora-Devops" "ansible-role-blazegraph"
download "Islandora-Devops" "ansible-role-cantaloupe"
download "Islandora-Devops" "ansible-role-crayfish"
download "Islandora-Devops" "ansible-role-drupal-openseadragon"
download "Islandora-Devops" "ansible-role-fcrepo"
download "Islandora-Devops" "ansible-role-fcrepo-syn"
download "Islandora-Devops" "ansible-role-tomcat8"
download "Islandora-Devops" "ansible-role-fits"
download "Islandora-Devops" "ansible-role-grok"
download "Islandora-Devops" "ansible-role-karaf"
download "Islandora-Devops" "ansible-role-keymaster"
download "Islandora-Devops" "ansible-role-matomo"
