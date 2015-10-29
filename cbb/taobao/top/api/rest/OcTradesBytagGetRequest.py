'''
Created by auto_sdk on 2015.04.17
'''
from top.api.base import RestApi
class OcTradesBytagGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.page = None
		self.page_size = None
		self.tag_name = None
		self.tag_type = None

	def getapiname(self):
		return 'taobao.oc.trades.bytag.get'
