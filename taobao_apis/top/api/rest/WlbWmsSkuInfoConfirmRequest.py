'''
Created by auto_sdk on 2016.01.29
'''
from top.api.base import RestApi
class WlbWmsSkuInfoConfirmRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.content = None

	def getapiname(self):
		return 'taobao.wlb.wms.sku.info.confirm'
