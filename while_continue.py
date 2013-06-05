#!/usr/bin/python

while True:
	s = raw_input ('Enter sth: ')

	if s == 'quit':
		break

	if len(s) < 3:
		continue

	print 'the string is: ', s, 'length is: ', len(s)

