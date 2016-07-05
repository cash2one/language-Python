'''
Created by auto_sdk on 2016.03.15
'''
from top.api.base import RestApi
class WlbWmsSnInfoQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None
		self.order_code_type = None
		self.page_index = None

	def getapiname(self):
		return 'taobao.wlb.wms.sn.info.query'
