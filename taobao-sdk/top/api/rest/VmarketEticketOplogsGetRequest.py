'''
Created by auto_sdk on 2014.11.21
'''
from top.api.base import RestApi
class VmarketEticketOplogsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.codemerchant_id = None
		self.end_time = None
		self.mobile = None
		self.page_no = None
		self.page_size = None
		self.posid = None
		self.sort = None
		self.start_time = None
		self.type = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.oplogs.get'
