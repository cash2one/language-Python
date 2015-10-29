'''
Created by auto_sdk on 2015.07.15
'''
from top.api.base import RestApi
class WlbWaybillICancelRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.waybill_apply_cancel_request = None

	def getapiname(self):
		return 'taobao.wlb.waybill.i.cancel'
