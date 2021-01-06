import sqlite3
import argparse
import csv
from os import path
from utilities import tokenize_functions

parser = argparse.ArgumentParser()
parser.add_argument('--input-file', '-i', help="File with aligned sentences")
parser.add_argument('--tokenize', '-t', action='store_true', help="Tokenize (Icelandic and English)")
parser.add_argument('--db-name', help="DB name", default='alignments.db')
args = parser.parse_args()

if path.exists(args.db_name):
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()
else:
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()
    c.execute('''CREATE TABLE ALIGNMENTS ([id] INTEGER PRIMARY KEY,[src_sentence] text, [trg_sentence] text, [alignments_u1] text, [alignments_u2] text, [confidence] text, [source_filename] text, [done1] boolean, [done2] boolean, [discard] boolean)''')
    conn.commit()


with open(args.input_file, newline='') as alignments:
    read_alignments = csv.reader(alignments, delimiter='\t')
    for alignment in read_alignments:
        src_alignment = alignment[0].strip().rstrip()
        trg_alignment = alignment[1].strip().rstrip()
        if args.tokenize:
            src_alignment = tokenize_functions.tokenize_en_line(src_alignment).replace("'", "''")
            trg_alignment = tokenize_functions.tokenize_is_line(trg_alignment).replace("'", "''")
        else:
            src_alignment = src_alignment.replace("'", "''")
            trg_alignment = trg_alignment.replace("'", "''")
        print(alignment[0], alignment[1])
        c.execute("select count() from alignments where src_sentence = '{}' and trg_sentence = '{}' and source_filename = '{}'".format(src_alignment, trg_alignment, args.input_file))
        if c.fetchone()[0] == 0:
            c.execute("INSERT INTO ALIGNMENTS (trg_sentence, src_sentence, source_filename, done1, done2) VALUES ('{}', '{}', '{}', {}, {})".format(src_alignment, trg_alignment, args.input_file, 0, 0))
    conn.commit()
