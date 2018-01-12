#!/bin/bash

base=$(echo $1 | rev | cut -d'/' -f1 | rev)
./csv2fasta.pl $1 > ${base%.*}.fasta
./fasta2blast.sh ${base%.*}.fasta
./sam2feat.sh ${base%.*}_vs_plantdb.sam

