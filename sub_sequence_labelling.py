# generate long contaminated sequence

import pickle
import numpy as np

plant_genome = 'data/RefSeq/Zea_mays/GCF_000005005.2_B73_RefGen_v4_genomic.fna'

with open(plant_genome, 'rb') as h:

    plant_lines = h.readlines()

    seq = ''

    for line in plant_lines:

        if line[0] == '>':

            continue

        seq += line

        if len(seq) > 10000:

            break


with open('bacmet_seqs.p', 'rb') as h:

    bacmet_genes = pickle.load(h)

print len(bacmet_genes[3])


contam_seq = seq[:2000] + bacmet_genes[3] + seq[2000:]

print len(contam_seq)

grab_size = 500
stride = 100

draw_dataset = []

for i in range(0,len(contam_seq), stride):

    draw = contam_seq[i : i + grab_size]
    draw_dataset.append(draw)

print len(draw_dataset[0])
print len(draw_dataset)

d = np.array(draw_dataset)
print d.shape
print d[0]


with open('long_sample.p', 'wb') as h:

    pickle.dump(draw_dataset, h)
