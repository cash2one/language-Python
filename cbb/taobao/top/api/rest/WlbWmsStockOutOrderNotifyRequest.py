'''
Created by auto_sdk on 2015.09.16
'''
from top.api.base import RestApi
class WlbWmsStockOutOrderNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.car_no = None
		self.carriers_name = None
		self.extend_fields = None
		self.order_code = None
		self.order_create_time = None
		self.order_item_list = None
		self.order_type = None
		self.outbound_type_desc = None
		self.pick_call = None
		self.pick_id = None
		self.pick_name = None
		self.prev_order_code = None
		self.receiver_info = None
		self.remark = None
		self.send_time = None
		self.sender_info = None
		self.store_code = None
		self.transport_mode = None

	def getapiname(self):
		return 'taobao.wlb.wms.stock.out.order.notify'
