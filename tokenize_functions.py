# -*- coding: UTF-8 -*-

import spacy
from tokenizer import split_into_sentences

sp = spacy.load('en_core_web_sm')


def tokenize_en_line(curr_line):
    line = sp(curr_line)
    tokenized_line = ''
    for sentence in line.sents:
        for word in sentence:
            tokenized_line += str(word) + ' '
    return tokenized_line


def tokenize_is_line(curr_line):
    g = split_into_sentences(curr_line)
    tokenized_line = ''
    for sentence in g:
        tokens = sentence.split()
        curr_sentence = ' '.join(tokens)
        tokenized_line += curr_sentence + ' '
    tokenized_line = ' '.join(tokenized_line.split())
    return tokenized_line
