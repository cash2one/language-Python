'''
Created by auto_sdk on 2015.05.29
'''
from top.api.base import RestApi
class TmallProductAddSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.brand_id = None
		self.category_id = None

	def getapiname(self):
		return 'tmall.product.add.schema.get'
