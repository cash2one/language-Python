'''
Created by auto_sdk on 2015.04.28
'''
from top.api.base import RestApi
class WlbImportsWaybillGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None

	def getapiname(self):
		return 'taobao.wlb.imports.waybill.get'
