'''
Created by auto_sdk on 2014.12.12
'''
from top.api.base import RestApi
class PromotionActivityGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.activity_id = None

	def getapiname(self):
		return 'taobao.promotion.activity.get'
