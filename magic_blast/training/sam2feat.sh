#!/bin/bash

grep -v '^@' $1 | cut -f2 -s   | xargs -I{} sh -c 'echo "obase=2;{}" | bc' | xargs printf '%012d\n' | rev | perl -ne  'chomp; print join("\t", split(//, $_)), "\n"' > tmp1_${1%.*}
grep -v '^@' $1 | cut -f3 > tmp2_${1%.*}
grep -v '^@' $1 | cut -f 6 | perl -ne '/(?:(\d+)S)?(\d+)M(?:(\d+)S)?/; if ($1) {print "$1\t"} else {print "0\t"} ; print "$2\t" ;  if ($3) {print "$3\n"} else {print "0\n"} ' > tmp4_${1%.*}

grep -v '^#' ${1%.*}.tabular | cut -f3,13,14,15,18 > tmp3_${1%.*}




paste tmp2_${1%.*} tmp3_${1%.*} tmp4_${1%.*} tmp1_${1%.*} > ${1%.*}_table.tsv


#rm tmp1 tmp2 tmp3 tmp4
