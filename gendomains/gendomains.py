#!/usr/bin/env python

LISTFILE = 'gendomains.lst'

if __name__ == '__main__':
    dct = open(LISTFILE, 'r')

#    for item in dct:
#        print item,;     # remove enter character
    al = dct.readlines()
    dct.close()

    res = open('result.txt', 'w')
    for item1 in al:
        for item2 in al:
            res.write(item1[0:len(item1)-2] + item2[0:len(item2)-2] + '.com\r\n')

    res.close()

