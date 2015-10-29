#!/usr/bin/env python
# coding: utf-8

import top.api
import sys, logging
import MySQLdb

def buildSQL(quantity, num_iid, type=2):
	return 'UPDATE limited_buy SET rest=' + str(quantity) + ' WHERE num_iid=' + str(num_iid) + ' AND type=' + str(type)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	appkey = ''
	appsecret = ''
	sessionkey = ''

	# 日志配置，打印和写文件
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s', filename='limit_buy.py.log', filemode='w')
	#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	# 请求方法，只需配置一次
	req = top.api.ItemSkuGetRequest(domain='gw.api.taobao.com', port=80)
	req.set_app_info(top.appinfo(appkey, appsecret))
	req.fields = "quantity"

	db = MySQLdb.connect('172.26.152.176', 'root', 'root', 'cbbweb')
	cursor = db.cursor()

	try:
		req.sku_id = 
		req.num_iid = 
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('xxx: ' + str(resp['item_sku_get_response']['sku']['quantity']))

	except Exception, e:
		# logging.error(e)
		raise e
