'''
Created by auto_sdk on 2015.12.29
'''
from top.api.base import RestApi
class DeliveryTemplatesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None

	def getapiname(self):
		return 'taobao.delivery.templates.get'
