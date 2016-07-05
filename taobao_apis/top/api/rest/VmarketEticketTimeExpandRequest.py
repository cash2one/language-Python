'''
Created by auto_sdk on 2014.11.10
'''
from top.api.base import RestApi
class VmarketEticketTimeExpandRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.expand_days = None
		self.order_id = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.time.expand'
