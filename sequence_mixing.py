import random

"""Choose an insert sequence of a given size from a
large sequence, chosen randomly from all sequences of
such size in the large sequence"""
def choose_insert(seq, size):
    if size > len(seq): return
    loc = random.randint(0, len(seq)-size)
    return seq[loc : loc + size]

"""Choose an insert from a contaminant sequence and
insert it into a randomly chosen location in another sequence"""
def mixed_sequence(master_seq, contaminant_seq, size):
    insert = choose_insert(contaminant_seq, size)
    insert_location = random.randint(0, len(master_seq))
    mixed_sequence = \
        master_seq[:insert_location] + insert + master_seq[insert_location:]
    return mixed_sequence

"""Choose a size randomly and contaminate a sequence with an insert
of that size"""
def random_mixed_sequence(master_seq, contaminant_seq, min_contaminant_size, max_contaminant_size):
    size = random.randint(min_contaminant_size, max_contaminant_size)
    mixed_sequence = mixed_sequence(master_seq, contaminant_seq)
