'''
Created by auto_sdk on 2015.05.29
'''
from top.api.base import RestApi
class TmallProductSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.product_id = None

	def getapiname(self):
		return 'tmall.product.schema.get'
