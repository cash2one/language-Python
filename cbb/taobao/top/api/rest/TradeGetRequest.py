'''
Created by auto_sdk on 2015.10.14
'''
from top.api.base import RestApi
class TradeGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.tid = None

	def getapiname(self):
		return 'taobao.trade.get'
