#!/usr/bin/python3 -tt

import sys
import os
import math
import string
import re

word_dict = {}
prob1 = 0.0
prob2 = 0.0
prob3 = 0.0
prob4 = 0.0

def write_output (fwrite, subdir, file):
    global prob1
    global prob2
    global prob3
    global prob4

    max_value = max (prob1, prob2, prob3, prob4)

    if (prob1 == max_value):
        temp = ""
        temp += "truthful" + " " + "positive" + " " + os.path.join (subdir, file) + "\n"
        fwrite.write (temp)
    elif (prob2 == max_value):
        temp = ""
        temp += "truthful" + " " + "negative" + " " + os.path.join (subdir, file) + "\n"
        fwrite.write (temp)
    elif (prob3 == max_value):
        temp = ""
        temp += "deceptive" + " " + "positive" + " " + os.path.join (subdir, file) + "\n"
        fwrite.write (temp)
    elif (prob4 == max_value):
        temp = ""
        temp += "deceptive" + " " + "negative" + " " + os.path.join (subdir, file) + "\n"
        fwrite.write (temp)



def calculate_prob (fwrite, subdir, file, word):
    global prob1
    global prob2
    global prob3
    global prob4

    #print ("Word = %s\n" % word)
    if word in word_dict:
        temp = word_dict[word]
        count = 0
        for buf in temp.split():
            if (count == 0):
                #print ("buf = %s, log = %f" % (buf, math.log (float(buf))))
                prob1 += math.log (float(buf))
            elif (count == 1):
                prob2 += math.log (float(buf))
            elif (count == 2):
                prob3 += math.log (float(buf))
            elif (count == 3):
                prob4 += math.log (float(buf))
            count += 1


def process_filename (fwrite, subdir, file):
    try:
        if (file != ".DS_Store"):
            global prob1
            prob1 = 0
            global prob2
            prob2 = 0
            global prob3
            prob3 = 0
            global prob4
            prob4 = 0
            filepath = os.path.join (subdir, file)
            #print ("%s\n" % (file))
            fd1 = open (filepath, "r")
            for line in fd1:
                words = re.sub('[^A-Za-z]',' ',line).split()
                for word in words:
                    '''
                    for c in string.punctuation:
                        word = word.replace (c,"")
                    '''
                    word = word.lower()
                    calculate_prob (fwrite, subdir, file, word)
            #print ("%f %f %f %f\n" % (prob1, prob2, prob3, prob4))
            write_output (fwrite, subdir, file)
    except FileNotFoundError:
        print ("File not found\n")

def traverse_file():
    fwrite = open ("nboutput.txt", "w")
    for subdir, dirs, files in os.walk (sys.argv[1]):
        if (len(files) != 0):
            for file in files:
                process_filename (fwrite, subdir, file)


def print_classification():
    for i in word_dict:
        print ("%s -> %s\n" % (i, word_dict[i]))


def read_model_file ():
    try:
        fd = open ("nbmodel.txt", "r")
        for line in fd:
            count = 0
            word_buf = ""
            for word in line.split():
                if (count == 0):
                    word_buf = word
                    word_buf_second = ""
                else:
                    word_buf_second += " " + word
                if (count == 4 and len(word_buf) != 0):
                    word_dict[word_buf] = word_buf_second
                count += 1
    except FileNotFoundError:
        print ("File does not exist\n")


def check_syntax():
    if (len (sys.argv) != 2):
        print ("Syntax: ./nbclassify <file_path>")
        exit()

def main():
    #print ("\n\n Calculate prior probability !!!!!\n")
    #exit ()
    check_syntax ()
    read_model_file()
    #print_classification()
    traverse_file()

if __name__ == "__main__":
    main()
