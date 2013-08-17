#coding=utf-8

#!/bin/env python

import time, urllib, lxml.html, json, os, sys, sqlite3

def InitDatabase(user):
	return 'CREATE TABLE IF NOT EXISTS ht_' + user + ''' (
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

def InsertDatabase(dictParam):
	serial = ['id','nickName','url','sex','avatar','age','following','followed','height','education','salary','province','city','school','company','isCheckCorp','isCheckSchool','isCheckSalary','isOnline','isAvatarAudit','photoCount']
	cols = ''
	for col in serial:
		if col == 'id': col = 'uid'
		cols += col + ','
	sql = 'INSERT INTO ht_' + str(dictParam['url']) + '(' + cols[:-1] + ') VALUES ('
	for item in serial: sql += '\'' + str(dictParam[item]) + '\','
	return sql[:-1] + ');'

def GetUserData(user):
	url = 'http://love.163.com/' + user
	dom = urllib.urlopen(url).read()
	tree = lxml.html.fromstring(dom)
	tre = tree.xpath("//script[@id='data_userProfile']")
	return json.loads(tre[0].text)

def GetCurrent():
	return time.strftime('%x %X', time.localtime())

def ShowOnlineStatus(opt):
	if opt == '0': return 'Offline'
	elif opt == '1': return 'Online (web browser)'
	elif opt == '2': return 'Online (Android)'
	elif opt == '3': return 'Online (iPhone)'
	else: return 'Online (' + opt + ')'

# add id:name below
userlist = {'': ''}
dbfile = 'users.db'
conn = None

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	conn = sqlite3.connect(dbfile)
	conn.isolation_level = None     # save on changes
	online_status = ['0'] * len(userlist)

	while True:
		try:
			for index in range(len(userlist)):
				cur = GetCurrent() + ' |'
				conn.execute(InitDatabase(userlist.keys()[index]))
				jsons = GetUserData(userlist.keys()[index])
				print cur, userlist.keys()[index], userlist.values()[index]
				if jsons['isOnline'] != online_status[index]:
					online_status[index] = jsons['isOnline']
					print ' ' * len(cur), 'new online status:', online_status[index], ':', ShowOnlineStatus(online_status[index])
					conn.execute(InsertDatabase(jsons))
					conn.commit()
			time.sleep(30)
		except (KeyboardInterrupt), e:
			print 'admin canelled, saving...'
			break
		except Exception, e:
			print e

	conn.commit()
	conn.close()

