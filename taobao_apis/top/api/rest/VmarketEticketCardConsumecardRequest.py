'''
Created by auto_sdk on 2015.07.17
'''
from top.api.base import RestApi
class VmarketEticketCardConsumecardRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.buyer_nick = None
		self.card_id = None
		self.card_level = None
		self.consume_code = None
		self.consume_serial_num = None
		self.consume_value = None
		self.operator_id = None
		self.reason = None
		self.store_id = None
		self.token = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.card.consumecard'
