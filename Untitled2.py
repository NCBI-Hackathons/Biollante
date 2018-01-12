
# coding: utf-8

# In[36]:

import csv
import numpy as np
import pickle
import pandas as pd


# In[63]:

blastseq=pd.read_csv('example_head.txt', sep='\t',header=None,usecols=[1,2,3,4,5,6,7,8,9],names=['The alignment score', 'Read paired','Read mapped in proper pair','Read unmapped','Mate unmapped','Read reverse strand','Mate reverse strand','First in pair','Second in pair'])


# In[64]:

blastseq


# In[67]:

clean_sequences = []

samples = 10

feature_vector=list(blastseq)


for i in blastseq[:samples]:

    if blastseq.index(i) % 100 == 0:

        print blastseq.index(i)

    #z, feature_vector = featurize_seq(i, 3, 2)
    feature_vector = list(blastseq)   
    clean_sequences.append(feature_vector)


# In[69]:

feature_vector = list(blastseq) 
feature_vector


# In[38]:

example

