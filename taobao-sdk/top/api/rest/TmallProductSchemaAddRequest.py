'''
Created by auto_sdk on 2015.10.15
'''
from top.api.base import RestApi
class TmallProductSchemaAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.brand_id = None
		self.category_id = None
		self.xml_data = None

	def getapiname(self):
		return 'tmall.product.schema.add'
