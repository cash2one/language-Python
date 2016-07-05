'''
Created by auto_sdk on 2016.01.27
'''
from top.api.base import RestApi
class WlbImportsGeneralConsignRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cancel_id = None
		self.first_logistics = None
		self.first_waybillno = None
		self.resource_id = None
		self.sender_id = None
		self.store_code = None
		self.trade_order_id = None

	def getapiname(self):
		return 'taobao.wlb.imports.general.consign'
