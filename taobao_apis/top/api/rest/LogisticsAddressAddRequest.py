'''
Created by auto_sdk on 2016.04.11
'''
from top.api.base import RestApi
class LogisticsAddressAddRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.addr = None
		self.cancel_def = None
		self.city = None
		self.contact_name = None
		self.country = None
		self.get_def = None
		self.memo = None
		self.mobile_phone = None
		self.phone = None
		self.province = None
		self.seller_company = None
		self.send_def = None
		self.zip_code = None

	def getapiname(self):
		return 'taobao.logistics.address.add'
