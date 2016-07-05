'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsSkuCombinationCreateUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.dest_item = None
		self.item_id = None
		self.owner_user_id = None
		self.proportion = None

	def getapiname(self):
		return 'taobao.wlb.wms.sku.combination.create.update'
