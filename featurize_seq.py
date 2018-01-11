import numpy as np
from keras.utils import to_categorical
import random

def kmerize(seq, k, stride):

    kmers = []

    for i in range(0, len(seq) - k + 1, stride):

        kmers.append(seq[i:i + k])

    return kmers

def generate_all_unique_kmers(k):

    bases = ['A', 'G', 'C', 'T']

    unique_kmers = []

    for i in range(len(bases) ** k):

        base_codes = []

        current_val = i

        for h in range(1, k + 1):

           base_codes.append(current_val % 4)

           current_val /= 4

        s = ''

        for j in base_codes:

            s += bases[j]

        unique_kmers.append(s)

    return unique_kmers

def featurize_seq(seq, k, stride, kmer_list):

    bases = ['A', 'T', 'C', 'G']

    for i in range(len(seq)):

        if seq[i] not in bases:

            seq = seq[:i] + random.choice(bases) + seq[i + 1 : ]

    #kmer_list = generate_all_unique_kmers(k)

    kmers = kmerize(seq, k, stride)

    feature_vector = []

    for z in kmers:

        feature_vector.append(kmer_list.index(z))

    #encoded = to_categorical(feature_vector, 4 ** k )

    #return encoded, feature_vector
    return feature_vector


def flatten_feature_vector(feature_vector):

    return [item for sublist in feature_vector for item in sublist]


'''
z, feature_vector = featurize_seq('AATTGCTAGGC', 3, 2)

print feature_vector
print z
print flatten_feature_vector(z)
'''
