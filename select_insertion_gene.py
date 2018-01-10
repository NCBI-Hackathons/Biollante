import pickle
import random

with open('bacmet_seqs.p') as h:

    bacmet_seqs = pickle.load(h)

with open('herb_seqs.p') as h:

    herb_seqs = pickle.load(h)

#print len(bacmet_seqs)
#print len(herb_seqs)

def select_insertion_gene(gene_list, insertion_length_min, insertion_length_max):

    while 1:

        try:

            insertion_length = random.randint(insertion_length_min, insertion_length_max)

            insertion_gene = random.choice(gene_list)

            insertion_start_index = random.randint(0, insertion_length - 1)

            return insertion_gene[insertion_start_index : insertion_start_index + insertion_length]

        except:

            pass
