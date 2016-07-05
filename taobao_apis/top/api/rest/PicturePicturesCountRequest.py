'''
Created by auto_sdk on 2015.10.13
'''
from top.api.base import RestApi
class PicturePicturesCountRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.client_type = None
		self.deleted = None
		self.end_date = None
		self.picture_category_id = None
		self.picture_id = None
		self.start_date = None
		self.start_modified_date = None
		self.title = None

	def getapiname(self):
		return 'taobao.picture.pictures.count'
