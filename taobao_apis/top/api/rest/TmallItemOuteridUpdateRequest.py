'''
Created by auto_sdk on 2015.06.09
'''
from top.api.base import RestApi
class TmallItemOuteridUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.outer_id = None
		self.sku_outers = None

	def getapiname(self):
		return 'tmall.item.outerid.update'
