'''
Created by auto_sdk on 2015.02.04
'''
from top.api.base import RestApi
class TmallProductSchemaMatchRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.category_id = None
		self.propvalues = None

	def getapiname(self):
		return 'tmall.product.schema.match'
