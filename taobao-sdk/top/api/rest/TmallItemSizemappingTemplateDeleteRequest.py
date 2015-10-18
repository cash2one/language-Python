'''
Created by auto_sdk on 2015.01.23
'''
from top.api.base import RestApi
class TmallItemSizemappingTemplateDeleteRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.template_id = None

	def getapiname(self):
		return 'tmall.item.sizemapping.template.delete'
