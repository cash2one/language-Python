'''
Created by auto_sdk on 2016.03.19
'''
from top.api.base import RestApi
class SellercenterSubusersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.nick = None

	def getapiname(self):
		return 'taobao.sellercenter.subusers.get'
