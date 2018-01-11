import random

"""Choose an insert sequence of a given size from a
large sequence, chosen randomly from all sequences of
such size in the large sequence"""
def choose_fragment(seq, size):
    if size > len(seq) or len(seq) == 0: return seq
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
def random_mixed_sequence(master_seq, contaminant_seq, min_contaminant_size = 100, max_contaminant_size = 300, mixed_len = 500):
    truncated_min = min(min_contaminant_size, len(contaminant_seq))
    truncated_max = min(max_contaminant_size, len(contaminant_seq))
    contaminant_size = random.randint(truncated_min, truncated_max)
    master_subseq = choose_fragment(master_seq, mixed_len - contaminant_size)
    mixed_seq = mixed_sequence(master_subseq, contaminant_seq, contaminant_size)
    return mixed_seq
