#!/usr/bin/python3.4 -tt


import sys

word_dict = {}
tag_dict = {}
end_tag_dict = {}
trans_dict = {}


def print_dictionary():

    print ("WORD/TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in word_dict:
        print ("%s %d" % (key, word_dict[key]))

    print ("TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in tag_dict:
        print ("%s %d" % (key, tag_dict[key]))

    print ("END TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in end_tag_dict:
        print ("%s %d" % (key, end_tag_dict[key]))

    print ("Transition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in trans_dict:
        print ("%s %d" % (key, trans_dict[key]))


def fill_dictionary (cur_dict, words):
    key = words[1].strip()
    value = words[2].strip()
    cur_dict[key] = int(value)


def read_model_file (fd):
    global word_dict
    global tag_dict
    global end_tag_dict

    for line in fd:
        words = line.split()
        flag = words[0].strip()
        if "1" == flag:
            fill_dictionary (word_dict, words)
        elif "2" == flag:
            fill_dictionary (tag_dict, words)
        elif "3" == flag:
            fill_dictionary (end_tag_dict, words)
        elif "4" == flag:
            key1 = words[1].strip()
            key2 = words[2].strip()
            value = words[3].strip()
            key = key1 + "!@#$%" + key2
            trans_dict[key] = int(value)


def process_model_file (filename):
    try:
        fd = open (filename, "r")
        read_model_file (fd)
    except FileNotFoundError:
        print ("Can't open the file for reading")


def syntax_check():
    if len(sys.argv) != 2:
        print ("Syntax: ./hmmdecode.py /path/to/input")
        exit()


def main():
    #syntax_check()
    process_model_file("hmmmodel.txt")
    print_dictionary()

if __name__ == "__main__":
    main()
