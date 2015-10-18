'''
Created by auto_sdk on 2015.01.15
'''
from top.api.base import RestApi
class WlbItemMapGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None

	def getapiname(self):
		return 'taobao.wlb.item.map.get'
