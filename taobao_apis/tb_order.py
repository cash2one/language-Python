#!/usr/bin/env python
# coding: utf-8

import top.api
import sys, logging, urllib2, urllib, json

def post(data):
	d = {}
	d['tid'] = data['tid']
	d['num_iid'] = data['num_iid']
	d['receiver_mobile'] = data['receiver_mobile']
	d['receiver_address'] = data['receiver_address']
	d['receiver_name'] = data['receiver_name']
	d['status'] = data['status']
	d['type'] = data['type']
	d['payment'] = round(float(data['payment']), 2)
	d['order_info'] = json.dumps(data, ensure_ascii=False)
	request = urllib2.Request('http://api.chebaba.com/TbOrder.do?action=Add', urllib.urlencode(d))
	return urllib2.urlopen(request).read()

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	appkey = '23042241'
	appsecret = '9949111fbfc91f1ad8587c24e81ac26f'
	sessionkey = '6102509a0c354d6b71aa7f0ce739f31499dac85d5f229ef2258287667'

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s: %(message)s', filename='tb_order.py.log', filemode='a')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	req = top.api.TradesSoldGetRequest(domain='gw.api.taobao.com', port=80)
	req.set_app_info(top.appinfo(appkey, appsecret))
	req.fields = 'buyer_nick,created,tid,status,payment,pay_time,end_time,modified,num_iid,num,price,type,receiver_name,receiver_state,receiver_city,receiver_district,receiver_address,receiver_mobile,receiver_phone'
	req.type = 'fixed'
	req.page_size = 40
	req.use_has_next = 'true'
        req.start_created = '2015-11-01 00:00:00'
        req.end_created = '2015-11-11 23:59:59'

	page_no = 1
	while True:
		try:
			req.page_no = page_no
			resp = req.getResponse(sessionkey)
			trades = resp['trades_sold_get_response']['trades']['trade']
			for trade in trades:
				logging.info('[P' + str(page_no) + '] ' + str(trade['tid']) + ':' + int(json.loads(post(trade))['retnCode'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m')
			if not resp['trades_sold_get_response']['has_next']: break
			page_no += 1

		except Exception, e:
			logging.error(e)
			continue
			# raise e
