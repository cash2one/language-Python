'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsOrderCancelNotifyRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None
		self.order_type = None
		self.store_code = None

	def getapiname(self):
		return 'taobao.wlb.wms.order.cancel.notify'
