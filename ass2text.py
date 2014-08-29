# date: 2014-08-30
# author: doni, tom
# function: convert ass files to txt files
# usage: ass2text.py filename.ass filename.txt
#        for i in *.ass; do python ass2text.py $i ${i%.ass}.txt; done
# target: Desperate housewives Season 1 (23 episodes) from yyets.com

#!/usr/bin/env python
import codecs, re, sys

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Usage: ', sys.argv[0], '[ASS File] [TXT File]'
        exit(1)

    f = codecs.open(sys.argv[1], 'r', encoding='utf-16')
    data = []
    for line in f:
        line = re.sub(r'\{[^}]+}', '', line)
        line = re.sub(r'Di[^,]+(,[^,]*){8},', '', line)
        line = re.sub(r'<i>', '', line)
        line = re.sub(r'</i>', '', line)
        line = re.sub(r'\\N', "\n", line)
        data.append(line)
    f.close()

    #print "\n".join([ "%d. %s" % (i, l) for i, l in enumerate(data)])

    n = open(sys.argv[2], 'wb')
    for line in data:
        if line is not None:
            n.write(line.encode('utf-8') + '\n')
    n.close()

