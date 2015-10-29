'''
Created by auto_sdk on 2014.03.25
'''
from top.api.base import RestApi
class TmallProductSuitespecsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.cat_id = None
		self.product_id = None
		self.properties = None

	def getapiname(self):
		return 'tmall.product.suitespecs.get'
