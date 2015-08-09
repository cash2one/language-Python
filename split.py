#-*- coding: utf-8 -*-
#/usr/bin/env python

import sys

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage:', sys.argv[0], 'filename'
		exit()
	filename = sys.argv[1]
	a = open(filename, 'r')
	b = open('result.sql', 'a')
	for line in a.readlines():
		line = line.strip()
		tmp = line.split()
		if len(tmp) < 2: continue
		tmp = "INSERT INTO userdb(email, passwd) VALUES ('"+tmp[0]+"','"+tmp[1]+"');"
		b.write(tmp + '\n')
		#print tmp
	a.close()
	b.close()
