'''
Created by auto_sdk on 2013.11.18
'''
from top.api.base import RestApi
class VmarketEticketQrcodeImguploadRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None
		self.code_merchant_id = None
		self.img_bytes = None
		self.order_id = None

	def getapiname(self):
		return 'taobao.vmarket.eticket.qrcode.imgupload'

	def getMultipartParas(self):
		return ['img_bytes']
