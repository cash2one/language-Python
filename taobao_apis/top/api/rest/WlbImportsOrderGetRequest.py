'''
Created by auto_sdk on 2016.01.27
'''
from top.api.base import RestApi
class WlbImportsOrderGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.gmt_create_end = None
		self.gmt_create_start = None
		self.page_no = None
		self.page_size = None
		self.status_code = None
		self.trade_id = None

	def getapiname(self):
		return 'taobao.wlb.imports.order.get'
