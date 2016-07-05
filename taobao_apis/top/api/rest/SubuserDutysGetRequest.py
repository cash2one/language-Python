'''
Created by auto_sdk on 2016.04.13
'''
from top.api.base import RestApi
class SubuserDutysGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.user_nick = None

	def getapiname(self):
		return 'taobao.subuser.dutys.get'
