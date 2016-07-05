'''
Created by auto_sdk on 2016.03.08
'''
from top.api.base import RestApi
class SellercenterRoleAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.description = None
		self.name = None
		self.nick = None
		self.permission_codes = None

	def getapiname(self):
		return 'taobao.sellercenter.role.add'
