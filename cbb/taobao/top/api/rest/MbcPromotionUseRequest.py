'''
Created by auto_sdk on 2015.09.06
'''
from top.api.base import RestApi
class MbcPromotionUseRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.actual_fee = None
		self.discount_fee = None
		self.end_time = None
		self.outer_no = None
		self.promotion_id = None
		self.promotion_type = None
		self.start_time = None
		self.total_fee = None
		self.use_time = None
		self.user_id = None

	def getapiname(self):
		return 'taobao.mbc.promotion.use'
