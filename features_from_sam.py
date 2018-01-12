import re
from xgboost import XGBClassifier
import numpy as np
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

def cigar_chopper(cigar):

    sms = [0,0,0]

    current_str = ''
    i = 0

    for c in cigar:



        if c == 'S':

            if current_str != '':

                sms[i] = current_str
                current_str = ''
                i += 1

        if c == 'M':

            if i == 0:

                i += 1
                sms[i] = current_str
                current_str = ''
                i += 1

            if i == 1:

                sms[i] = current_str
                current_str = ''
                i += 1
        else:

            if c not in ['S', 'M']:

                current_str += c

    return sms

def get_lines(filename):
    with open(filename, 'rb') as f:
        features = []
        lines = f.readlines()

        #print len(herb_lines)

        for l in lines:

            if l[0] != '@':

                try:

                    current_row = l.split()

                    #bin_string = format(int(current_row[1]), 'b')
                    #print bin_string
                    #print current_row[5]
                    chopped_cigar = cigar_chopper(current_row[5])
                    #current_row[2],
                    feature_vector = [int(current_row[1]), int(current_row[3]), int(chopped_cigar[0]), int(chopped_cigar[1]), int(chopped_cigar[2])]

                    features.append(feature_vector)

                except:

                    pass

        return lines, features

def compute_accuracy(contam_filename, non_contam_filename, speciesname):
    contam_lines, contam_features = get_lines(contam_filename)
    non_lines, non_contam_features = get_lines(non_contam_filename)

    #print len(non_contam_features)
    #print len(contam_features)
    #print len(contam_features)

    clean_labels = [0] * len(non_contam_features)
    contam_labels = [1] * len(contam_features)

    non_contam_features.extend(contam_features)
    clean_labels.extend(contam_labels)

    X = np.array(non_contam_features)
    Y = np.array(clean_labels)
    print('')

    # make predictions for test data
    print 'predicting for', speciesname, '...'
    y_pred = model.predict(X)
    predictions = [round(value) for value in y_pred]

    # evaluate predictions
    accuracy = accuracy_score(Y, predictions)
    print("Accuracy: %.2f%%" % (accuracy * 100.0))

herb_contam_filename = 'data/bacmet_contaminated_sequences_vs_plantdb.sam.txt'
non_contam_filename = 'data/non_contaminated_sequences_vs_plantdb.sam.txt'

herb_lines, herb_features = get_lines(herb_contam_filename)
non_lines, non_contam_features = get_lines(non_contam_filename)

#print len(non_contam_features)
#print len(herb_features)
#print len(contam_features)

clean_labels = [0] * len(non_contam_features)
herb_labels = [1] * len(herb_features)

non_contam_features.extend(herb_features)
clean_labels.extend(herb_labels)

X = np.array(non_contam_features)
Y = np.array(clean_labels)

seed = 777
test_size = 0.1

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size = test_size, random_state = seed)

#print X_train.shape, y_train.shape
#print X_test.shape, y_test.shape

print('')
print 'training...'
model = XGBClassifier()
model.fit(X_train, y_train)

# make predictions for test data
print 'predicting...'
y_pred = model.predict(X)
predictions = [round(value) for value in y_pred]

# evaluate predictions
accuracy = accuracy_score(Y, predictions)
print("Accuracy: %.2f%%" % (accuracy * 100.0))

non_contam_filename = ['data/non_contaminated_oryza_sequences_vs_plantdb.sam.txt']
contam_filename = ['data/bacmet_contaminated_oryza_sequences_vs_plantdb.sam.txt']
speciesname = ['Oryza']

# evaluate predictions for holdout species
for i in range(len(speciesname)):
    compute_accuracy(contam_filename[i], non_contam_filename[i], speciesname[i])

# find predicted percentage of plant DNA in sample
srr_filename = 'data/SRR5069665_vs_PlantDB.sam'
srr_line, srr_features = get_lines(srr_filename)

print('')
X = np.array(srr_features)
x_pred = model.predict(X)
percent_plant = sum(x_pred) / float(len(x_pred))
print 'Predicted percent plant DNA: %.2f%%' % (percent_plant * 100)
