#!/bin/bash

pip_packages="lxml \
feedgen"

mkdir -p package
cd package 
pip install $pip_packages --target .
zip -r9 ../function.zip .
cd ..
zip -g function.zip function.py

aws lambda update-function-code --function-name morning-edition --zip-file fileb://function.zip