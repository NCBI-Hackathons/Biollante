import pickle

def reverse_translate_protein(protein_seq):

    codon_table = {
                      'F' : ['TTT', 'TTC'],
                      'L' : ['TTA', 'TTG'],
                      'S' : ['TCT', 'TCC', 'TCA', 'TCG'],
                      'Y' : ['TAT', 'TAC'],
                      'C' : ['TGC', 'TGT'],
                      'W' : ['TGG'],
                      'L' : ['CTA', 'CTT', 'CTG', 'CTC'],
                      'P' : ['CCA', 'CCT', 'CCG', 'CCC'],
                      'H' : ['CAC', 'CAT'],
                      'Q' : ['CAA', 'CAG'],
                      'R' : ['CGA', 'CGT', 'CGG', 'CGC'],
                      'I' : ['ATA', 'ATT', 'ATC'],
                      'M' : ['ATG'],
                      'T' : ['ACA', 'ACT', 'ACG', 'ACC'],
                      'N' : ['AAT', 'AAC'],
                      'K' : ['AAA', 'AAG'],
                      'S' : ['AGT', 'AGC'],
                      'R' : ['AGA', 'AGG'],
                      'V' : ['GTA', 'GTT', 'CTG', 'GTC'],
                      'A' : ['GCA', 'GCT', 'GCG', 'GCC'],
                      'D' : ['GAT', 'GAC'],
                      'E' : ['GAA', 'GAG'],
                      'G' : ['GGA', 'GGT', 'GGG', 'GGC']

      }

    dna_from_prot = ''

    for a in protein_seq:

        try:
            dna_from_prot += (codon_table[a][0])

        except:
            dna_from_prot += a

    return dna_from_prot


bacmet_filename = 'data/BacMet2_predicted_database.fasta'

with open(bacmet_filename) as f:

    bacmet_lines = f.readlines()

bacmet_sequences = [] # {}

for i in range(len(bacmet_lines)):

    current_line = bacmet_lines[i].rstrip()

    if current_line[0] == ">":

        bacmet_sequences.append('')

    else:

        bacmet_sequences[-1] += reverse_translate_protein(current_line)

with open('bacmet_seqs.p', 'wb') as h:

    pickle.dump(bacmet_sequences, h)
