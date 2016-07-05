'''
Created by auto_sdk on 2016.04.07
'''
from top.api.base import RestApi
class VmarketEticketReverseRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.codemerchant_id = None
		self.consume_secial_num = None
		self.order_id = None
		self.posid = None
		self.qr_images = None
		self.reverse_code = None
		self.reverse_num = None
		self.token = None
		self.verify_codes = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.reverse'
