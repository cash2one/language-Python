'''
Created by auto_sdk on 2016.04.13
'''
from top.api.base import RestApi
class VmarketEticketTasksGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.codemerchant_id = None
		self.page_no = None
		self.page_size = None
		self.seller_id = None
		self.type = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.tasks.get'
