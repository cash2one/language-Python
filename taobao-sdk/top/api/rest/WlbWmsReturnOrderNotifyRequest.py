'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsReturnOrderNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.buyer_nick = None
		self.extend_fields = None
		self.order_code = None
		self.order_create_time = None
		self.order_flag = None
		self.order_item_list = None
		self.order_source = None
		self.order_type = None
		self.owner_user_id = None
		self.prev_order_code = None
		self.receiver_info = None
		self.remark = None
		self.return_reason = None
		self.sender_info = None
		self.store_code = None
		self.tms_order_code = None
		self.tms_service_code = None
		self.tms_service_name = None

	def getapiname(self):
		return 'taobao.wlb.wms.return.order.notify'
