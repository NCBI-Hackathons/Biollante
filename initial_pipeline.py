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
parser.add_argument('-s', '--samples', help='Number of samples', default='20000', required = False)
parser.add_argument('-f', '--file', help='dna2vec model file',
                    default='dna2vec/results/refseq-training-vec-k3to8.w2v', required = False)

args = vars(parser.parse_args())

samples = int(args['samples'])

print 'Using %s samples...' % samples

filepath = args['file']

if not os.path.exists(filepath):
    'dna2vec model file does not exist: ' + filepath
    sys.exit(1)
print 'Using dna2vec model: ' + filepath

mk_model = MultiKModel(filepath)

herb_seqs = []

with open('bacmet_contaminated_sequences.csv', 'rb') as csvfile:

     herb_reader = csvfile.readlines() #(csvfile, delimiter=' ', quotechar='|')

     for row in herb_reader[1:]:

        r = row.split(',')
        r.pop(0)

        r = [i.rstrip() for i in r]

        for i in r:
            if len(i) != 500:
                print len(i)
                print(i)

        herb_seqs.extend(r)

clean_seqs = []

with open('non_contaminated_sequences.csv', 'rb') as csvfile:

     clean_reader = csvfile.readlines() #(csvfile, delimiter=' ', quotechar='|')

     for row in clean_reader[1:]:

        r = row.split(',')
        r.pop(0)

        r = [i.rstrip() for i in r]

        for i in r:
            if len(i) != 500:
                print len(i)
                print(i)

        clean_seqs.extend(r)

print len(clean_seqs)

contaminated_sequences = []
clean_sequences = []

kmer_len = 8
kmer_list = generate_all_unique_kmers(kmer_len)
print len(kmer_list)

for i in herb_seqs[:samples]:

    if herb_seqs.index(i) % 100 == 0:

        print herb_seqs.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    contaminated_sequences.append(feature_vector)
    #contaminated_sequences.append(flatten_feature_vector(z))

contaminated_labels = [1] * len(contaminated_sequences)



for i in clean_seqs[:samples]:

    if clean_seqs.index(i) % 100 == 0:

        print clean_seqs.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    clean_sequences.append(feature_vector)
    #clean_sequences.append(flatten_feature_vector(z))

clean_labels = [0] * len(clean_sequences)

seed = 777
test_size = 0.1


contaminated_sequences.extend(clean_sequences)
contaminated_labels.extend(clean_labels)

X = np.array(contaminated_sequences)
Y = np.array(contaminated_labels)

print X.shape
print Y.shape

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state = seed)



# fit model no training data
print 'training...'
model = XGBClassifier()
model.fit(X_train, y_train)

# make predictions for test data
print 'predicting...'
y_pred = model.predict(X_test)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

pickle_file = 'models/' + (str)(2*samples/1000) + 'K_samples_model.p'
with open(pickle_file, 'wb') as h:
    pickle.dump(model, h)

#with open('resistance_feature_vectors_2.p', 'wb') as h:

#    pickle.dump(featurized_resistance, h)

#z, feature_vector = featurize_seq(herb_seqs[0], 3, 2)

#print len(z)
