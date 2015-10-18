'''
Created by auto_sdk on 2015.08.14
'''
from top.api.base import RestApi
class WmsOrderWarehouseRouteGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None

	def getapiname(self):
		return 'taobao.wms.order.warehouse.route.get'
