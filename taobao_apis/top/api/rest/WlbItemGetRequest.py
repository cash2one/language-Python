'''
Created by auto_sdk on 2016.03.15
'''
from top.api.base import RestApi
class WlbItemGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None

	def getapiname(self):
		return 'taobao.wlb.item.get'
