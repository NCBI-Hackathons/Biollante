#!/bin/bash

grep -v '^@' $1 | cut -f2 -s  | head | xargs -I{} sh -c 'echo "obase=2;{}" | bc' | xargs printf '%012d\n' | rev | perl -ne  'chomp; print join("\t", split(//, $_)), "\n"' > tmp1
grep -v '^@' $1 | cut -f3,5 > tmp2
paste tmp2 tmp1 > ${1%.*}_table.tsb


#rm tmp1 tmp2
