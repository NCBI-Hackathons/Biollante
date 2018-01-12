import csv
import numpy as np
import pickle
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from featurize_seq import *
from dna2vec.multi_k_model import MultiKModel


filepath = 'dna2vec/pretrained/dna2vec-20161219-0153-k3to8-100d-10c-29320Mbp-sliding-Xat.w2v'
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

samples = 50000

kmer_len = 8
kmer_list = generate_all_unique_kmers(kmer_len)
print len(kmer_list)

for i in herb_seqs[:samples]:

    if herb_seqs.index(i) % 100 == 0:

        print herb_seqs.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    #feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    feature_vector = featurize_seq(i, kmer_len, kmer_len, kmer_list)
    contaminated_sequences.append(feature_vector)
    #contaminated_sequences.append(flatten_feature_vector(z))

contaminated_labels = [1] * len(contaminated_sequences)



for i in clean_seqs[:samples]:

    if clean_seqs.index(i) % 100 == 0:

        print clean_seqs.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    #feature_vector = embedding_featurize_seq(i, mk_model, kmer_len, kmer_len, kmer_list)
    feature_vector = featurize_seq(i, kmer_len, kmer_len, kmer_list)
    clean_sequences.append(feature_vector)
    #clean_sequences.append(flatten_feature_vector(z))

clean_labels = [0] * len(clean_sequences)

seed = 777
test_size = 0.1

X_clean_train = np.array([clean_sequences[i] for i in range(len(clean_sequences)) if i % (int)(1/test_size) != 0])
#y_clean_train = np.array([clean_labels[i] for i in range(len(clean_labels)) if i % (int)(1/test_size) != 0])
X_contaminated_train = np.array([contaminated_sequences[i] for i in range(len(contaminated_sequences)) if i % (int)(1/test_size) != 0])
#y_contaminated_train = np.array([contaminated_labels[i] for i in range(len(contaminated_labels)) if i % (int)(1/test_size) != 0])

X_test = np.array([clean_sequences[i] for i in range(len(clean_sequences)) if i % (int)(1/test_size) == 0] + \
    [contaminated_sequences[i] for i in range(len(contaminated_sequences)) if i % (int)(1/test_size) == 0])
y_test = [clean_labels[i] for i in range(len(clean_labels)) if i % (int)(1/test_size) == 0] + \
    [contaminated_labels[i] for i in range(len(contaminated_labels)) if i % (int)(1/test_size) == 0]

# fit LDA models
print 'training...'
clean_model = LatentDirichletAllocation(verbose = 0)
clean_model.fit(X_clean_train)

contaminated_model = LatentDirichletAllocation(verbose = 0)
contaminated_model.fit(X_contaminated_train)

# make predictions for test data
print 'predicting...'

clean_scores = []
contaminated_scores = []

for i in [j for j in range(len(clean_sequences)) if j % (int)(1/test_size) == 0]:
    clean_scores.append(clean_model.score(np.array(clean_sequences[i])))
    contaminated_scores.append(contaminated_model.score(np.array(clean_sequences[i])))

for i in [j for j in range(len(contaminated_sequences)) if j % (int)(1/test_size) == 0]:
    clean_scores.append(clean_model.score(np.array(contaminated_sequences[i])))
    contaminated_scores.append(contaminated_model.score(np.array(contaminated_sequences[i])))

#print clean_scores
#print contaminated_scores

predictions = []
for i in range(len(list(clean_scores))):
    if clean_scores[i] > contaminated_scores[i]:
        predictions.append(0)
    else:
        predictions.append(1)

predictions = np.array(predictions)
y_test = np.array(y_test)

# evaluate predictions
accuracy = accuracy_score(y_test, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))


#with open('resistance_feature_vectors_2.p', 'wb') as h:

#    pickle.dump(featurized_resistance, h)

#z, feature_vector = featurize_seq(herb_seqs[0], 3, 2)

#print len(z)
