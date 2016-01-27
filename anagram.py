#!/usr/bin/python -tt

import sys

global output
output = []

def anagram (string_array):
    if [] == string_array or string_array == None:
        return

    if 1 == len(string_array):
        output.append (string_array[0])
        print ''.join(output)
        output.pop()
        return

    for index in range (0, len(string_array)):
        output.append (string_array[index])
        temp = string_array[:index] + string_array[index+1:]
        anagram (temp)
        output.pop()


def main():
    if len(sys.argv) != 2:
        print "Syntax : ./anagram.py <string1>"
        exit()

    string_length = len (sys.argv[1]);
    string_array = list (sorted(sys.argv[1]));

    anagram (string_array);

if __name__ == "__main__":
    main()
