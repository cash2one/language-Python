'''
Created by auto_sdk on 2015.11.04
'''
from top.api.base import RestApi
class ItemRecommendDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.num_iid = None

	def getapiname(self):
		return 'taobao.item.recommend.delete'
