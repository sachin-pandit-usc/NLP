#!/usr/bin/python2.7 -tt

import sys
import codecs
from collections import defaultdict

candidate_input = defaultdict()
reference_input = defaultdict()
candidate_count = defaultdict()
reference_input = defaultdict()
candidate_clipped = defaultdict()
reference_clipped = defaultdict()

def debug_print():
    print candidate_input
    print reference_input

def read_candidate_file (filename):
    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            candidate_input[index] = str(line).strip()
            index += 1

def read_reference_file (filename):
    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            reference_input[index] = str(line).strip()
            index += 1

def check_syntax (length):
    if length != 3:
        print "Syntax: calculatebleu.py /path/to/candidate /path/to/reference"

if __name__ == "__main__":
    check_syntax(len(sys.argv))
    read_candidate_file (sys.argv[1])
    read_reference_file (sys.argv[2])
    debug_print()