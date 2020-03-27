#!/bin/bash

# Four arguments
# - New jsonld version
# - New crayfish-commons version
# - New version for islandora in packagist
# - New version for islandora on drupal packagist

echo
echo "Releasing islandora"
echo

cd islandora

sed -i "s/\"islandora\/jsonld\": \"dev-8.x-1.x\"/\"islandora\/jsonld\": \"$1\"/" composer.json
sed -i "s/\"islandora\/crayfish-commons\": \"dev-dev\"/\"islandora\/crayfish-commons\": \"$2\"/" composer.json

git add composer.json
git commit -m "Version $3"
git tag "$3"
git tag "$4"

git push origin master
git push --tags origin

cd -
