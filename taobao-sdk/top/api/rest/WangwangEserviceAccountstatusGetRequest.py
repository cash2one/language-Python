'''
Created by auto_sdk on 2014.07.02
'''
from top.api.base import RestApi
class WangwangEserviceAccountstatusGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.btime = None
		self.etime = None
		self.uid = None

	def getapiname(self):
		return 'taobao.wangwang.eservice.accountstatus.get'
