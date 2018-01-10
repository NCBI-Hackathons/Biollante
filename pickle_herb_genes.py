import csv
import pickle

herb_seqs = []

with open('data/herbicide_resistant_weed_sequences.csv', 'rb') as csvfile:

     herb_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')

     for row in herb_reader:

        l = row[0].split(',')

        herb_seqs.append(l[1])

print len(herb_seqs)
herb_seqs.pop(0)
print len(herb_seqs)

with open('herb_seqs.p', 'wb')as h:

    pickle.dump(herb_seqs, h)
