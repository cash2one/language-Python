'''
Created by auto_sdk on 2015.06.16
'''
from top.api.base import RestApi
class JdsTradeTracesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.return_user_status = None
		self.tid = None

	def getapiname(self):
		return 'taobao.jds.trade.traces.get'
