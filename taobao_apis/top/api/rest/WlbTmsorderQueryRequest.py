'''
Created by auto_sdk on 2016.04.13
'''
from top.api.base import RestApi
class WlbTmsorderQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_code = None
		self.page_no = None
		self.page_size = None

	def getapiname(self):
		return 'taobao.wlb.tmsorder.query'
