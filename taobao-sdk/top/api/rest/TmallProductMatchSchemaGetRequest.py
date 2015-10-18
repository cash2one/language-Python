'''
Created by auto_sdk on 2015.01.15
'''
from top.api.base import RestApi
class TmallProductMatchSchemaGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None

	def getapiname(self):
		return 'tmall.product.match.schema.get'
