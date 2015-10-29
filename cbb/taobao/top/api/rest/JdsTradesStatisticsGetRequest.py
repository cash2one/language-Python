'''
Created by auto_sdk on 2015.04.13
'''
from top.api.base import RestApi
class JdsTradesStatisticsGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.date = None

	def getapiname(self):
		return 'taobao.jds.trades.statistics.get'
