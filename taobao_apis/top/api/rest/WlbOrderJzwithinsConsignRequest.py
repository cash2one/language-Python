'''
Created by auto_sdk on 2015.03.11
'''
from top.api.base import RestApi
class WlbOrderJzwithinsConsignRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.ins_partner = None
		self.jz_consign_args = None
		self.tid = None
		self.tms_partner = None

	def getapiname(self):
		return 'taobao.wlb.order.jzwithins.consign'
