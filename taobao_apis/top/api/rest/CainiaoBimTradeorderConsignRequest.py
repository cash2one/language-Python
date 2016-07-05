'''
Created by auto_sdk on 2016.03.01
'''
from top.api.base import RestApi
class CainiaoBimTradeorderConsignRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.store_code = None
		self.trade_id = None

	def getapiname(self):
		return 'cainiao.bim.tradeorder.consign'
