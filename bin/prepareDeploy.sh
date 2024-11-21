#!/bin/bash
set -e

cd ../client/

npm install

npm run build

rm -rf ../server/dist || true

cp -r dist/ ../server/dist/

rm -rf dist/

cd ../server

rm full.zip || true

7z a -tzip full.zip . -xr!node_modules