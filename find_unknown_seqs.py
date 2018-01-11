'''
Created on Jan 10, 2018

@author: erikedlund
'''
from argparse import ArgumentParser
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio.Alphabet import IUPAC
import logging
import multiprocessing
import os
import sys

from pysam import AlignmentFile


QUALITY_CUTOFF = '39' #TODO decide on a default quality score cutoff

logger = logging.getLogger('find_unknown_seqs')

def parse_magic_blast_out(sam_output, working_dir, cutoff):
    unknown_out = os.path.join(working_dir, 'unknown.fasta')
    with open(unknown_out, 'w') as unk_out:
        bf = AlignmentFile(sam_output, 'r', check_header=False, check_sq=False)
        for r in bf.fetch(until_eof=True):
            if r.is_unmapped or (r.qual and r.qual < cutoff):
                sequences = SeqRecord(Seq(r.query, IUPAC.IUPACUnambiguousDNA), id = r.qname, description='')
                SeqIO.write(sequences, unk_out, "fasta")
    return unknown_out

if __name__ == '__main__':
    parser = ArgumentParser(description="This script parses the output SAM file from a Magic BLAST " + 
                            " run and dumps input sequences that are unaligned or below a quality score cutoff to a fasta.")
    parser.add_argument('-q', '--query', help='path to a SAM file', required = True)
    parser.add_argument('-c', '--cutoff', help='quality score cutoff', default=QUALITY_CUTOFF, required = False)
    parser.add_argument('-w', '--working-dir', help='working directory', default='.', required = False)
   
    args = vars(parser.parse_args())
    cutoff = float(args['cutoff'])
    output_fasta = parse_magic_blast_out(args['query'], args['working_dir'], cutoff)
    logging.info("Compiled unaligned and low scoring aligned sequences to " + output_fasta)
    sys.exit(0)