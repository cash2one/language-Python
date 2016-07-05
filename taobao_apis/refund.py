#!/usr/bin/env python
# coding: utf-8

#
#
# 批量退款会触发批量短信验证，所以无法通过程序自动完成
#
#

#import top.api
import sys, time, logging, json

top.setDefaultAppInfo('23042241', 'c879c598abce8f412a77b03ffb046e83')
SESSION_CODE = '6101b188b6d254f60ba3edb43a1dfeac4cc58c261c22c442691740505'
TAOBAO_API_SERVER_ADDR = 'gw.api.taobao.com'
TAOBAO_API_SERVER_PORT = 80

def reject(order):
	if not order: return None
	req_refund_rej = top.api.RefundRefuseRequest(domain=TAOBAO_API_SERVER_ADDR, port=TAOBAO_API_SERVER_PORT)
	req_refund_rej.oid = order['oid']
	req_refund_rej.refund_id = order['refund_id']
	req_refund_rej.refund_phase = 'onsale'
	req_refund_rej.refund_version = order['refund_version']
	req_refund_rej.refuse_message = u'非常感谢您对东风日产的关注和支持，订单是已按约定时间发货的，有任何疑问详情请咨询在线客服为您核实解答，若执意退款，请修改退款原因。谢谢！'
	req_refund_rej.refuse_proof = open('1.png', 'r').read()
	req_refund_rej.refuse_reason_id = None
	req_refund_rej.tid = order['tid']

        try:
	        resp_refund_rej = req_refund_rej.getResponse(SESSION_CODE)['refund_refuse_response']
	        if resp_refund_rej.has_key('is_success') and resp_refund_rej['is_success']:
                        return '[已拒绝] buyer_nick: %s, order_status: %s, status: %s, tid: %d, refund_fee: %s, reason: %s' % (order['buyer_nick'], order['order_status'], order['status'], order['tid'], order['refund_fee'], order['reason'])
        except Exception, e:
                return order, e
                        
def accept(order):
	if not order: return None
	req_refund_acp = top.api.RpRefundsAgreeRequest(domain=TAOBAO_API_SERVER_ADDR, port=TAOBAO_API_SERVER_PORT)
	req_refund_acp.code = None
	req_refund_acp.refund_infos = '%d|%d|%d|%s' % (order['refund_id'], float(order['refund_fee']) * 100, order['refund_version'], 'onsale')

        try:
	        resp_refund_acp = req_refund_acp.getResponse(SESSION_CODE)['rp_refunds_agree_response']
	        if resp_refund_acp.has_key('succ') and resp_refund_acp['succ']:
		        return '[已退款] buyer_nick: %s, order_status: %s, status: %s, tid: %d, refund_fee: %s, reason: %s' % (order['buyer_nick'], order['order_status'], order['status'], order['tid'], order['refund_fee'], order['reason'])
        except Exception, e:
                return order, e

                        
if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')
	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(levelname)s: %(message)s', filename='refund.py.log', filemode='a')

	tmp = time.time()
	page_no = 1
	while True:
		req_refund_get = top.api.RefundsReceiveGetRequest(domain=TAOBAO_API_SERVER_ADDR, port=TAOBAO_API_SERVER_PORT)
		req_refund_get.fields = 'refund_id,tid,order_status,status,oid,refund_fee,created,buyer_nick,modified,reason,refund_version'
		req_refund_get.start_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp - 24*60*60))
		req_refund_get.end_modified = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp))
		req_refund_get.page_no = page_no
		req_refund_get.page_size = 40
		req_refund_get.status = 'WAIT_SELLER_AGREE'
                req_refund_get.type = 'fixed'
		req_refund_get.use_has_next = 'true'

		try:
			resp_refund_get = req_refund_get.getResponse(SESSION_CODE)['refunds_receive_get_response']
			orders = resp_refund_get.has_key('refunds') and resp_refund_get['refunds']['refund'] or None
			if not orders:
				logging.info('这个时间段内没有查询到需要退款的订单')
				break
			for order in orders:
                                print json.dumps(order, ensure_ascii=False)
                                logging.info(json.dumps(order, ensure_ascii=False))
				if float(order['refund_fee']) >= 100 or order['reason'] == u'未按约定时间发货':
					tmp = reject(order)
				else:
					tmp = accept(order)
                        print u'结果：', tmp
                        logging.info(tmp)
			if resp_refund_get['has_next']: page_no += 1
			else: break
		except Exception, e:
                        print e
			logging.error(e)
