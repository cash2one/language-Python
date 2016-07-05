'''
Created by auto_sdk on 2016.03.06
'''
from top.api.base import RestApi
class VmarketEticketFailsendRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.error_code = None
		self.error_msg = None
		self.order_id = None
		self.token = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.failsend'
