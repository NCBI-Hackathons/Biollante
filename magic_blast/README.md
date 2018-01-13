#scripts

## generate\_magicblast\_commands.sh [number of threats]

This script generate a series of magicblast commands to align several plant sequencing experiments to our plant database. The commands can then be run using xargs, parallel or split to be run in several computers. By default the commands are set to use 6 cores.

## mit\_minus.pl fasta\_file.fasta > clean\_fasta\_file.fasta

mit\_minus.pl remove the mitochondrion and chloroplast sequences from a fasta files (those are more similar to bacteria than to plants).
SRR5069665_vs_PlantDB.sam.gz Setaria italica 82.36%;    Bacteria: 1.18% 
SRR5860247   Brachypodium distachyon: 64.25% 
