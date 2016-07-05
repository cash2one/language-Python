'''
Created by auto_sdk on 2015.11.16
'''
from top.api.base import RestApi
class WlbWmsInventoryQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.batch_code = None
		self.channel_code = None
		self.due_date = None
		self.inventory_type = None
		self.item_id = None
		self.page_no = None
		self.page_size = None
		self.produce_date = None
		self.store_code = None
		self.type = None

	def getapiname(self):
		return 'taobao.wlb.wms.inventory.query'
