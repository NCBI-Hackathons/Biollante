import csv
from xgboost import XGBClassifier
import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from featurize_seq import *


herb_seqs = []

with open('data/contaminated_sequences.csv', 'rb') as csvfile:

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

with open('data/non_contaminated_sequences.csv', 'rb') as csvfile:

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

bags = 10

model = XGBClassifier()

bag_size = len(clean_seqs)/bags

for b in range(bags):

    print 'creating bag', b

    start_index = bag_size * b
    end_index = bag_size * (b + 1)

    #kmer_list = generate_all_unique_kmers(6)
    #print len(kmer_list)

    for i in herb_seqs[start_index:end_index]:

        if herb_seqs.index(i) % 1000 == 0:

            print herb_seqs.index(i)

        #feature_vector = call seq2vec here
        feature_vector = [0]

        contaminated_sequences.append(feature_vector)


    contaminated_labels = [1] * len(contaminated_sequences)

    for i in clean_seqs[start_index:end_index]:

        if clean_seqs.index(i) % 1000 == 0:

            print clean_seqs.index(i)

        #feature_vector = call seq2vec here
        feature_vector = [1]

        clean_sequences.append(feature_vector)


    clean_labels = [0] * len(clean_sequences)

    seed = 777
    test_size = 0.02

    contaminated_sequences.extend(clean_sequences)
    contaminated_labels.extend(clean_labels)

    X = np.array(contaminated_sequences)
    Y = np.array(contaminated_labels)

    #print X.shape
    #print Y.shape

    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state = seed)




    print 'training on bag', b

    model.fit(X_train, y_train)

    # make predictions for test data
    print 'predicting...'
    y_pred = model.predict(X_test)
    predictions = [round(value) for value in y_pred]

    # evaluate predictions
    accuracy = accuracy_score(y_test, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

    model_checkpoint_savename = 'xgb_vector_embedding_model_bag_' + str(b) + '.p'

    with open(model_checkpoint_savename, 'wb') as h:

        pickle.dump(model, h)


#with open('resistance_feature_vectors_2.p', 'wb') as h:

#    pickle.dump(featurized_resistance, h)

#z, feature_vector = featurize_seq(herb_seqs[0], 3, 2)
