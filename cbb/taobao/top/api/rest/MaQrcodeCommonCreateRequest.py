'''
Created by auto_sdk on 2015.04.23
'''
from top.api.base import RestApi
class MaQrcodeCommonCreateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.channel_name = None
		self.content = None
		self.logo = None
		self.name = None
		self.need_eps = None
		self.size = None
		self.style = None
		self.type = None

	def getapiname(self):
		return 'taobao.ma.qrcode.common.create'
