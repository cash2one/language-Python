#!/usr/bin/env python
# coding: utf-8

import top.api
import sys, logging, urllib2, urllib, json

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	appkey = ''
	appsecret = ''
	sessionkey = ''

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s: %(message)s', filename='lannia2.py.csv', filemode='a')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	req = top.api.TradesSoldGetRequest(domain='gw.api.taobao.com', port=80)
	req.set_app_info(top.appinfo(appkey, appsecret))

	page_no = 1
	while True:
		try:
			req.fields = 'tid,buyer_nick,payment,status,receiver_name,receiver_address,receiver_mobile,receiver_phone,num_iid,receiver_state,receiver_city,receiver_district'
			req.type = 'fixed'
			req.page_size = 40
			req.use_has_next = 'true'
			req.start_created = '2015-10-20 18:00:00'
			req.end_created = '2015-11-01 00:00:00'
			req.page_no = page_no

			resp = req.getResponse(sessionkey)
			trades = resp['trades_sold_get_response']['trades']['trade']

			for trade in trades:
				if not trade.has_key('receiver_name') or not trade['receiver_name']: trade['receiver_name'] = ''
				if not trade.has_key('receiver_state') or not trade['receiver_state']: trade['receiver_state'] = ''
				if not trade.has_key('receiver_city') or not trade['receiver_city']: trade['receiver_city'] = ''
				if not trade.has_key('receiver_district') or not trade['receiver_district']: trade['receiver_district'] = ''
				if not trade.has_key('receiver_address') or not trade['receiver_address']: trade['receiver_address']  = ''
				if not trade.has_key('receiver_phone') or not trade['receiver_phone']: trade['receiver_phone'] = ''
				if not trade.has_key('receiver_mobile') or not trade['receiver_mobile']: trade['receiver_mobile'] = ''

				if not trade['status'] or trade['status'] not in ('WAIT_BUYER_CONFIRM_GOODS', 'TRADE_FINISHED'): continue
				if not trade['payment'] or trade['payment'] != '1.00': continue

				logging.info(str(trade['tid']) + ',' + trade['buyer_nick'] + ',' + trade['payment'] + ',' + trade['status'] + ',' + trade['receiver_name'] + ',' + trade['receiver_state'] + ',' + trade['receiver_city'] + ',' + trade['receiver_district'] + ',' + trade['receiver_address'] + ',' + trade['receiver_mobile'] + ',' + trade['receiver_phone'])

			if not resp['trades_sold_get_response']['has_next']: break
			page_no += 1

		except Exception, e:
			raise e
			continue
