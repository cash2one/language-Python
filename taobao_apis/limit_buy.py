#!/usr/bin/env python
# coding: utf-8

import top.api
import sys, logging
import MySQLdb

def buildSQL(quantity, sku_id, type = 4):
	return 'UPDATE limited_buy SET rest=' + str(quantity) + ' WHERE num_iid=' + str(sku_id) + ' AND type=' + str(type)

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	appkey = '23042241'
	appsecret = '9949111fbfc91f1ad8587c24e81ac26f'
	sessionkey = '6102509a0c354d6b71aa7f0ce739f31499dac85d5f229ef2258287667'

	# 日志配置，打印和写文件
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s', filename='limit_buy.py.log', filemode='a')
	#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	# 请求方法，只需配置一次
	#req = top.api.ItemSkuGetRequest(domain='gw.api.taobao.com', port=80)
	req = top.api.ItemSkuGetRequest(domain='140.205.164.88', port=80)
	req.set_app_info(top.appinfo(appkey, appsecret))
	req.fields = "quantity"

	try:
		db = MySQLdb.connect(host='172.26.153.45', user='root', passwd='root', db='cbbweb', port=3306)
		cursor = db.cursor()

		# 天籁
		req.sku_id = 3121209488643
		req.num_iid = 524423079444
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591577
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

		# 轩逸
		req.sku_id = 3121127789951
		req.num_iid = 524454641641
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591578
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

		# 奇骏
		req.sku_id = 3121064354657
		req.num_iid = 524423851393
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591579
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

		# 逍客
		req.sku_id = 3121065554381
		req.num_iid = 524423831635
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591580
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

		# 骊威
		req.sku_id = 3121066142384
		req.num_iid = 524455417244
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591581
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

		# 骐达
		req.sku_id = 3120983791763
		req.num_iid = 524424023626
		resp1 = req.getResponse(sessionkey)
		req.sku_id = 3120780591582
		req.num_iid = 524434420577
		resp2 = req.getResponse(sessionkey)
		resp = resp1['item_sku_get_response']['sku']['quantity'] + resp2['item_sku_get_response']['sku']['quantity']
		cursor.execute(buildSQL(resp, req.sku_id))
		logging.info('num_iid: ' + str(req.num_iid) + ', sku_id: ' + str(req.sku_id) + ', quantity: ' + str(resp))

	except Exception, e:
		logging.error(e)
		raise e
