'''
Created by auto_sdk on 2015.05.06
'''
from top.api.base import RestApi
class ItemIncrementUpdateSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None
		self.item_id = None
		self.update_fields = None

	def getapiname(self):
		return 'taobao.item.increment.update.schema.get'
