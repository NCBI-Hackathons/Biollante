import pandas
import time
import Bio.SeqIO
from sequence_mixing import *

# Names of FASTA files containing plant genomes
file_names = [
    'RefSeqPlants\Brachypodium_distachyon\GCF_000005505.2_Brachypodium_distachyon_v2.0_genomic.fna',
    'RefSeqPlants\Oryza_sativa\GCF_001433935.1_IRGSP-1.0_genomic.fna',
    'RefSeqPlants\Setaria_italica\GCF_000263155.2_Setaria_italica_v2.0_genomic.fna',
    'RefSeqPlants\Sorghum_bicolor\GCF_000003195.3_Sorghum_bicolor_NCBIv3_genomic.fna',
    'RefSeqPlants\Zea_mays\GCF_000005005.2_B73_RefGen_v4_genomic.fna'
]

species = [
    'Brachypodium_distachyon',
    'Oryza_sativa',
    'Setaria_italica',
    'Sorghum_bicolor',
    'Zea_mays'
]

# Number of mixed genomes per species-species combination
genomes_per_mix = 4000

# Cleaning method adapted from create_herb_bacmet_contaminated_training_pipeline.py
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

# Removes non-sequence lines and combines combines records
def combine_records(f):
    combined = ''
    for record in Bio.SeqIO.parse(f, 'fasta'):
        if 'chloroplast' not in record.description and 'mitochondria' not in record.description:
            combined += str(record.seq.upper())
    return combined

# Start timing process
start = time.time()

# Remove mitochondria/chloroplast sequences & combine sequences
# This saves some time by only cleaning each genome once
print 'Cleaning FASTA files.'
for f in range(len(file_names)):
    with open(file_names[f], 'r') as raw_file:
        cleaned_sequence = combine_records(raw_file)
        with open(file_names[f][:len(file_names[f]) - 3] + 'txt', 'w') as output:
            output.write(cleaned_sequence)
        print 'Cleaned', file_names[f]
        output.close()
print 'Finished cleaning FASTA files.'

print 'Starting plant genome mixing.'
data = {}

# Open master sequence file
for m in range(len(file_names)):
    with open(file_names[m][:len(file_names[m]) - 3] + 'txt', 'r') as m_file:
        master = m_file.read()
        print 'Opened', species[m], 'genome file.'
        # Open contaminant sequence file
        for c in range(len(file_names)):
            # Do not combine each genome with itself
            if c != m:
                with open(file_names[c][:len(file_names[c]) - 3] + 'txt', 'r') as c_file:
                    contaminant = c_file.read()
                    contaminated_seqs = []
                    print 'Opened', species[c], 'genome file.'
                    #Add each 500bp contaminated sequence to list
                    for i in range(genomes_per_mix):
                        contaminated_seqs.append(clean_sequence(random_mixed_sequence(master, contaminant, 400, 1200, 2000).upper()))
                c_file.close()
                data[species[m] + species[c]] = contaminated_seqs
                print 'Mixed genomes from', species[m], 'and', species[c]
    m_file.close()

# Copy to CSV file
print 'Writing to file.'
contam_seqs_data = pandas.DataFrame(data)
contam_seqs_data.to_csv('plant_mix_contaminated_sequences.csv')

end = time.time()
print 'Done in', str(end - start), 'seconds.'
