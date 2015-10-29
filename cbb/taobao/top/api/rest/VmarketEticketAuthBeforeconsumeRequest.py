'''
Created by auto_sdk on 2013.07.12
'''
from top.api.base import RestApi
class VmarketEticketAuthBeforeconsumeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.operatorid = None
		self.storeid = None
		self.verify_code = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.auth.beforeconsume'
