#!/usr/bin/python3.4 -tt

import sys

global output
output = []

def anagram (string_array, fd):
    if [] == string_array or string_array == None:
        return

    if 1 == len(string_array):
        output.append (string_array[0])
        fd.write (''.join(output))
        fd.write ("\n")
        output.pop()
        return

    for index in range (0, len(string_array)):
        output.append (string_array[index])
        temp = string_array[:index] + string_array[index+1:]
        anagram (temp, fd)
        output.pop()


def main():
    if len(sys.argv) != 2:
        print ("Syntax : ./anagram.py <string1>")
        exit()

    fd = open ("anagram_out.txt", "w");
    string_length = len (sys.argv[1]);
    string_array = list (sorted(sys.argv[1]));

    anagram (string_array, fd);

if __name__ == "__main__":
    main()
