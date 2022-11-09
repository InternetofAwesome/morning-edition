#!/bin/bash

set -ex

# pipreqs --force .
mkdir -p package
sudo docker run -v "$PWD":/var/task "lambci/lambda:build-python3.7" /bin/sh -c "pip install -r requirements.txt -t ./package; exit"


cd package 
# pip install -r ./requirements.txt  --target .
zip -r9 ../function.zip .
cd ..
zip -g function.zip function.py

aws lambda update-function-code --function-name morning-edition --zip-file fileb://function.zip