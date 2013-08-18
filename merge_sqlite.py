#coding=utf-8

#!/bin/env python

import time, urllib, lxml.html, json, sys, sqlite3, os

def InitDatabase(user):
	return 'CREATE TABLE IF NOT EXISTS ht_' + str(user) + ''' (
		ID INTEGER PRIMARY KEY AUTOINCREMENT,
		UID TEXT NOT NULL,
		NICKNAME TEXT NOT NULL,
		URL TEXT NOT NULL,
		SEX TEXT NOT NULL,
		AVATAR TEXT NOT NULL,
		AGE TEXT NOT NULL,
		FOLLOWING TEXT NOT NULL,
		FOLLOWED TEXT NOT NULL,
		HEIGHT TEXT NULL,
		EDUCATION TEXT NULL,
		SALARY TEXT NULL,
		PROVINCE TEXT NULL,
		CITY TEXT NULL,
		SCHOOL TEXT NULL,
		COMPANY TEXT NULL,
		ISCHECKCORP TEXT NOT NULL,
		ISCHECKSCHOOL TEXT NOT NULL,
		ISCHECKSALARY TEXT NOT NULL,
		ISONLINE TEXT NOT NULL,
		ISAVATARAUDIT TEXT NOT NULL,
		PHOTOCOUNT TEXT NOT NULL,
		RECORDTIME TIMESTAMP DEFAULT(DATETIME('NOW', 'LOCALTIME')) NOT NULL);'''

def InsertDatabase(dictParam, userid):
	cols = ('UID', 'NICKNAME', 'URL', 'SEX', 'AVATAR', 'AGE', 'FOLLOWING', 'FOLLOWED', 'HEIGHT', 'EDUCATION', 'SALARY', 'PROVINCE', 'CITY', 'SCHOOL', 'COMPANY', 'ISCHECKCORP', 'ISCHECKSCHOOL', 'ISCHECKSALARY', 'ISONLINE', 'ISAVATARAUDIT', 'PHOTOCOUNT', 'RECORDTIME')
	return 'INSERT INTO ht_' + str(userid) + str(cols) + 'VALUES' + str(dictParam[1:]).replace("u'", "'") + ';'

def LoadRecords(dbfile, userid):
	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None
	cur = conn.cursor()
	sql = 'select * from ht_' + str(userid) + ';'
	cur.execute(sql)
	res = cur.fetchall()
	conn.close()
	return res

def show_progress(num = 1, nums = 100, bar_word = '.'):
	rate = float(num) / float(nums)
	rate_num = int(rate * 100)
	print '\r%d%% :' % rate_num,
	for i in range(num):
		os.write(1, bar_word)
	sys.stdout.flush()

def get_terminal_size():
	return os.popen('stty size', 'r').read().split()

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	userid = 557363
	pool = []

	# list all db file under current directory
	dblist = os.listdir(os.path.abspath(os.curdir))
	for db in dblist:
		_, extension = os.path.splitext(db)
		if extension.lower() == '.db':
			res = LoadRecords(db, userid)
			pool.extend(res)

	# remove repeat contents
	result = list(set(pool))
	count = len(result)

	conn = sqlite3.connect('lala.sqlite3')
	conn.isolation_level = None
	conn.execute(InitDatabase(userid))
	index = 0
	width = int(get_terminal_size()[1]) - 5

	for item in result:
		conn.execute(InsertDatabase(item, userid))
		show_progress(index * width / count, width)
		index += 1

	conn.close()
	print 'done.'
