#!/bin/bash
cores="${1:-6}"

cut -f 1 SRA_codes.txt -d' ' | xargs -I{} echo 'magicblast -sra {} -db ~/data/DB/PlantDB -num_threads '$cores' -splice F | gzip -c > {}_vs_PlantDB.sam.gz' 
cut -f 1 SRA_codes.txt -d' ' | xargs -I{} echo 'magicblast -sra {} -outfmt tabular -db ~/data/DB/PlantDB -num_threads '$cores' -splice F | gzip -c > {}_vs_PlantDB.tabular.gz'
