'''
Created by auto_sdk on 2015.02.25
'''
from top.api.base import RestApi
class JdsRefundTracesGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.refund_id = None
		self.return_user_status = None

	def getapiname(self):
		return 'taobao.jds.refund.traces.get'
