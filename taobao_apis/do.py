#!/usr/bin/env python
# coding: utf-8

import top.api
import sys, time, logging

top.setDefaultAppInfo('23042241', 'c879c598abce8f412a77b03ffb046e83')
SESSION_CODE = '61014101196335f5551cf6e8d150c78358b8aedb3d449272258287667'

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', filename='do.py.log', filemode='a')

	req_order = top.api.TradesSoldIncrementGetRequest(domain='gw.api.taobao.com', port=80)
	req_logis = top.api.LogisticsDummySendRequest(domain='gw.api.taobao.com', port=80)

	tmp = time.time()
	page_no = 1
	while True:
		req_order.fields = 'tid,num_iid,payment,type'
		req_order.start_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp - 24*60*60))
		req_order.end_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp))
		logging.info('时间范围: ' + req_order.start_modified + ' | ' + req_order.end_modified)
		req_order.status = 'WAIT_SELLER_SEND_GOODS'
		req_order.type = 'fixed'
		req_order.page_no = page_no
		req_order.page_size = 40
		req_order.use_has_next = 'true'

		try:
			resp_order = req_order.getResponse(SESSION_CODE)['trades_sold_increment_get_response']
			orders = resp_order.has_key('trades') and resp_order['trades']['trade'] or None
			if not orders:
				logging.info('这个时间段内没有查询到一口价类型的订单')
				break
			for order in orders:
				if order['type'] == 'fixed':
					req_logis.tid = order['tid']
					resp_logis = req_logis.getResponse(SESSION_CODE)
					temp_result = resp_logis['logistics_dummy_send_response']['shipping']['is_success']
					logging.info('自动发货 tid: %s, num_iid: %s, payment: %s, type: %s, result: %s' % (str(order['tid']), str(order['num_iid']), str(order['payment']), str(order['type']), (temp_result==True and '\033[32m成功\033[0m' or '\033[31m失败\033[0m')))
				else:
					logging.error('无法发货 tid: %s, num_iid: %s, payment: %s, type: %s' % (str(order['tid']), str(order['num_iid']), str(order['payment']), str(order['type'])))
			if resp_order['has_next']: page_no += 1
			else: break
		except Exception, e:
			logging.error(e)
			break
