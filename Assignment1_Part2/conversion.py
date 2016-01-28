#!/usr/bin/python -tt

import sys
import binascii


def final_result (number, num_bits, f_write, bin_string):
    if num_bits == 1:
        final_string = "0"
        for i in range (1, 8):
            final_string += bin_string[i]
        #print final_string

    elif num_bits == 2:
        final_string = "110"
        for i in range (5, 10):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (10, 16):
            final_string += bin_string[i]

    elif num_bits == 3:
        final_string = "1110"
        for i in range (8, 12):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (12, 18):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (18, 24):
            final_string += bin_string[i]

    elif num_bits == 4:
        final_string = "11110"
        for i in range (11, 14):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (14, 20):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (20, 26):
            final_string += bin_string[i]
        final_string += "10"
        for i in range (26, 32):
            final_string += bin_string[i]

    n = int (final_string, 2)
    print final_string, n, num_bits
    if (n != 12 and n != 10):
        print binascii.unhexlify('%x' % n)
        f_write.write(binascii.unhexlify('%x' % n))
    else:
        f_write.write(' ')



def construct_binary (number, num_bits, f_write):
    #print number
    number_str = ""
    number_str += str(number)
    bin_string = bin(int(number_str, 10))[2:].zfill(num_bits*8)
    final_result (number, num_bits, f_write, bin_string)
    #print number, bin_string


def compare_and_convert (number, f_write):
    number = int(number, 16)
    print number
    if number > 0 and number <= 127:
        construct_binary (number, 1, f_write)
    elif number > 127 and number <= 2047:
        construct_binary (number, 2, f_write)
    elif number > 2047 and number <= 65535:
        construct_binary (number, 3, f_write)
    elif number > 65535:
        construct_binary (number, 4, f_write)


def read_a_file(file_name):
    fd = open(file_name, "rb")
    f_write = open('sample_output.txt', 'w')
    buffer = ""
    try:
        bytes_read = fd.read(1)
        while bytes_read != "":
            pre_bit1 = 0
            pre_bit2 = 0
            final_num = ""

            pre_bit1 = ord(bytes_read)

            bytes_read = fd.read(1)
            if bytes_read != "":
                pre_bit2 = ord(bytes_read)
            else:
                break

            if pre_bit1 != 0:
                final_num += hex(pre_bit1)[2:]
            final_num += hex(pre_bit2)[2:]
            print "Pre1 : ", pre_bit1, "Pre2 : ", pre_bit2, "Final :", final_num
            compare_and_convert (final_num, f_write)
            bytes_read = fd.read(1)
    finally:
        f_write.write('\n')
        f_write.write('\n')
        fd.close()
        f_write.close()

def main():
    if len(sys.argv) != 2:
        print "Syntax : ./conversion <file_name>"
        exit()

    read_a_file (sys.argv[1])

if __name__ == "__main__":
    main()
