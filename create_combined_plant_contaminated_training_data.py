import pandas
import pickle
import time
from sequence_mixing import *

# Names of FASTA files containing plant genomes
file_names = [
    'GCF_000001735.3_TAIR10_genomic.fna',
    'GCF_000002425.3_V1.1_genomic.fna',
    #'GCF_000005005.2_B73_RefGen_v4_genomic.fna',
    #'GCF_000005505.2_Brachypodium_distachyon_v2.0_genomic.fna',
    #'GCF_000143415.3_v1.0_genomic.fna',
    #'GCF_000219495.3_MedtrA17_4.0_genomic.fna',
]

species = [
    'Arabidopsis_thaliana',
    'Physcomitrella_patens',
    'Brachypodium_distachyon',
    'Selaginella_moellendorffii',
    'Zea mays',
    'Medicago_truncatul'
]

# Number of mixed genomes per species-species combination
genomes_per_mix = 4000

# Cleaning method from create_herb_bacmet_contaminated_training_pipeline.py
def clean_sequence(seq):
    good_chars = ['A', 'C', 'G', 'T']
    new_chars = []
    for i in range(len(seq)):
        if seq[i] not in good_chars:
            r = random.random()
            index = (int)(len(good_chars)*r)
            if index == 4: index = 3
            new_chars.append(good_chars[index])
        else:
            new_chars.append(seq[i])
    return ''.join(new_chars)

# Start timing process
print 'Starting plant genome mixing.'
data = {}
start = time.time()

# Open master sequence file
for m in range(len(file_names)):
    with open(file_names[m], 'r') as m_file:
        master = m_file.read()
        master = clean_sequence(master)
        print 'Opened', species[m], 'genome file.'

        # Open contaminant sequence file
        for c in range(len(file_names)):
            # Do not combine each genome with itself
            if c != m:
                with open(file_names[c], 'r') as c_file:
                    contaminant = c_file.read()
                    contaminant = clean_sequence(contaminant)
                    contaminated_seqs = []
                    print 'Opened', species[c], 'genome file.'
                    #Add each 500bp contaminated sequence to list
                    for i in range(genomes_per_mix):
                        contaminated_seqs.append(random_mixed_sequence(master, contaminant, 400, 1200, 2000))
                c_file.close()
                data[species[m] + species[c]] = contaminated_seqs
                print 'Mixed genomes from', species[m], 'and', species[c]
    m_file.close()

print 'Writing to file.'
contam_seqs_data = pandas.DataFrame(data)
contam_seqs_data.to_csv('plant_plant_contaminated_sequences.csv')

end = time.time()
print 'Done in', str(end - start), 'seconds.'
