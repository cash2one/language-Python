'''
Created by auto_sdk on 2014.02.28
'''
from top.api.base import RestApi
class ItemTemplatesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.item.templates.get'
