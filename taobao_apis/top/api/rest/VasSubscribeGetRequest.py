'''
Created by auto_sdk on 2016.04.11
'''
from top.api.base import RestApi
class VasSubscribeGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.article_code = None
		self.nick = None

	def getapiname(self):
		return 'taobao.vas.subscribe.get'
