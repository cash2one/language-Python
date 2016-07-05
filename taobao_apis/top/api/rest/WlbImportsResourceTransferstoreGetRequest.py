'''
Created by auto_sdk on 2016.01.27
'''
from top.api.base import RestApi
class WlbImportsResourceTransferstoreGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cids = None
		self.from_id = None
		self.resource_id = None
		self.to_address = None

	def getapiname(self):
		return 'taobao.wlb.imports.resource.transferstore.get'
