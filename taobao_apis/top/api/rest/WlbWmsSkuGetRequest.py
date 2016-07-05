'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsSkuGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_code = None
		self.item_id = None
		self.owner_user_id = None

	def getapiname(self):
		return 'taobao.wlb.wms.sku.get'
