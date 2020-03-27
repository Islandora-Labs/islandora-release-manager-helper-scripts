#!/bin/bash

echo
echo "Releasing chullo"
echo

cd chullo
git tag "$1"
git push --tags origin
cd -
