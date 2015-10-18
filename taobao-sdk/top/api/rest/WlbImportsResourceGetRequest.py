'''
Created by auto_sdk on 2015.09.24
'''
from top.api.base import RestApi
class WlbImportsResourceGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.from_id = None
		self.to_address = None

	def getapiname(self):
		return 'taobao.wlb.imports.resource.get'
