#!/bin/bash

echo
echo "Releasing islandora_defaults"
echo

# Five arguments
# - New islandora version
# - New openseadragon version
# - New controlled_access_terms version
# - New version for islandora_defaults in packagist
# - New version for islandora_defaults on drupal packagist

cd islandora_defaults

sed -i "s/\"islandora\/islandora\": \"dev-8.x-1.x\"/\"islandora\/islandora\": \"$1\"/" composer.json
sed -i "s/\"islandora\/openseadragon\": \"dev-8.x-1.x\"/\"islandora\/openseadragon\": \"$2\"/" composer.json
sed -i "s/\"islandora\/controlled_access_terms\": \"dev-8.x-1.x\"/\"islandora\/controlled_access_terms\": \"$3\"/" composer.json

git add composer.json
git commit -m "Version $4"
git tag "$4"
git tag "$5"

git push origin master
git push --tags origin

cd -

