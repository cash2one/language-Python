#!/usr/bin/python

def func():
	global x

	print 'before global def x is ', x

	x = 2

	print 'defed x is ', x

x = 60
func()

print 'result x is ', x

