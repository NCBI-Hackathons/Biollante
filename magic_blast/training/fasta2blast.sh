#!/bin/bash

magicblast -query $1 -db ~/data/DB/PlantDB -num_threads 6 -splice F > ${1%.*}_vs_platdb.sam
