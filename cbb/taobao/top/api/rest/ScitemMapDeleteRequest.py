'''
Created by auto_sdk on 2013.04.09
'''
from top.api.base import RestApi
class ScitemMapDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.sc_item_id = None
		self.user_nick = None

	def getapiname(self):
		return 'taobao.scitem.map.delete'
