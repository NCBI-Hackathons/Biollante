
cat ../sequences/GCF_000003195.3_Sorghum_bicolor_NCBIv3_genomic.fna ../sequences/GCF_000005005.2_B73_RefGen_v4_genomic.fna ../sequences/GCF_000005505.2_Brachypodium_distachyon_v2.0_genomic.fna ../sequences/GCF_000263155.2_Setaria_italica_v2.0_genomic.fna | ./mit_minus.pl > all_train.fasta

makeblastdb -in all_train.fasta -dbtype nucl -parse_seqids -out allpDB -title "all plant database"
