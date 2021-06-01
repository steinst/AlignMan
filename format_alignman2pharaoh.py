# -*- coding: UTF-8 -*-

import sys

src_file = sys.argv[1]
alignmenttype = sys.argv[2]


srcIn = open(src_file, 'r')
srcLines = srcIn.readlines()
srcIn.close()

if alignmenttype == 'pharaoh':
    with open(src_file, 'w') as of:
        for i in srcLines:
            currLine = i.replace(':P', '').replace(':S', '')
            of.write(currLine)
elif alignmenttype == 'aer':
    with open(src_file, 'w') as of:
        for i in srcLines:
            currLine = ""
            try:
                curr_alignments = i.split('\t')[1].strip()
                ca_list = curr_alignments.split()
                for ca in ca_list:
                    curr = ca.split(':')
                    if curr[1] == 'S':
                        currLine += curr[0] + ' '
                    elif curr[1] == 'P':
                        currLine += curr[0].replace('-', 'p') + ' '
            except:
                pass
            of.write(currLine.strip() + '\n')
