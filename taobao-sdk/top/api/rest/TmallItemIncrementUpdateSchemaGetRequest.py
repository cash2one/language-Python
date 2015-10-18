'''
Created by auto_sdk on 2015.08.03
'''
from top.api.base import RestApi
class TmallItemIncrementUpdateSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.xml_data = None

	def getapiname(self):
		return 'tmall.item.increment.update.schema.get'
