'''
Created by auto_sdk on 2015.08.05
'''
from top.api.base import RestApi
class TmallItemSchemaIncrementUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.xml_data = None

	def getapiname(self):
		return 'tmall.item.schema.increment.update'
