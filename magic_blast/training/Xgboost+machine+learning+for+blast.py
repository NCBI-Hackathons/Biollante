
# coding: utf-8

# In[ ]:

import csv
from xgboost import XGBClassifier
import numpy as np
import pandas as  pd
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from featurize_seq import *
from dna2vec.multi_k_model import MultiKModel


#artificial contaminated seq
contamseq=pd.read_csv('herb_contaminated_sequences_vs_plantdb_table.csv', sep='\t',header=None,usecols=[1,2,3,4,5,6,7,8,9],names=['The alignment score', 'Read paired','Read mapped in proper pair','Read unmapped','Mate unmapped','Read reverse strand','Mate reverse strand','First in pair','Second in pair'])

#non-contaminated srr seq, which contains some bacteria and other DNA fragment
blastseq=pd.read_csv('on_contaminated_sequences_vs_plantdb_table.csv', sep='\t',header=None,usecols=[1,2,3,4,5,6,7,8,9],names=['The alignment score', 'Read paired','Read mapped in proper pair','Read unmapped','Mate unmapped','Read reverse strand','Mate reverse strand','First in pair','Second in pair'])


#
contaminated_sequences = [] 
clean_sequences = [] 

samples = 20000

contam_vals = contamseq.get_values()

#select mapped reads to clean_sequence and unmapped reads to contaminated_sequences
for i in contam_vals:

    feature_vector = list(i)   
    if contamseq['Read unmapped'][i]=0:
        clean_sequences.append(feature_vector)
    else:
        contaminated_sequences.append(feature_vector) 
    
    
blast_vals = blastseq.get_values()

for i in blast_vals:

    feature_vector = list(i) 
    if blastseq['Read unmapped'][i]==0:
        clean_sequences.append(feature_vector)
    else:
        contaminated_sequences.append(feature_vector) 
        

contaminated_labels = [1] * len(contaminated_sequences)

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


#with open('resistance_feature_vectors_2.p', 'wb') as h:

#    pickle.dump(featurized_resistance, h)

#z, feature_vector = featurize_seq(herb_seqs[0], 3, 2)

#print len(z)
    
    

