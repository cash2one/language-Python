'''
Created by auto_sdk on 2016.03.05
'''
from top.api.base import RestApi
class SellercenterRolemembersGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.role_id = None

	def getapiname(self):
		return 'taobao.sellercenter.rolemembers.get'
