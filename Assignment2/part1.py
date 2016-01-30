#!/usr/bin/python3.4 -tt

import sys
import os
import string

truth_pos = {}
truth_neg = {}
decep_pos = {}
decep_neg = {}

def check_and_increment (dict_var, word):
    #print ("Word = %s" % word)
    if word in dict_var:
        dict_var[word] += 1
    else:
        dict_var[word] = 1

def print_dictionary ():
    print ("TRUTHFUL NEGATIVE------------------------------\n")
    for i in truth_neg:
        if (len (i) != 0):
            print ("%s : %s" % (i, truth_neg[i]))

    print ("TRUTHFUL POSITIVE-------------------------------\n")
    for i in truth_pos:
        if (len (i) != 0):
            print ("%s : %s" % (i, truth_pos[i]))

    print ("DECEPTIVE POSITIVE------------------------------\n")
    for i in decep_pos:
        if (len (i) != 0):
            print ("%s : %s" % (i, decep_pos[i]))

    print ("DECEPTIVE NEGATIVE-------------------------------\n")
    for i in decep_neg:
        if (len (i) != 0):
            print ("%s : %s" % (i, decep_neg[i]))

def generate_dictionary (word, case_number):
    if (case_number == 1):
        check_and_increment (truth_neg, word)
    elif (case_number == 2):
        check_and_increment (decep_neg, word)
    elif (case_number == 3):
        check_and_increment (truth_pos, word)
    elif (case_number == 4):
        check_and_increment (decep_pos, word)

def read_file (filename, case_number):
    try:
        temp = ""
        fd = open (filename, "r")
        for line in fd:
            for word in line.split():
                for c in string.punctuation:
                    word = word.replace(c,"")
                word = word.lower()
                generate_dictionary (word, case_number)
                #print ("Word = %s" % word)
            #print ("%s" % (word))

    except FileNotFoundError:
        print ("Cant open the file\n")


def process_filename(subdir, file):
    if (file != ".DS_Store"):
        temp = os.path.join (subdir, file)
        if (("negative" in temp) and ("truthful" in temp)):
            print ("\n%s is %s and %s" % (file, "negative", "truthful"))
            read_file (temp, 1)
            #print_dictionary ()
        if (("negative" in temp) and ("deceptive" in temp)):
            print ("\n%s is %s and %s" % (file, "negative", "deceptive"))
            read_file (temp, 2)
        if (("positive" in temp) and ("truthful" in temp)):
            print ("\n%s is %s and %s" % (file, "positive", "truthful"))
            read_file (temp, 3)
        if (("positive" in temp) and ("deceptive" in temp)):
            print ("\n%s is %s and %s" % (file, "positive", "deceptive"))
            read_file (temp, 4)

def main():
    for subdir, dirs, files in os.walk ("op_spam_train"):
        if (len(files) != 0):
            for file in files:
                process_filename (subdir, file)

    #print_dictionary ()

if __name__ == "__main__":
    main ()
