'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsStockPruductProcessingNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.extend_fields = None
		self.material_items = None
		self.order_code = None
		self.order_create_time = None
		self.order_type = None
		self.plan_qty = None
		self.plan_work_time = None
		self.product_items = None
		self.remark = None
		self.service_type = None
		self.store_code = None

	def getapiname(self):
		return 'taobao.wlb.wms.stock.pruduct.processing.notify'
