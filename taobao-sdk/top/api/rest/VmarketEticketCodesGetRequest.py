'''
Created by auto_sdk on 2012.12.06
'''
from top.api.base import RestApi
class VmarketEticketCodesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.codemerchant_id = None
		self.order_id = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.codes.get'
