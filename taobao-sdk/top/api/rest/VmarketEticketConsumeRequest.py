'''
Created by auto_sdk on 2015.07.21
'''
from top.api.base import RestApi
class VmarketEticketConsumeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.codemerchant_id = None
		self.consume_num = None
		self.mobile = None
		self.new_code = None
		self.order_id = None
		self.posid = None
		self.qr_images = None
		self.serial_num = None
		self.token = None
		self.verify_code = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.consume'
