#!/bin/bash

BRANCH=$1

set -e

if [ ! -d ./fasset-bots ]; then
    echo "Missing directory fasset-bots. Please run 'git submodule update --remote --merge'."
    exit 1
fi

cd ./fasset-bots
git fetch origin $BRANCH
git checkout $BRANCH
git pull origin $BRANCH
yarn
yarn clean
yarn build
