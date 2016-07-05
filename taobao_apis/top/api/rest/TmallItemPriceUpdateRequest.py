'''
Created by auto_sdk on 2015.10.15
'''
from top.api.base import RestApi
class TmallItemPriceUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.item_id = None
		self.item_price = None
		self.options = None
		self.sku_prices = None

	def getapiname(self):
		return 'tmall.item.price.update'
