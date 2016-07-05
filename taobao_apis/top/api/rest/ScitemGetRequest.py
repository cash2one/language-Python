'''
Created by auto_sdk on 2012.11.28
'''
from top.api.base import RestApi
class ScitemGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None

	def getapiname(self):
		return 'taobao.scitem.get'
