from argparse import ArgumentParser
import csv
from dna2vec.multi_k_model import MultiKModel
import pickle
import sys

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from featurize_seq import *
import numpy as np
from xgboost import XGBClassifier
import os

mk_model = MultiKModel(filepath)

pickled_model_file = 'models/refseq_2_sample_k8_160K_samples_model.p'
pickled_test_file = 'long_sample.p'
pickled_output_file = 'long_sample_predictions.p'

with open(pickled_model_file, 'rb') as h:
    model = pickle.load(h)

with open(pickled_test_file, 'rb') as h:
    test_sequences = pickle.load(h)

kmer_len = 8
kmer_list = generate_all_unique_kmers(kmer_len)

query_sequences = []
for i in test_sequences:

    if test_sequences.index(i) % 100 == 0:

        print test_sequences.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    query_sequences.append(feature_vector)

query_sequences = np.array(query_sequences)
predictions = model.predict(query_sequences)

with open(pickled_output_file, 'rb') as h:
    pickle.dump(predictions, h)
