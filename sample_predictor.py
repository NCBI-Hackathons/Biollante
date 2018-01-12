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

parser = ArgumentParser(description="This script builds plant data packages from Ref Seq.")
parser.add_argument('-f', '--file', help='dna2vec model file',
                    default='dna2vec/results/refseq-training-vec-k3to8.w2v', required = False)

args = vars(parser.parse_args())

filepath = args['file']

if not os.path.exists(filepath):
    'dna2vec model file does not exist: ' + filepath
    sys.exit(1)
print 'Using dna2vec model: ' + filepath

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

predictions = []
ct = 0
for j in test_sequences:
    i = j.upper()

    if test_sequences.index(j) % 100 == 0:
        print test_sequences.index(j)

    #z, feature_vector = featurize_seq(i, 3, 2)
    feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    feature_vector = np.array([feature_vector])
    try:
        prediction = model.predict(feature_vector)
        predictions.append(prediction)
        ct += 1
    except: 
        print 'error'
print 'Did not fail %s times' % ct
with open(pickled_output_file, 'w') as h:
    pickle.dump(predictions, h)
