'''
Created by auto_sdk on 2013.11.05
'''
from top.api.base import RestApi
class WangwangEserviceStreamweigthsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.wangwang.eservice.streamweigths.get'
