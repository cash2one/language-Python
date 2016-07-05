#!/usr/bin/env python
# coding: utf-8

'''
1. sql文件最后不要用Limit关键词
2. sql文件最后不要加分号结尾
3. sql目录中存放sql文件，文件名对应本地数据库中的表名
'''

import cx_Oracle, simplemysql
import os, sys, logging

class SyncTask:
	def load_sql(self):
		sql_files = []
		list_dirs = os.walk(os.getcwd() + '\sql')
		for root, dirs, files in list_dirs:
			for f in files:
				if os.path.splitext(f)[1] == '.sql': sql_files.append(os.path.join(root, f))
		return sql_files

	def sql(self, path):
		f = open(path, 'r')
		r = f.read()
		f.close()
		return r

	def sync_data(self, sdb, tdb, sql):
		target_table = os.path.splitext(sql)[0]
		i = 0
		step = 50
		rows = True
		sql = self.sql(sql)
		while rows:
			rows = sdb.execute(sql + ' LIMIT %d, %d' % (i, step)).fetchall()
			i += step
			for row in rows:
				tdb.insert(table=target_table, data=row, key=None)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')#, filename='sync.py.log', filemode='a')

	db1 = None
	db2 = None
	# Oracle查询出来是乱码 # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
	os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

	try:
		db1 = cx_Oracle.connect('sjglb1', 'jsglb1!!1921%', 'TC0010', '1521', 'sjglb').cursor()
		db2 = simplemysql.SimpleMysql(host='172.26.146.42', db='dndcdata', 'zhouqr', passwd='mm123456')

		s = SyncTask()
		sql_files = s.load_sql()
		for sql_file in sql_files:
			s.sync_data(db1, db2, sql_file)

	except Exception, e:
		logging.error(e)

	finally:
		if db1: db1.close()

	raw_input(unicode('Press Enter to quit...', 'UTF-8').decode('GBK'))
