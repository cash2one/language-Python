'''
Created by auto_sdk on 2015.09.17
'''
from top.api.base import RestApi
class WlbWmsInventoryLackUploadRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.inventory.lack.upload'
