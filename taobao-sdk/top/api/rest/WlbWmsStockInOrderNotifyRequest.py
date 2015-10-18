'''
Created by auto_sdk on 2015.09.16
'''
from top.api.base import RestApi
class WlbWmsStockInOrderNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.expect_end_time = None
		self.expect_start_time = None
		self.extend_fields = None
		self.inbound_type_desc = None
		self.order_code = None
		self.order_create_time = None
		self.order_flag = None
		self.order_item_list = None
		self.order_type = None
		self.prev_order_code = None
		self.receiver_info = None
		self.remark = None
		self.return_reason = None
		self.sender_info = None
		self.store_code = None
		self.supplier_code = None
		self.supplier_name = None
		self.tms_order_code = None
		self.tms_service_code = None
		self.tms_service_name = None

	def getapiname(self):
		return 'taobao.wlb.wms.stock.in.order.notify'
