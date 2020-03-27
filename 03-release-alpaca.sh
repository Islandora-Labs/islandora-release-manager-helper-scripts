#!/bin/bash

cd Alpaca
./gradlew release
git add "docs/$1"
git commit -m "Add documentation for $1"
git push origin master

echo
echo "!!!"
echo "DON'T FORGET TO GO RELEASE IT FROM SONATYPE"
echo "https://github.com/Islandora/Alpaca/wiki/Alpaca-Release-Process#release-from-sonatype"
echo "!!!"
echo
