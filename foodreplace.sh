#!/bin/bash

[ $# != 2 ] && echo "twwo args" && exit

match=$1
repl=$2

file1=../logs/keto_foodlog.txt
file2=../logs/keto_foodlog.backup

cat $file1 | sed "s/$match/$repl/" > $file2
cp $file2 $file1
