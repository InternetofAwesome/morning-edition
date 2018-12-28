#!/bin/bash

aws lambda invoke --function-name morning-edition --log-type Tail  outfile
cat outfile
rm outfile