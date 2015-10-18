'''
Created by auto_sdk on 2015.05.07
'''
from top.api.base import RestApi
class ItemSchemaIncrementUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None
		self.item_id = None
		self.parameters = None

	def getapiname(self):
		return 'taobao.item.schema.increment.update'
