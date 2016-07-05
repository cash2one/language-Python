'''
Created by auto_sdk on 2016.01.27
'''
from top.api.base import RestApi
class WlbImportsOrderCancelRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.lgorder_code = None

	def getapiname(self):
		return 'taobao.wlb.imports.order.cancel'
