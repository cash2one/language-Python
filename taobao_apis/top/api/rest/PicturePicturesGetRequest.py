'''
Created by auto_sdk on 2016.03.23
'''
from top.api.base import RestApi
class PicturePicturesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.client_type = None
		self.current_page = None
		self.deleted = None
		self.end_date = None
		self.is_https = None
		self.order_by = None
		self.page_size = None
		self.picture_category_id = None
		self.picture_id = None
		self.start_date = None
		self.start_modified_date = None
		self.title = None
		self.urls = None

	def getapiname(self):
		return 'taobao.picture.pictures.get'
