'''
Created by auto_sdk on 2014.11.10
'''
from top.api.base import RestApi
class RpReturngoodsAgreeRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.address = None
		self.mobile = None
		self.name = None
		self.post = None
		self.refund_id = None
		self.refund_phase = None
		self.refund_version = None
		self.remark = None
		self.seller_address_id = None
		self.tel = None

	def getapiname(self):
		return 'taobao.rp.returngoods.agree'
