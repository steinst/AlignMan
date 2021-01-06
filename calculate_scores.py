import sqlite3
import argparse
import csv
import sys
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('--manual-alignments', '-m', help="File containing manual alignments")
parser.add_argument('--automatic-alignments', '-a', help="File containing automatic alignments")
parser.add_argument('--alignment-format', '-f', default='pharaoh', choices=['classic', 'pharaoh'])
parser.add_argument('--test-type', '-t', default='prf', choices=['precision', 'recall', 'f-score', 'prf', 'aer'])
parser.add_argument('--results', '-r', default='total', choices=['individual', 'total', 'both']) # not implemented
parser.add_argument('--confidence-type', '-c', default='all', choices=['sure', 'probable', 'all'])
args = parser.parse_args()

manFile = open(args.manual_alignments, 'r')
manLines = manFile.readlines()
manFile.close()

autoFile = open(args.automatic_alignments, 'r')
autoLines = autoFile.readlines()
autoFile.close()

autoDict = {}


def precision(auto, gold):
    return len(set.intersection(set(auto), set(gold))) / len(auto)


def recall(auto, gold):
    return len(set.intersection(set(auto), set(gold))) / len(gold)


def fscore(precision, recall):
    if (precision + recall) > 0:
        return (2*precision*recall) / (precision + recall)
    else:
        return 0


def measure(id, gold, test, confidence):
    global autoDict
    #confidence not implemented
    auto = autoDict[id]
    if test == 'precision':
        try:
            return precision(auto, gold)
        except:
            return None
    elif test == 'recall':
        try:
            return recall(auto, gold)
        except:
            return None
    elif test == 'f-score':
        try:
            p = precision(auto, gold)
            r = recall(auto, gold)
            return fscore(p,r)
        except:
            return None
    elif test == 'prf':
        try:
            p = precision(auto, gold)
            r = recall(auto, gold)
            return p, r, fscore(p, r)
        except:
            return None
    else:
        return None

if args.alignment_format == 'pharaoh':
    sum = 0
    count = 0
    p_sum = 0
    r_sum = 0
    f_sum = 0
    p_count = 0
    r_count = 0
    f_count = 0

    for i in autoLines:
        temp = i.split('\t')
        autoDict[temp[0]] = temp[1].strip().split()

    for i in manLines:
        temp = i.split('\t')
        sentID = temp[0]
        alignments = temp[1].strip().split()

        if args.test_type == 'prf':
            line_p, line_r, line_f = measure(sentID, alignments, args.test_type, args.confidence_type)
            if line_p is not None:
                p_sum += line_p
                p_count += 1
            if line_r is not None:
                r_sum += line_r
                r_count += 1
            if line_f is not None:
                f_sum += line_f
                f_count += 1
        else:
            line_score = measure(sentID, alignments, args.test_type, args.confidence_type)
            if line_score is not None:
                sum += line_score
                count += 1

    if args.test_type == 'prf':
        print('P: ' + str(p_sum/p_count) + ' average precision in ' + str(p_count) + ' lines')
        print('R: ' + str(r_sum/r_count) + ' average recall in ' + str(r_count) + ' lines')
        print('F: ' + str(f_sum/f_count) + ' average f-score in ' + str(p_count) + ' lines')
    else:
        print('Results: ' + str(sum/count) + ' average ' + args.test_type + ' in ' + str(count) + ' lines')

elif args.alignment_format == 'classic':
    print('not implemented yet!')
    sys.exit(0)
