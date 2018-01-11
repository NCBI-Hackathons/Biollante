import pickle
import time
from sequence_mixing import *

# Names of FASTA files containing plant genomes
file_names = [
    'GCF_000001735.3_TAIR10_genomic.fna',
    'GCF_000002425.3_V1.1_genomic.fna',
    'GCF_000005005.2_B73_RefGen_v4_genomic.fna',
    'GCF_000005505.2_Brachypodium_distachyon_v2.0_genomic.fna',
    'GCF_000143415.3_v1.0_genomic.fna',
    'GCF_000219495.3_MedtrA17_4.0_genomic.fna',
]

# Number of mixed genomes per species-species combination
genomes_per_mix = 4000

start = time.time()
files = []
contaminated_seqs = []
for f in file_names:
    data = open(f, 'r').read()
    files.append(data)
    print 'Read file', f
print 'Done reading files.'
mixed_genomes = []
output = open('mixed_seqs.p', 'wb')
for master in files:
    other_files = files[:]
    other_files.remove(master)
    for contaminant in other_files:
        contaminated_seqs.append(mixed_sequence(master, contaminant, 500))
end = time.time()
print 'Done in', str(end - start), 'seconds.'
