'''
Created by auto_sdk on 2014.12.12
'''
from top.api.base import RestApi
class MarketingPromotionsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.fields = None
		self.is_new_tag = None
		self.num_iid = None
		self.page_no = None
		self.page_size = None
		self.prom_id = None
		self.status = None
		self.tag_id = None

	def getapiname(self):
		return 'taobao.marketing.promotions.get'
