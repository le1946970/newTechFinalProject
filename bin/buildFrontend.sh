#!/bin/bash

cd ../public

npm install

npm run build

cp -r build/ ../server/react_build

rm -rf build/