#!/usr/bin/python2.7 -tt

import sys
import codecs
from collections import defaultdict
import glob, os
import string


candidate_input = defaultdict()
reference_input = defaultdict()
candidate_count = defaultdict()
reference_count = defaultdict()
candidate_clipped = defaultdict()

def clip_the_words():
    global candidate_clipped
    global reference_clipped

    candidate_clipped[0] = defaultdict()
    for candid_key in candidate_count[0]:
        max_list = []
        for ref_key in reference_count:
            if candid_key in reference_count[ref_key]:
                max_list.append(reference_count[ref_key][candid_key])

        if max_list:
            max_ref_count = max(max_list)
            candidate_clipped[0][candid_key] = min(candidate_count[0][candid_key], max_ref_count)


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def debug_print():
    print candidate_input
    print reference_input
    print candidate_count
    print reference_count


def store_ngrams (dictionary, line_string, fileindex):
    line_list = []
    line_list = line_string.split()
    ngrams_list = find_ngrams(line_list, 1)
    for tuple in ngrams_list:
        ngrams_string = ""
        for word in tuple:
            ngrams_string += word + " "
        ngrams_string = ngrams_string.strip()
        if ngrams_string in dictionary[fileindex]:
            dictionary[fileindex][ngrams_string] += 1
        else:
            dictionary[fileindex][ngrams_string] = 1


def read_candidate_file (filename):
    global candidate_input
    global candidate_count

    candidate_count[0] = defaultdict()
    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            temp_line = str(line).strip().lower()
            for c in string.punctuation:
                temp_line = temp_line.replace(c, "")
            candidate_input[index] = temp_line
            store_ngrams (candidate_count, temp_line, 0)
            index += 1
    fd.close()

def read_reference_directory (directory):
    global reference_input
    global reference_count

    filecount = 0
    for file in os.listdir(directory):
        reference_count[filecount] = defaultdict()
        filename = directory + "/" + file
        with open(filename, "r") as fd:
            index = 0
            for line in fd:
                temp_line = str(line).strip().lower()
                for c in string.punctuation:
                    temp_line = temp_line.replace(c, "")
                reference_input[index] = temp_line
                store_ngrams (reference_count, temp_line, filecount)
                index += 1
        filecount += 1
        fd.close()

def check_syntax (length):
    if length != 3:
        print "Syntax: calculatebleu.py /path/to/candidate /path/to/reference"

if __name__ == "__main__":
    check_syntax(len(sys.argv))
    read_candidate_file (sys.argv[1])
    read_reference_directory (sys.argv[2])
    clip_the_words()
    debug_print()