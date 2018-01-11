#!/bin/bash

grep -v '^@' $1 | cut -f2 -s  | head | xargs -I{} sh -c 'echo "obase=2;{}" | bc' | xargs printf '%012d\n' | rev | perl -ne  'chomp; print join("\t", split(//, $_)), "\n"' > tmp1
grep -v '^@' $1 | cut -f1,3,5,9 > tmp2
paste tmp1 tmp2 > ${1%.*}_table.tsb
rm tmp1 tmp2
