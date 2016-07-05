'''
Created by auto_sdk on 2016.01.25
'''
from top.api.base import RestApi
class WlbWmsConsignBillGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cn_order_code = None
		self.order_code = None

	def getapiname(self):
		return 'taobao.wlb.wms.consign.bill.get'
