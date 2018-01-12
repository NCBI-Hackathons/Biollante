#!/bin/bash

magicblast -query $1 -db ~/data/DB/allpDB -num_threads 6 -splice F > ${1%.*}_vs_plantdb.sam
magicblast -query $1 -db ~/data/DB/allpDB -outfmt tabular  -num_threads 6 -splice F > ${1%.*}_vs_plantdb.tabular
