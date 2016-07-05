'''
Created by auto_sdk on 2016.02.17
'''
from top.api.base import RestApi
class WlbWmsCainiaoBillQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.end_modified_time = None
		self.order_type = None
		self.page_no = None
		self.page_size = None
		self.start_modified_time = None

	def getapiname(self):
		return 'taobao.wlb.wms.cainiao.bill.query'
