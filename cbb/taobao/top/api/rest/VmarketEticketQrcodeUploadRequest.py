'''
Created by auto_sdk on 2015.06.18
'''
from top.api.base import RestApi
class VmarketEticketQrcodeUploadRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code_merchant_id = None
		self.img_bytes = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.qrcode.upload'

	def getMultipartParas(self):
		return ['img_bytes']
