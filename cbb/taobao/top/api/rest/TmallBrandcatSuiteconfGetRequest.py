'''
Created by auto_sdk on 2014.03.25
'''
from top.api.base import RestApi
class TmallBrandcatSuiteconfGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'tmall.brandcat.suiteconf.get'
