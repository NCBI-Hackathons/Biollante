import sys
import random

# Substitute a given nucleotide with another
# Parameters: bp (string)
# Output: new basepair (string)
def replace_basepair(bp):
    nucleotides = ['A', 'T', 'C', 'G']
    if bp in nucleotides:
        nucleotides.remove(bp)
        return nucleotides[random.randint(0, 2)]
    else:
        return bp

# Randomly switch nucleotides in a sequence with stated frequency
# Parameters: sequence (string), swapFreq (int)
# Output: new sequence (string)
def insert_swaps(sequence, swapFreq):
    sequence = sequence.upper()
    swaps = int(len(sequence)*swapFreq)
    indices = random.sample(range(0, len(sequence) - 1), swaps)
    for i in indices:
        nucleotides = list(sequence)
        nucleotides[i] = replace_basepair(nucleotides[i])
        sequence = ''.join(nucleotides)
    return sequence
