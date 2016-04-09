#!/usr/bin/python3.4 -tt

import sys
import collections

word_dict = {}
tag_dict = {}
end_tag_dict = {}

def print_frequency ():
    print ("Words >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for word in word_dict:
        print ("1 %s %s" % (word, word_dict[word]))

    print ("Tag>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for tag in tag_dict:
        temp = 0
        if tag in end_tag_dict:
            temp = end_tag_dict[tag]
        print ("2 %s %s" % (tag, tag_dict[tag] + temp))

def calculate_frequency (cur_tag_dict, word):
    tag = word[-2:]

    if word in word_dict:
        word_dict[word] += 1
    else:
        word_dict[word] = 1

    if tag in cur_tag_dict:
        cur_tag_dict[tag] += 1
    else:
        cur_tag_dict[tag] = 1
    #print ("%s, %s, %s" % (word, actual_word, tag))


def read_file (fd):
    for line in fd:
        words = line.split()
        for i in range(0, len(words)-2):
            #calculate_transition_prob (words)
            calculate_frequency (tag_dict, words[i].strip())
        calculate_frequency (end_tag_dict, words[len(words)-1].strip())
    print_frequency()

def process_file (filename):
    try:
        fd = open (filename, "r")
        read_file (fd)
    except FileNotFoundError:
        print ("Can't open the file for reading")

def check_syntax ():
    if len (sys.argv) != 2:
        print ("Syntax: ./hmmlearn3.py /path/to/input")
        exit ()

def main():
    check_syntax ()
    process_file (sys.argv[1])


if __name__ == "__main__":
    main()
