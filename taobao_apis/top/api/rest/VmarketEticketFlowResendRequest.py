'''
Created by auto_sdk on 2016.02.26
'''
from top.api.base import RestApi
class VmarketEticketFlowResendRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.biz_type = None
		self.outer_id = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.flow.resend'
