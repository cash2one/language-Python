'''
Created by auto_sdk on 2015.09.11
'''
from top.api.base import RestApi
class TmallItemShiptimeUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.option = None
		self.ship_time = None
		self.sku_ship_times = None

	def getapiname(self):
		return 'tmall.item.shiptime.update'
