'''
Created by auto_sdk on 2012.10.16
'''
from top.api.base import RestApi
class AftersaleGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.aftersale.get'
