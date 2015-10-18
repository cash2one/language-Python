'''
Created by auto_sdk on 2015.07.15
'''
from top.api.base import RestApi
class PictureUploadRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.client_type = None
		self.image_input_title = None
		self.img = None
		self.is_https = None
		self.picture_category_id = None
		self.picture_id = None
		self.title = None

	def getapiname(self):
		return 'taobao.picture.upload'

	def getMultipartParas(self):
		return ['img']
