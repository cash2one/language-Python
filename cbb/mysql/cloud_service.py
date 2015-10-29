# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, json, md5

PRODUCTION=True
#json.dumps(data, ensure_ascii=False)
URL_PREFIX = 'http://0.0.0.0:81'
if PRODUCTION: URL_PREFIX = 'http://0.0.0.0'

BASE_URL = URL_PREFIX + '/webservice/'
SECRET = ''

def post(api, act, data):
	if not data or not api: return

	data = sorted(data.iteritems(), key=lambda d:d[0], reverse=False)
	string = ''
	for i in range(len(data)):
		if not data[i][1] and data[i][1] != None: string += '@'
		else: string += str(data[i][1]) + '@'
	s = md5.new(SECRET + string[:-1]).hexdigest()

	print '\033[33m' + BASE_URL + api + act + str(s) + '\033[0m'
	try:
		request = urllib2.Request(BASE_URL + api + act + str(s), urllib.urlencode(data))
		response = urllib2.urlopen(request).read()
		return json.loads(response)
	except Exception, e:
		return json.loads('{"error":1, "data":"failed", "msg":"' + str(e) + '"}')

# 车系维护操作
class Cars:
	api = 'index.php?act='

	def AddSeries(self, data): # 车系添加
		act = 'car_series_add&AUTH_KEY='
		return post(self.api, act, data)

	def ModifySeries(self, data): # 车系修改
		act = 'car_series_edit&AUTH_KEY='
		return post(self.api, act, data)

	def GetSeriesList(self, data): # 车系列表
		act = 'car_series_list&AUTH_KEY='
		return post(self.api, act, data)

	def GetSeriesDetail(self, data): # 车系详情
		act = 'car_series_info&AUTH_KEY='
		return post(self.api, act, data)

	def DeleteSeries(self, data): # 车系删除
		act = 'car_series_del&AUTH_KEY='
		return post(self.api, act, data)

	def AddModel(self, data): # 车型添加
		act = 'car_model_add&AUTH_KEY='
		return post(self.api, act, data)

	def ModifyModel(self, data): # 车型修改
		act = 'car_model_edit&AUTH_KEY='
		return post(self.api, act, data)

	def GetModelList(self, data): # 车型列表
		act = 'car_model_list&AUTH_KEY='
		return post(self.api, act, data)

	def GetModelDetail(self, data): # 车型详情
		act = 'car_model_info&AUTH_KEY='
		return post(self.api, act, data)

	def DeleteModel(self, data): # 车型删除
		act = 'car_model_del&AUTH_KEY='
		return post(self.api, act, data)

	def PageConfig(self, data): # 页面配置
		act = 'car_config&AUTH_KEY='
		return post(self.api, act, data)

# 经销商管理操作
class Dealers:
	api = 'dealer.php?act='

	def AddDealer(self, data): # 经销商添加
		act = 'dealer_base_add&AUTH_KEY='
		return post(self.api, act, data)

	def ModifyDealer(self, data): # 经销商修改
		act = 'dealer_base_edit&AUTH_KEY='
		return post(self.api, act, data)

	def GetDealerList(self, data): # 经销商列表
		act = 'dealer_list&AUTH_KEY='
		return post(self.api, act, data)

	def GetDealerDetail(self, data): # 经销商详情
		act = 'dealer_info&AUTH_KEY='
		return post(self.api, act, data)

	def DeleteDealer(self, data): # 经销商删除
		act = 'dealer_del&AUTH_KEY='
		return post(self.api, act, data)

	def AddPrice(self, data): # 经销商报价
		act = 'dealer_price_do&AUTH_KEY='
		return post(self.api, act, data)

	def GetPriceList(self, data): # 报价列表
		act = 'dealer_price_list&AUTH_KEY='
		return post(self.api, act, data)

	def DeletePrice(self, data): # 经销商报价删除
		act = 'dealer_price_del&AUTH_KEY='
		return post(self.api, act, data)

	def DealerSeries(self, data):
		self.api = 'webservice.php/webservice/dealer/'
		act = 'update_series?sign='
		return post(self.api, act, data)

# 活动维护操作
class Activities:
	api = 'dealer.php?act='

	def AddActivity(self, data): # 活动添加
		act = 'activity_add&AUTH_KEY='
		return post(self.api, act, data)

	def ModifyActivity(self, data): # 活动修改
		act = 'activity_edit&AUTH_KEY='
		return post(self.api, act, data)

	def GetActivityList(self, data): # 活动列表
		act = 'activity_list&AUTH_KEY='
		return post(self.api, act, data)

	def GetActivityDetail(self, data): # 活动详情
		act = 'activity_info&AUTH_KEY='
		return post(self.api, act, data)

	def DeleteActivity(self, data): # 活动删除
		act = 'activity_del&AUTH_KEY='
		return post(self.api, act, data)

	def AddPromotion(self, data): # 车型促销添加
		act = 'promotions_add&AUTH_KEY='
		return post(self.api, act, data)

	def ModifyPromotion(self, data): # 车型促销修改
		act = 'promotions_edit&AUTH_KEY='
		return post(self.api, act, data)

	def GetPromotionList(self, data): # 车型促销列表
		act = 'promotions_list&AUTH_KEY='
		return post(self.api, act, data)

	def GetPromotionDetail(self, data): # 车型促销详情
		act = 'promotions_info&AUTH_KEY='
		return post(self.api, act, data)

	def DeletePromotion(self, data): # 车型促销删除
		act = 'promotions_del&AUTH_KEY='
		return post(self.api, act, data)

class Customers:
	api = 'customer.php?act='

	def GetApplyList(self, data): # 留资列表
		act = 'customer_apply_list&AUTH_KEY='
		return post(self.api, act, data)

	def ModifyCheckStatus(self, data): # 修改核销状态
		act = 'customer_verify_status&AUTH_KEY='
		return post(self.api, act, data)

	def DeleteApply(self, data): # 留资信息删除
		act = 'apply_del&AUTH_KEY='
		return post(self.api, act, data)

class Financial:
	api = 'webservice.php/webservice/financial/'

	def AddFinancial(self, data):
		act = 'update_financial?sign='
		return post(self.api, act, data)

	def FinancialBrand(self, data):
		act = 'update_financial_band?sign='	#Todo
		return post(self.api, act, data)

	def FinancialDealer(self, data):
		act = 'update_dealer?sign='
		return post(self.api, act, data)

	def FinancialSeries(self, data):
		act = 'update_series?sign='
		return post(self.api, act, data)

class Debug:
	def Post(self, url, data):
		return post(url, '', data)

	def sms(self, url, data):
		return post(url, '', data)
