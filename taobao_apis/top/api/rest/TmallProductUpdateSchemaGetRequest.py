'''
Created by auto_sdk on 2016.02.29
'''
from top.api.base import RestApi
class TmallProductUpdateSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.product_id = None

	def getapiname(self):
		return 'tmall.product.update.schema.get'
