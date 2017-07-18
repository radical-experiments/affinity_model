#!/usr/bin/env bash

dirname=$1
find ../data -type d > d1.txt
cat d1.txt | sed 's/^........//' > d2.txt
sed '1d' d2.txt > dir_structure.txt
rm d1.txt d2.txt
mkdir $dirname
cp dir_structure.txt $dirname
cd $dirname
xargs mkdir -p < dir_structure.txt
rm dir_structure.txt
