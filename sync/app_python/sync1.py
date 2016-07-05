#!/usr/bin/env python
# coding: utf-8

#import cx_Oracle, simplemysql
import os, sys, logging, json

CONFIG_FILE = 'sync.json'

class Config:
	def __init__(self, path):
                self.path = path

        def load(self):
		try:
			return json.loads(open(self.path).read())
		except Exception, e:
			logging.error(e)
			return None

class SyncTask:
        def __init__(self, db1, db2):
                self.db1 = db1
                self.db2 = db2

        def load_tables(self):
                try:
                        return Config(CONFIG_FILE).load()['tables']
                except Exception, e:
                        logging.error(e)
                        return None

        def init_table(self, table):
                sql = '''
                SELECT %s FROM all_tables
                WHERE nvl(tablespace_name, 'no tablespace') NOT IN ('SYSTEM', 'SYSAUX')
                AND OWNER = :owner
                AND IOT_NAME IS NULL
                '''
                sql = sql % table
        
        def start_sync(self, table):
                pass
                
if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')#, filename='sync.py.log', filemode='a')

	cfg = Config(CONFIG_FILE).load()
        if not cfg:
                logging.error('config load failed')
                exit()

	db1 = None
	db2 = None
	# Oracle查询出来是乱码 # UnicodeEncodeError: 'ascii' codec can't encode characters in position 1-7: ordinal not in range(128)
	os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

	try:
		db1 = 1#cx_Oracle.connect('sjglb1', 'jsglb1!!1921%', '172.26.146.42', '1521', 'sjglb').cursor() # TC0100
		db2 = 2#simplemysql.SimpleMysql(host='172.26.146.42', db='dndcdata', user='zhouqr', passwd='mm123456')

		s = SyncTask()
                while table in s.load_tables():
                        s.init_table(table)
                        s.start_sync(table)

                logging.info('All tables were synced successfully.')

	except Exception, e:
		logging.error(e)

	finally:
		pass#if db1: db1.close()

	raw_input(unicode('Press Enter to quit...', 'UTF-8').decode('GBK'))
