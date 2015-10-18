'''
Created by auto_sdk on 2015.07.29
'''
from top.api.base import RestApi
class VmarketEticketStoreGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.order_id = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.store.get'
