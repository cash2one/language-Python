'''
Created by auto_sdk on 2016.04.06
'''
from top.api.base import RestApi
class WlbWmsInventoryCountRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.inventory.count'
