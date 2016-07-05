'''
Created by auto_sdk on 2015.02.25
'''
from top.api.base import RestApi
class JdsHluserUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.open_for_buyer = None
		self.open_nodes = None

	def getapiname(self):
		return 'taobao.jds.hluser.update'
