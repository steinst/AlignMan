# -*- coding: UTF-8 -*-

import spacy
import os
import sys
from glob import glob
import multiprocessing

en_file = sys.argv[1]
sp = spacy.load('en_core_web_sm')

def tokenize_file(curr_file):
    txt_file = open(curr_file, 'r')
    lines = txt_file.readlines()
    print(curr_file)

    try:
        with open(curr_file + '.tokenized', 'w') as outfile:
            for l in lines:
                if len(l.strip()) == 0:
                    outfile.write('\n')
                else:
                    curr_lines = sp(l.strip())
                    for sentence in curr_lines.sents:
                        tokenized_line = ''
                        for word in sentence:
                            tokenized_line += str(word) + ' '
                        outfile.write(tokenized_line.strip() + '\n')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    tokenize_file(en_file)
