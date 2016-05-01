#!/usr/bin/python2.7 -tt

import sys
import codecs
from collections import defaultdict

candidate_input = defaultdict()
reference_input = defaultdict()
candidate_count = defaultdict()
reference_count = defaultdict()
candidate_clipped = defaultdict()
reference_clipped = defaultdict()

def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

def debug_print():
    print candidate_input
    print reference_input
    print candidate_count
    print reference_count


def store_ngrams (dictionary, line_string):
    line_list = []
    line_list = line_string.split()
    ngrams_list = find_ngrams(line_list, 1)
    for tuple in ngrams_list:
        ngrams_string = ""
        for word in tuple:
            ngrams_string += word + " "
        ngrams_string = ngrams_string.strip()
        if ngrams_string in dictionary:
            dictionary[ngrams_string] += 1
        else:
            dictionary[ngrams_string] = 1



def read_candidate_file (filename):
    global candidate_input
    global candidate_count

    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            temp_line = str(line).strip()
            candidate_input[index] = temp_line
            store_ngrams (candidate_count, temp_line)
            index += 1

def read_reference_file (filename):
    global reference_input
    global reference_count

    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            temp_line = str(line).strip()
            reference_input[index] = temp_line
            store_ngrams (reference_count, temp_line)
            index += 1

def check_syntax (length):
    if length != 3:
        print "Syntax: calculatebleu.py /path/to/candidate /path/to/reference"

if __name__ == "__main__":
    check_syntax(len(sys.argv))
    read_candidate_file (sys.argv[1])
    read_reference_file (sys.argv[2])
    debug_print()