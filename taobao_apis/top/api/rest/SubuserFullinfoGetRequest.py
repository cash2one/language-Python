'''
Created by auto_sdk on 2016.04.13
'''
from top.api.base import RestApi
class SubuserFullinfoGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.sub_id = None
		self.sub_nick = None

	def getapiname(self):
		return 'taobao.subuser.fullinfo.get'
