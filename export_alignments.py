import sqlite3
import argparse
import sys
from os import path

parser = argparse.ArgumentParser()
parser.add_argument('--sentences', '-s', help="Output sentences", action='store_true')
parser.add_argument('--sentence-number', '-sn', default='0', help="Output sentences by id-s [example: 1 or 1-3 or 1-3,7-9]. Default is all sentences.")
parser.add_argument('--sentence-format', '-sf', default='text', choices=['markup', 'text', 'fa'])
parser.add_argument('--alignments', '-a', help="Output alignments", action='store_true')
parser.add_argument('--alignment-number', '-an', default='0', help="Output alignments by id-s [example: 1 or 1-3 or 1-3,7-9]. Default is all sentences.")
parser.add_argument('--alignment-format', '-af', default='classic', choices=['classic', 'pharaoh'])
parser.add_argument('--include-source', '-source', help="Include source?", action='store_true')
parser.add_argument('--select-alignments', '-select', help="Select which alignments", default='combined', choices=['user1', 'user2', 'combined'])
parser.add_argument('--db-name', help="DB name", default='alignments.db')
args = parser.parse_args()

if path.exists(args.db_name):
    conn = sqlite3.connect(args.db_name)
    c = conn.cursor()


def get_ids(numbers):
    selected_ids = []
    ranges = numbers.strip().split(',')
    for range in ranges:
        try:
            selected_ids.append(int(range))
        except:
            r = range.split('-')
            if len(r) == 2:
                if int(r[0]) and int(r[1]):
                    if int(r[0]) < int(r[1]):
                        for i in range(int(r[0]),int(r[0])+1):
                            selected_ids.append(i)

    if args.select_alignments == 'user1':
        sqlstring = 'select id from alignments where done1 = 1 and discard is not 1'
    elif args.select_alignments == 'user2':
        sqlstring = 'select id from alignments where done2 = 1 and discard is not 1'
    elif args.select_alignments == 'combined':
        sqlstring = 'select id from alignments where done1 = 1 and done2 = 1 and discard is not 1'
    c.execute(sqlstring)
    out_ids = []
    for row in c.fetchall():
        if (int(row[0]) in selected_ids) or numbers == '0':
            out_ids.append(int(row[0]))
    return out_ids


def return_sentences(ids, format, source):
    if args.select_alignments == 'user1':
        sqlstring = 'select id, src_sentence, trg_sentence, source_filename from alignments where done1 = 1 and discard is not 1'
    elif args.select_alignments == 'user2':
        sqlstring = 'select id, src_sentence, trg_sentence, source_filename from alignments where done2 = 1 and discard is not 1'
    elif args.select_alignments == 'combined':
        sqlstring = 'select id, src_sentence, trg_sentence, source_filename from alignments where done1 = 1 and done2 = 1 and discard is not 1'
    c.execute(sqlstring)
    src_text_out = ''
    trg_text_out = ''
    info_out = ''
    for lina in c.fetchall():
        if lina[0] in ids:
            if format == 'text':
                src_text_out += str(lina[0]) + '\t' + lina[1] + '\n'
                trg_text_out += str(lina[0]) + '\t' + lina[2] + '\n'
            elif format == 'markup':
                src_text_out += '<s snum=' + str(lina[0]) + '>' + lina[1] + '</s>\n'
                trg_text_out += '<s snum=' + str(lina[0]) + '>' + lina[2] + '</s>\n'
            elif format == 'fa':
                src_text_out += lina[1] + ' ||| ' + lina[2] + '\n'
        if source: info_out += lina[3] + '\n'
    return src_text_out, trg_text_out, info_out


def return_alignments(ids, format, source):
    if args.select_alignments == 'user1':
        sql_string = "select id, alignments_u1, source_filename from alignments where done1 = 1 and discard is not 1"
    elif args.select_alignments == 'user2':
        sql_string = "select id, alignments_u2, source_filename from alignments where done2 = 1 and discard is not 1"
    elif args.select_alignments == 'combined':
        sql_string = "select id, confidence, source_filename from alignments where done1 = 1 and done2 = 1 and discard is not 1"
    c.execute(sql_string)
    alignments_out = ''
    info_out = ''
    for lina in c.fetchall():
        if lina[0] in ids:
            print(sorted(lina[1].strip().split()))
            alignments_ordered = ' '.join(sorted(lina[1].strip().split()))
            if format=='pharaoh':
                alignments_out += str(lina[0]) + '\t' + alignments_ordered + '\n'
            elif format=='classic':
                word_alignments = alignments_ordered.split()
                for word_alignment in word_alignments:
                    current = word_alignment.split('-')
                    if str(current[1]).find(':') > -1:
                        current[1] = current[1].replace(':', ' ')
                    alignments_out += str(lina[0]) + ' ' + str(current[0]) + ' ' + str(current[1]) + '\n'
        if source: info_out += lina[2] + '\n'
    return alignments_out, info_out


if __name__ == '__main__':
    filename = args.db_name.strip('.db')
    info_out = ''
    if args.sentences:
        print_ids = get_ids(args.sentence_number)
        src_text_out, trg_text_out, info_out = return_sentences(print_ids, args.sentence_format, args.include_source)
        if args.sentence_format == 'fa':
            srcFile = open(filename + '.' + args.sentence_format, 'w')
            srcFile.write(src_text_out)
            srcFile.close()
        else:
            srcFile = open(filename + '_src_' + args.sentence_format + '.txt', 'w')
            srcFile.write(src_text_out)
            srcFile.close()
            trgFile = open(filename + '_trg_' + args.sentence_format + '.txt', 'w')
            trgFile.write(trg_text_out)
            trgFile.close()
    elif args.alignments:
        print_ids = get_ids(args.alignment_number)
        alignments_out, info_out = return_alignments(print_ids, args.alignment_format, args.include_source)
        trgFile = open(filename + '_alignments_' + args.alignment_format + '.txt', 'w')
        trgFile.write(alignments_out)
        trgFile.close()
    else:
        print("Output has to be selected, either sentences (-s) or alignments (-a)")
        sys.exit(0)
    if len(info_out) > 0:
        infoFile = open(filename + '_sources' + '.txt', 'w')
        infoFile.write(info_out)
        infoFile.close()
