#!/usr/bin/python

def prtMax(x, y):
	if int (x) > int (y):
		print x
	elif int (x) == int (y):
		print x, '=', y
	else:
		print y

prtMax(232, 235)

