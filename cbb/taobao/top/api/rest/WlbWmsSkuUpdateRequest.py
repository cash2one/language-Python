'''
Created by auto_sdk on 2015.08.17
'''
from top.api.base import RestApi
class WlbWmsSkuUpdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.advent_lifecycle = None
		self.approval_number = None
		self.attribute = None
		self.bar_code = None
		self.brand = None
		self.brand_name = None
		self.category = None
		self.category_name = None
		self.color = None
		self.cost_price = None
		self.extend_fields = None
		self.gross_weight = None
		self.height = None
		self.is_batch_mgt = None
		self.is_danger = None
		self.is_hygroscopic = None
		self.is_shelflife = None
		self.is_sn_mgt = None
		self.item_id = None
		self.item_price = None
		self.length = None
		self.lifecycle = None
		self.lockup_lifecycle = None
		self.name = None
		self.net_weight = None
		self.origin_address = None
		self.pcs = None
		self.reject_lifecycle = None
		self.size = None
		self.specification = None
		self.store_code = None
		self.tag_price = None
		self.title = None
		self.type = None
		self.use_yn = None
		self.volume = None
		self.width = None

	def getapiname(self):
		return 'taobao.wlb.wms.sku.update'
