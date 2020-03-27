#!/bin/bash

echo
echo "Releasing Crayfish-Commons"
echo

cd Crayfish-Commons
sed -i "s/\"islandora\/chullo\": \"dev-dev\",/\"islandora\/chullo\": \"$1\",/" composer.json
composer update islandora/chullo
git add composer.json composer.lock
git commit -m "Version $2"
git tag "$2"
git push origin master
git push --tags origin
cd -
