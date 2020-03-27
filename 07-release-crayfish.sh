#!/bin/bash

prepare_microservice() {

  echo
  echo "Preparing $1 for release"
  echo

  cd "Crayfish/$1"
  rm composer.lock
  sed -i "s/\"islandora\/crayfish-commons\": \"dev-dev\"/\"islandora\/crayfish-commons\": \"$2\"/" composer.json
  composer update islandora/crayfish-commons
  git add composer.json composer.lock
  cd -

}

release_crayfish() {

  echo
  echo "Releasing Crayfish"
  echo

  cd Crayfish
  git commit -m "Version $1"
  git tag "$1"
  git push origin master
  git push --tags origin
  cd -
}

#prepare_microservice "Gemini" "1.1.0"
#prepare_microservice "Hypercube" "1.1.0"
#prepare_microservice "Homarus" "1.1.0"
#prepare_microservice "Milliner" "1.1.0"
#prepare_microservice "Recast" "1.1.0"
## Next time include Houdini

release_crayfish 1.1.1
