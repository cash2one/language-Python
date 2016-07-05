'''
Created by auto_sdk on 2015.04.17
'''
from top.api.base import RestApi
class OcTradetagAttachRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.tag_name = None
		self.tag_type = None
		self.tag_value = None
		self.tid = None
		self.visible = None

	def getapiname(self):
		return 'taobao.oc.tradetag.attach'
