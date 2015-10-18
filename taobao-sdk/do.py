#!/usr/bin/env python
# coding: utf-8

import top.api
import logging

appkey = ''
appsecret = ''
sessionkey = ''
refresh_token = ''

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s')

	req_order = top.api.TradesSoldGetRequest(domain='gw.api.taobao.com', port=80)
	req_order.set_app_info(top.appinfo(appkey, appsecret))

	req_logis = top.api.LogisticsDummySendRequest(domain='gw.api.taobao.com', port=80)
	req_logis.set_app_info(top.appinfo(appkey, appsecret))

	page_no = 1

	while True:
		req_order.fields = 'tid,num_iid,payment'
		req_order.type = 'fixed'
		req_order.start_created = '2015-10-01'
		req_order.end_created = '2015-10-30'
		req_order.page_no = page_no
		req_order.page_size = 40
		req_order.status = 'WAIT_SELLER_SEND_GOODS'
		req_order.use_has_next = 'true'

		try:
			resp_order = req_order.getResponse(sessionkey)

			orders = resp_order['trades_sold_get_response']['trades']['trade']
			logging.info("\nWe've got " + str(len(orders)) + " orders:")
			for order in orders:
				req_logis.tid = order['tid']
				resp_logis = req_logis.getResponse(sessionkey)
				temp_result = resp_logis['logistics_dummy_send_response']['shipping']['is_success']
				logging.info(str(order['tid']) + ' has been delivered: ' + (temp_result==True and '\033[32m成功\033[0m' or '\033[31m失败\033[0m'))

			if resp_order['trades_sold_get_response']['has_next']:
				page_no += 1
				continue
			else:
				logging.info('The goods during your sepecified period of date have been delivered.')
				break
		except Exception, e:
			logging.error(e)
			continue
