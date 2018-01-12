import pandas as pd
from itertools import groupby
import string
from sequence_mixing import *

"""Read in the training/validation data"""
files = ['data/RefSeqPlantsTest/GCF_000004075.2_ASM407v2_genomic.fna',
        'data/RefSeqPlantsTest/GCF_000258705.1_Coccomyxa_subellipsoidae_v2.0_genomic.fna',
        'data/RefSeqPlantsTest/GCF_000493195.1_Citrus_clementina_v1.0_genomic.fna']

species = ['Mystery Plant 1', 'Mystery Plant 2', 'Mystery Plant 3']

training_point_count = 10000

data_points = {}
first_column = ['Non-contaminated']*training_point_count

"""Replace all non-A, C, G, T characters in a given sequence
with A, C, G, T, each possibility being equally likely"""
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

"""Loop through each of the species"""
for i in range(len(files)):
    print i
    filename = files[i]
    speciesname = species[i]

    """Read in the sequence for the current species, and clean by
    making all letters upper case and removing any letters that are
    not one of A, C, G, T"""
    with open(filename) as f:
        groups = groupby(f, key=lambda x: not x.startswith(">"))
        d = {}
        for k,v in groups:
            if not k:
                key, val = list(v)[0].rstrip(), "".join(map(str.rstrip,next(groups)[1],""))
                d[key] = val
    f.close()

    seq_fragments = [d[key] for key in d.keys() if ('chloroplast' not in key and 'mitochondria' not in key)]
    seq = ''.join(seq_fragments)
    seq = seq.upper()
    seq = seq.strip()

    good_chars = ['A', 'C', 'G', 'T']
    seq = seq.replace('N', '')

    """Choose a random subsequence of the appropriate length (don't contaminate)"""
    non_contaminated_seqs = []
    for j in range(training_point_count):
        non_contaminated_seq = random_mixed_sequence(seq, '', mixed_len = 500)
        non_contaminated_seq = clean_sequence(non_contaminated_seq)
        non_contaminated_seqs.append(non_contaminated_seq)

    data_points[speciesname] = non_contaminated_seqs

"""Write everything out to a file"""
non_contaminated_seqs_df = pd.DataFrame(data_points, index = first_column)
non_contaminated_seqs_df.to_csv('non_contaminated_mystery_sequences.csv')
