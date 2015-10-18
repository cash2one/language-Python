'''
Created by auto_sdk on 2014.04.21
'''
from top.api.base import RestApi
class VmarketTaomaMerchantConsumeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.consume_num = None
		self.operator = None
		self.serial_num = None
		self.verify_code = None

	def getapiname(self):
		return 'taobao.vmarket.taoma.merchant.consume'
