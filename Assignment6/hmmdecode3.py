#!/usr/bin/python3.4 -tt


import sys
from collections import defaultdict

tag_dict = {}
end_tag_dict = {}
line_count = 0


emission_dict = {}
trans_dict = defaultdict (dict)
probability = defaultdict (dict)
backpointer = defaultdict (dict)


def print_dictionary():
    print ("WORD/TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in emission_dict:
        print ("%s %d" % (key, emission_dict[key]))

    print ("TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in tag_dict:
        print ("%s %d" % (key, tag_dict[key]))

    print ("END TAG >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key in end_tag_dict:
        print ("%s %d" % (key, end_tag_dict[key]))

    print ("Transition >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    for key1 in trans_dict:
        for key2 in trans_dict[key1]:
            print ("%s %s %d" % (key1, key2, trans_dict[key1][key2]))


def fill_dictionary (cur_dict, words):
    key = words[1].strip()
    value = words[2].strip()
    cur_dict[key] = int(value)


def read_model_file (fd):
    global emission_dict
    global tag_dict
    global end_tag_dict
    global line_count
    global trans_dict

    for line in fd:
        words = line.split()
        flag = words[0].strip()
        if "1" == flag:
            fill_dictionary (emission_dict, words)
        elif "2" == flag:
            fill_dictionary (tag_dict, words)
        elif "3" == flag:
            fill_dictionary (end_tag_dict, words)
        elif "4" == flag:
            key1 = words[1].strip()
            key2 = words[2].strip()
            value = int(words[3].strip())
            if key1 in tag_dict:
                trans_dict[key1][key2] = value/tag_dict[key1]
        elif "5" == flag:
            line_count = int(words[1].strip())


def transition_prob (flag, tag1, tag2):
    res = 0.0

    if tag1 in trans_dict:
        if tag2 in trans_dict[tag1]:
            num = trans_dict[tag1][tag2]
        else:
            return (0.00001)/line_count
    else:
        return (0.00001)/line_count

    if flag == 0:
        den = line_count
    else:
        if tag1 in tag_dict:
            den = tag_dict[tag1]
        if tag1 in end_tag_dict:
            den = den - end_tag_dict[tag1]

    if num == 0 or den == 0:
        return (0.00001)/line_count

    res = num/den
    return res


def emission_prob (tag, word):
    res = 0.0
    temp = word + "/" + tag

    if temp in emission_dict:
        num = emission_dict [temp]
    else:
        return (0.00001)/line_count

    if tag in tag_dict:
        den = tag_dict [tag]
    else:
        den = (0.00001)/line_count

    if num == 0 or den == 0:
        return (0.000001)/line_count

    res = num/den
    return res


def assign_tag (fdw, words):
    global probability
    global backpointer

    word = words[0].strip()
    for tag in tag_dict:
        probability[tag, 0] = transition_prob (0, "start_state_q0", tag) * emission_prob (tag, word)
        backpointer[tag, 0] = "start_state_q0"

    for t in range (1, len(words)):
        for tag in tag_dict:
            max_prob = -999999
            max_tag = ""
            for inner_tag in tag_dict:
                temp = probability [inner_tag, t-1] * transition_prob (1, inner_tag, tag) * emission_prob (tag, words[t].strip())
                if temp > max_prob:
                    max_prob = temp
                    max_tag = inner_tag
            probability[tag, t] = max_prob
            backpointer[tag, t] = max_tag


    max_prob = -999999
    max_tag = ""
    for tag in tag_dict:
        temp = probability [tag, len(words)-1]
        if temp > max_prob:
            max_prob = temp
            max_tag = tag

    tagged_sentence = words[len(words)-1].strip() + "/" + max_tag
    for t in reversed(range (len(words)-1)):
        temp = backpointer[max_tag, t+1]
        tagged_sentence = words[t].strip() + "/" + temp + " " + tagged_sentence
        max_tag = temp

    fdw.write(tagged_sentence + "\n")

def read_raw_file (fd):
    global probability
    global backpointer

    fdw = open ("hmmoutput.txt", "w")
    fdw = open ("hmmoutput.txt", "a")
    for line in fd:
        probability = defaultdict (dict)
        backpointer = defaultdict (dict)
        words = line.split()
        assign_tag (fdw, words)


def process_model_file (filename):
    try:
        fd = open (filename, "r")
        read_model_file (fd)
    except FileNotFoundError:
        print ("Can't open the file for reading")

def process_raw_file (filename):
    try:
        fd1 = open (filename, "r")
        read_raw_file(fd1)
    except:
        print ("Can't open the file for reading")


def syntax_check():
    if len(sys.argv) != 2:
        print ("Syntax: ./hmmdecode.py /path/to/input")
        exit()


def main():
    syntax_check()
    process_model_file("hmmmodel.txt")
    #print_dictionary()
    process_raw_file (sys.argv[1])

if __name__ == "__main__":
    main()
