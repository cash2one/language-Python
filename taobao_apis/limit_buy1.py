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
		# 蓝鸟库存
		req.sku_id = 3113410916556
		req.num_iid = 522965142555
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Lannia: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 天籁库存
		req.sku_id = 3113278858535
		req.num_iid = 522957698903
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Teana: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 逍客库存
		req.sku_id = 3113367696764
		req.num_iid = 522963240701
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Qashqai: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 骐达库存
		req.sku_id = 3113273862261
		req.num_iid = 522959177286
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Tiida: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 阳光库存
		req.sku_id = 3113363992010
		req.num_iid = 522936603039
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Sunny: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 玛驰库存
		req.sku_id = 3113313245048
		req.num_iid = 522936239979
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('March: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 奇骏库存
		req.sku_id = 3113314093087
		req.num_iid = 522963260533
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('X-Trail: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 轩逸库存
		req.sku_id = 3113206831249
		req.num_iid = 522962200327
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Sylphy: ' + str(resp['item_sku_get_response']['sku']['quantity']))

		# 轩逸经典库存
		req.sku_id = 3113272618405
		req.num_iid = 522935855736
		resp = req.getResponse(sessionkey)
		cursor.execute(buildSQL(resp['item_sku_get_response']['sku']['quantity'], req.num_iid))
		logging.info('Sylphy-Classic: ' + str(resp['item_sku_get_response']['sku']['quantity']))

	except Exception, e:
		# logging.error(e)
		raise e
