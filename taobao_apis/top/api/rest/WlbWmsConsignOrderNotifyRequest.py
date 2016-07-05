'''
Created by auto_sdk on 2016.04.07
'''
from top.api.base import RestApi
class WlbWmsConsignOrderNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.alipay_no = None
		self.ar_amount = None
		self.car_no = None
		self.carriers_name = None
		self.deliver_requirements = None
		self.discount_amount = None
		self.extend_fields = None
		self.got_amount = None
		self.invoice_info_list = None
		self.order_amount = None
		self.order_code = None
		self.order_create_time = None
		self.order_examination_time = None
		self.order_flag = None
		self.order_item_list = None
		self.order_pay_time = None
		self.order_priority = None
		self.order_shop_create_time = None
		self.order_source = None
		self.order_sub_source = None
		self.order_type = None
		self.picker_call = None
		self.picker_id = None
		self.picker_name = None
		self.postfee = None
		self.prev_order_code = None
		self.receiver_info = None
		self.remark = None
		self.sender_info = None
		self.service_fee = None
		self.store_code = None
		self.tms_service_code = None
		self.tms_service_name = None
		self.transport_mode = None

	def getapiname(self):
		return 'taobao.wlb.wms.consign.order.notify'
