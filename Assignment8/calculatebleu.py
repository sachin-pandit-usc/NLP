#!/usr/bin/python2.7 -tt

import sys
import codecs
from collections import defaultdict
import glob, os
import string
import math

#TODO : Handle encoding

candidate_input = defaultdict()
reference_input = defaultdict()
candidate_count = defaultdict()
reference_count = defaultdict()
candidate_clipped = defaultdict()
bp = 0.0
wn_pn = 0.0
bleu = 0.0

def calculate_bleu():
    bleu = pow(bp, wn_pn)
    #print "Final bleu value =", bleu
    fdw = open("bleu_out.txt", "w")
    fdw.write(str(bleu))
    fdw.close()

def calculate_pn():
    global wn_pn

    for ngrams_index in range(1, 5):
        pn = 0.0
        num = 0
        den = 0
        for line_index in candidate_count[0]:
            num += candidate_clipped[line_index][ngrams_index]["wordcount_clip_ngrams"]
            den += candidate_count[0][line_index][ngrams_index]["wordcount_cand_ngrams"]
        if num == 0 or den == 0:
            pn = 0
        else:
            pn = float(num)/den
        wn_pn += float(pn)/4.0

def brevity_penalty():
    global bp

    r = 0
    c = 0
    for cand_key in candidate_input:
        close_temp = 0
        r_value = 0
        cand_list = str(candidate_input[cand_key]).split()
        c += len(cand_list)
        for ref_index in reference_input:
            ref_list = str(reference_input[ref_index][cand_key]).split()
            temp_abs = abs(len(cand_list) - len(ref_list))
            if temp_abs < close_temp or ref_index == 0:
                close_temp = temp_abs
                r_value = len(ref_list)
        r += r_value

    if c > r:
        bp = 1
        #print "Brevity Penalty = ", bp
    else:
        power_part = 1 - float(r)/float(c)
        bp = math.exp(power_part)
        #print "Brevity Penalty =", bp


def clip_each_ngrams(candidate_clipped, line_index, ngrams_index):
    global  candidate_count

    cand_wordcount = 0
    clip_wordcount = 0

    for candid_key in candidate_count[0][line_index][ngrams_index]:
        max_list = []
        #print line_index, ngrams_index, candid_key #TODO Need to check if one of the reference file length is not matched with the candidate!!
        cand_wordcount += candidate_count[0][line_index][ngrams_index][candid_key]
        for ref_key in reference_count:
            if candid_key in reference_count[ref_key][line_index][ngrams_index]:
                max_list.append(reference_count[ref_key][line_index][ngrams_index][candid_key])

        if max_list:
            max_ref_count = max(max_list)
            temp = min(candidate_count[0][line_index][ngrams_index][candid_key],
                       max_ref_count)
            candidate_clipped[line_index][ngrams_index][candid_key] = temp
            clip_wordcount += temp

    candidate_count[0][line_index][ngrams_index]["wordcount_cand_ngrams"] = cand_wordcount
    candidate_clipped[line_index][ngrams_index]["wordcount_clip_ngrams"] = clip_wordcount


def clip_the_words():
    global candidate_clipped

    candidate_clipped = defaultdict()
    for line_index in candidate_count[0]:
        candidate_clipped[line_index] = defaultdict()
        for ngrams_index in range(1, 5):
            candidate_clipped[line_index][ngrams_index] = defaultdict()
            clip_each_ngrams(candidate_clipped, line_index, ngrams_index)


def find_ngrams(input_list, n):
    return zip(*[input_list[i:] for i in range(n)])

def debug_print():
    print candidate_input
    print reference_input
    print candidate_count
    print reference_count


def store_ngrams (dictionary, line_string, fileindex, lineindex):
    line_list = []
    dictionary[fileindex][lineindex] = defaultdict()
    line_list = line_string.split()
    for ngrams_index in range(1, 5):
        dictionary[fileindex][lineindex][ngrams_index] = defaultdict()
        ngrams_list = find_ngrams(line_list, ngrams_index)
        for tuple in ngrams_list:
            ngrams_string = ""
            for word in tuple:
                ngrams_string += word + " "
            ngrams_string = ngrams_string.strip()
            if ngrams_string in dictionary[fileindex][lineindex][ngrams_index]:
                dictionary[fileindex][lineindex][ngrams_index][ngrams_string] += 1
            else:
                dictionary[fileindex][lineindex][ngrams_index][ngrams_string] = 1


def read_candidate_file (filename):
    global candidate_input
    global candidate_count

    candidate_count[0] = defaultdict()
    with open(filename, "r") as fd:
        index = 0
        for line in fd:
            temp_line = str(line).strip().lower()
            '''
            for c in string.punctuation:
                temp_line = temp_line.replace(c, "")
            '''
            candidate_input[index] = temp_line
            store_ngrams (candidate_count, temp_line, 0, index)
            index += 1
    fd.close()


def read_reference_file (filename, filecount):
    with open(filename, "r") as fd:
        reference_input[filecount] = defaultdict()
        index = 0
        for line in fd:
            temp_line = str(line).strip().lower()
            '''
            for c in string.punctuation:
                temp_line = temp_line.replace(c, "")
            '''
            reference_input[filecount][index] = temp_line
            store_ngrams(reference_count, temp_line, filecount, index)
            index += 1
    fd.close()

def read_reference_directory (directory):
    global reference_input
    global reference_count

    filecount = 0
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            reference_count[filecount] = defaultdict()
            filename = directory + "/" + file
            read_reference_file(filename, filecount)
            filecount += 1
    elif os.path.isfile(directory):
        reference_count[filecount] = defaultdict()
        read_reference_file(directory, filecount)

def check_syntax (length):
    if length != 3:
        print "Syntax: calculatebleu.py /path/to/candidate /path/to/reference"

if __name__ == "__main__":
    check_syntax(len(sys.argv))
    read_candidate_file (sys.argv[1])
    read_reference_directory (sys.argv[2])
    clip_the_words()
    brevity_penalty()
    #debug_print()
    calculate_pn()
    calculate_bleu()
    #debug_print()