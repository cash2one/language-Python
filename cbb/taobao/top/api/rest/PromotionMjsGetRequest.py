'''
Created by auto_sdk on 2013.09.09
'''
from top.api.base import RestApi
class PromotionMjsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)

	def getapiname(self):
		return 'taobao.promotion.mjs.get'
