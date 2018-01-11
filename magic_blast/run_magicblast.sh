#!/bin/bash


cut -f 1 SRA_codes.txt -d' ' | xargs -I{} echo 'magicblast -sra {} -db ~/data/DB/PlantDB -num_threads 6 -splice F | gzip -c > {}_vs_PlantDB.sam.gz' 
