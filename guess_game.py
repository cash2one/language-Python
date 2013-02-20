#!/usr/bin/python

num = 52
running = True

while running:
	guess = int (raw_input('Enter an int: '))

	if guess == num:
		print 'cong!'
		running = False
	elif guess < num:
		print 'a little smaller'
	else:
		print 'a little bigger'

