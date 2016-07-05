'''
Created by auto_sdk on 2015.09.11
'''
from top.api.base import RestApi
class TmallItemUpdateSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None
		self.item_id = None
		self.product_id = None

	def getapiname(self):
		return 'tmall.item.update.schema.get'
