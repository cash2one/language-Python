#!/usr/bin/env python

import random

ROW_RANGE = 300000
COL_RANGE = 20

def genInt():
	return str(random.randint(-500, 500))

def genRecord(length):
	tmp = ''
	for i in range(length):
		tmp += genInt() + ','
	return tmp[:-1]

if __name__ == '__main__':
	fd = open('result.csv', 'w')

	for i in range(ROW_RANGE):
		tmp = genRecord(20)
		fd.write(tmp + '\r\n')
		print i + 1, '/', ROW_RANGE, '\b' * 20,

	fd.close()
