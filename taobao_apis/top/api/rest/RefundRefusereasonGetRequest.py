'''
Created by auto_sdk on 2016.02.20
'''
from top.api.base import RestApi
class RefundRefusereasonGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.refund_id = None
		self.refund_phase = None

	def getapiname(self):
		return 'taobao.refund.refusereason.get'
