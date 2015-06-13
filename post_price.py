#coding=utf-8

import urllib2
import urllib
from simplemysql import SimpleMysql

def u(s, encoding):
	if isinstance(s, unicode): return s
	return unicode(s, encoding)

def post(data):
	f = urllib2.urlopen(
		'http://erp.pp.cn:88/api/price',
		urllib.urlencode(data)
	)
	return f.read()

if __name__ == '__main__':
	import sys
	reload(sys)
	sys.setdefaultencoding('utf-8')
	conn = SimpleMysql(host="127.0.0.1", db='locoyspider', user='root', passwd='root')
	results = conn.getAll("data_content_153", ['dealer', 'dealerid', 'modelid', 'model', 'price', 'oprice'])

	a = open('r.txt', 'w')
	for result in results:
		data = {}
		data['dealer'] = result[0].encode('utf-8')
		data['dealerid'] = result[1].encode('utf-8')
		data['modelid'] = result[2].encode('utf-8')
		data['model'] = result[3].encode('utf-8')
		data['price'] = result[4].encode('utf-8')
		data['oprice'] = result[5].encode('utf-8')
		r = post(data)
		print r
		a.write(r + '\n')
	a.close()