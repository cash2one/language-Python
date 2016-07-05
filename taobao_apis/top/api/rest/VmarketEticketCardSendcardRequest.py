'''
Created by auto_sdk on 2015.07.25
'''
from top.api.base import RestApi
class VmarketEticketCardSendcardRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.actual_value = None
		self.card_id = None
		self.card_level = None
		self.codemerchant_id = None
		self.expand_value = None
		self.order_id = None
		self.token = None
		self.user_nick = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.card.sendcard'
