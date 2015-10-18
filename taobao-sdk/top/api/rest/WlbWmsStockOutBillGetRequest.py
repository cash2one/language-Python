'''
Created by auto_sdk on 2015.09.22
'''
from top.api.base import RestApi
class WlbWmsStockOutBillGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cn_order_code = None
		self.order_code = None

	def getapiname(self):
		return 'taobao.wlb.wms.stock.out.bill.get'
