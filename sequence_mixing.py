import random
import pickle
import time

"""Choose an insert sequence of a given size from a
large sequence, chosen randomly from all sequences of
such size in the large sequence"""
def choose_fragment(seq, size):
    if size > len(seq): return
    loc = random.randint(0, len(seq)-size)
    return seq[loc : loc + size]

"""Choose an insert from a contaminant sequence and
insert it into a randomly chosen location in another sequence"""
def mixed_sequence(master_seq, contaminant_seq, size):
    insert = choose_fragment(contaminant_seq, size)
    insert_location = random.randint(0, len(master_seq))
    mixed_sequence = \
        master_seq[:insert_location] + insert + master_seq[insert_location:]
    return mixed_sequence

"""Choose a size randomly and contaminate a sequence with an insert
of that size"""
<<<<<<< HEAD
def random_mixed_sequence(master_seq, contaminant_seq, min_contaminant_size = 100, max_contaminant_size = 300, mixed_len = 500):
    contaminant_size = random.randint(min_contaminant_size, max_contaminant_size)
    master_subseq = choose_fragment(master_seq, mixed_len - contaminant_size)
    mixed_seq = mixed_sequence(master_subseq, contaminant_seq, contaminant_size)
    return mixed_seq

def generate_mixed_sequences():
    start = time.time()
    count = 0
    file_names = [
        'GCF_000001735.3_TAIR10_genomic.fna',
        'GCF_000002425.3_V1.1_genomic.fna',
        'GCF_000005005.2_B73_RefGen_v4_genomic.fna',
        'GCF_000005505.2_Brachypodium_distachyon_v2.0_genomic.fna',
        'GCF_000143415.3_v1.0_genomic.fna',
        'GCF_000219495.3_MedtrA17_4.0_genomic.fna',
    ]
    files = []
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
            pickle.dump(mixed_sequence(master, contaminant, 500), output)
    end = time.time()
    return 'Done in', str(end- start), 'seconds.'

print generate_mixed_sequences()
=======
def random_mixed_sequence(master_seq, contaminant_seq, min_contaminant_size, max_contaminant_size):
    size = random.randint(min_contaminant_size, max_contaminant_size)
    mixed_sequence = mixed_sequence(master_seq, contaminant_seq)
    return mixed_sequence
>>>>>>> 65efc76fd36c8338ad3e1cbfc3f8d42ad5ae9831
