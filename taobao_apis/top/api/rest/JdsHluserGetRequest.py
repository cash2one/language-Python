'''
Created by auto_sdk on 2015.02.25
'''
from top.api.base import RestApi
class JdsHluserGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.jds.hluser.get'
