'''
Created by auto_sdk on 2014.03.18
'''
from top.api.base import RestApi
class WangwangEserviceGroupmemberGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.manager_id = None

	def getapiname(self):
		return 'taobao.wangwang.eservice.groupmember.get'
