# -*- coding: utf-8 -*-
#!/usr/bin/env python

from cloud_service import Cars, Dealers, Activities, Customers, Financial, Debug
import sys, json, urllib
from simplemysql import SimpleMysql

db = None
STEP = 50
DEBUG = False

def connect(host, db, user, passwd):
	print '[INFO]', 'Connecting to host', host, '...'
	tmp = SimpleMysql(host=host, db=db, user=user, passwd=passwd)
	if tmp: print '[INFO]', 'Connected to host', host, '.'
	return tmp

def rec2json(sql):
	try:
		rows = db.query(sql).fetchall()
		if not rows: return
		result = []
		for row in rows:
			data = {}
			for col in row:
				data[col] = row[col]
			result.append(data)
		if result: return json.dumps(result, ensure_ascii=False)
	except Exception, e:
		print e

def rec2jsonlist(sql):
	try:
		rows = db.query(sql).fetchall()
		if not rows: return
		result = []
		for row in rows:
			tmp = row.values()[0].strip()
			if tmp: result.append(tmp)
		if result: return json.dumps(result, ensure_ascii=False)
	except Exception, e:
		print e

def calc(prepay, item, pid, tp):
	total = 10000
	loan = total * (100 - prepay) / 100
	monthpay = 0

	result = []
	for i in item:
		data = {}
		rate = float(i['sku_rate']) / 100 / 12
		if rate < 0: rate = 0
		if tp == 1 or tp == 3:
			if rate:
				monthpay = loan * pow(1 + rate, i['sku_item']) * rate / (pow(1 + rate, i['sku_item']) - 1)
			else:
				monthpay = loan / i['sku_item']
			interest = monthpay * i['sku_item'] - loan
		elif tp == 2:
			interest = loan * rate / 100
			monthpay = loan / i['sku_item']
		data['period'] = i['sku_item']
		data['monthly'] = format(monthpay * 100, '.2f')
		data['interest'] = format(interest * 100, '.2f')
		tmp = "SELECT SKU_RATE FROM t_e4s_db_financial_pro_sku WHERE FINACIAL_PRODUCT_ID = '"+str(pid)+"' AND SKU_ITEM='"+str(i['sku_item'])+"'"
		data['annually'] = rec2jsonlist(tmp)[0]
		result.append(data)
	return result

def buildurl(field):
	base_url = 'http://www.chebaba.com/'
	return base_url + field

def InsertSeries():
	print '\n[INFO]', '开始更新车系数据...'

	rows = True
	pos = 0
	index = 0
	item = Cars()
	while rows:
		sql = '''
SELECT
	s.CAR_SERIES_ID series_id,
	s.CAR_BRAND_CODE brand_id,
	s.STRUCTURE `level`,
	s.CAR_SERIES_CN `name`,
	s.CAR_SERIES_EN en_name,
	s.MAIN_IMG logo,
	s.BIG_IMG picture,
	s.AD_IMG banner,
	0 discount_min,
	'' discount_min_pid,
	0 discount_max,
	'' discount_max_pid,
	s.START_GUIDEPRICE price_min,
	s.END_GUIDEPRICE price_max,
	s.IS_ENABLE isactive
FROM
	t_e4s_db_ve_car_series s
WHERE
	s.IS_ENABLE='1' 
	'''
		# sql += 'and s.CAR_SERIES_ID=101401 '
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['series_id']: continue
			data['series_id'] = row['series_id']
			data['brand_id'] = row['brand_id']
			if not row['name']: continue
			data['name'] = row['name']
			data['level'] = row['level']
			if not row['en_name']: continue
			data['en_name'] = row['en_name']
			data['logo'] = buildurl(row['logo'])
			data['picture'] = buildurl(row['picture'])
			data['banner'] = buildurl(row['banner'])
			data['banner_link'] = ''

			tmp = "SELECT MAX(PUBLIC_OFFER_PRICE) max_price, CAR_TYPE discount_min_pid FROM t_e4s_bu_offer_price t LEFT JOIN car_type c ON t.car_type = c.UUID WHERE c.CAR_SERIES_ID = '" + data['series_id'] + "';"
			tmp_result = json.loads(rec2json(tmp))
			data['discount_min'] = tmp_result[0]['max_price']
			data['discount_max_pid'] = tmp_result[0]['discount_min_pid']

			tmp = "SELECT MIN(PUBLIC_OFFER_PRICE) min_price, CAR_TYPE discount_max_pid FROM t_e4s_bu_offer_price t LEFT JOIN car_type c ON t.car_type = c.UUID WHERE c.CAR_SERIES_ID = '" + data['series_id'] + "';"
			tmp_result = json.loads(rec2json(tmp))
			data['discount_max'] = tmp_result[0]['min_price']
			data['discount_min_pid'] = tmp_result[0]['discount_max_pid']

			data['price_min'] = int(row['price_min']) * 100
			data['price_max'] = int(row['price_max']) * 100
			data['isactive'] = row['isactive']

			ret = item.AddSeries(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['name'], data['en_name']

def InsertModel():
	print '\n[INFO]', '开始更新车型数据...'
	# 特色参数：203 205 206，搜索表名：proper，两个表有关联
	rows = True
	pos = 0
	index = 0
	item = Cars()

	while rows:
		sql = '''
SELECT
	UUID model_id,
	CAR_SERIES_ID series_id,
	TYPE_NAME model_name,
	GUIDE_PRICE model_price,
	0 'Tmall_Discount',
	IS_ENABLE model_status,
	ALL_MONEY all_money,
	TAX_AND_INSURANCE tax_and_insurance,
	PURCHASE_TAX purchase_tax,
	VEHICLE_TAX vehicle_tax,
	TRAFFIC_TAX traffic_tax,
	COMMERCE_INSURANCE commerce_insurance
FROM
	car_type WHERE IS_ENABLE='1'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['series_id'] = row['series_id']
			data['model_id'] = row['model_id']
			data['model_e4s_id'] = row['model_id']
			if not row['model_name']: continue
			data['model_name'] = row['model_name']
			if not row['model_price']: row['model_price'] = 0
			data['model_price'] = int(row['model_price']) * 100
			data['Tmall_Discount'] = 0
			tmp = "SELECT a.CAR_COLOR_CODE color_name, b.RGB ascii_code FROM t_e4s_db_car_series_color a LEFT JOIN t_e4s_base_color b ON a.CAR_COLOR_CODE = b.`NAME` WHERE CAR_SERIES_ID='"+row['series_id']+"'"
			tmp = rec2json(tmp)
			if tmp: data['model_color'] = tmp
			tmp = '''
SELECT DISTINCT PROPERTY_VALUE FROM t_e4s_bu_car_type_property
WHERE PROPERTY_ID IN ( SELECT id FROM t_e4s_bu_property_template WHERE `name` IN ('车型特色参数I', '车型特色参数II', '车型特色参数III') )
AND IS_ENABLE = '1' AND CAR_TYPE_ID=
			'''
			tmp += "'" + row['model_id'] + "' LIMIT 3"
			tmp = rec2jsonlist(tmp)
			if tmp: data['model_attrib'] = tmp
			data['model_status'] = int(row['model_status'])
			data['all_money'] = int(row['all_money']) * 100
			data['tax_and_insurance'] = int(row['tax_and_insurance']) * 100
			data['purchase_tax'] = int(row['purchase_tax']) * 100
			data['vehicle_tax'] = int(row['vehicle_tax']) * 100
			data['traffic_tax'] = int(row['traffic_tax']) * 100
			data['commerce_insurance'] = int(row['commerce_insurance']) * 100

			ret = item.AddModel(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['model_name'], data['model_price']

def InsertDealer():
	print '\n[INFO]', '开始更新经销商数据...'

	rows = True
	pos = 0
	index = 0
	item = Dealers()
	while rows:
		sql = '''
SELECT
	s.STORE_ID dealer_id,
	s.IS_VIP isVIP,
	s.MAIN_BRAND brands,
	s.COMPANY_NAME dealer_name,
	s.STORE_NAME dealer_name_short,
	s.DLR_CODE dealer_code,
	s.county_id dealer_district,
	s.CITY_ID dealer_city,
	s.PROVINCE_ID dealer_province,
	s.X_COORDINATE dealer_long,
	s.Y_COORDINATE dealer_lat,
	s.ADDRESS dealer_address,
	s.SERVICE_PHONE dealer_phone,
	s.AFTER_SALES_SCORE after_score,
	s.PRE_SALES_SCORE pre_score,
	s.AFTER_SALES_SCORE_PROP after_score_rate,
	s.PRE_SALES_SCORE_PROP pre_score_rate,
	c.`STATUS` dealer_status
FROM
	store s
LEFT JOIN customer_account c ON c.CUSTOMER_ID = s.STORE_ID '''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			data['isVIP'] = row['isVIP']
			data['brands'] = row['brands']
			if not row['dealer_name']: continue
			data['dealer_name'] = row['dealer_name']
			if not row['dealer_name_short']: continue
			data['dealer_name_short'] = row['dealer_name_short']
			if not row['dealer_code']: continue
			data['dealer_code'] = row['dealer_code']
			data['dealer_district'] = row['dealer_district']
			data['dealer_city'] = row['dealer_city']
			data['dealer_province'] = row['dealer_province']
			data['dealer_long'] = row['dealer_long']
			data['dealer_lat'] = row['dealer_lat']
			data['dealer_address'] = row['dealer_address']
			data['dealer_phone'] = row['dealer_phone']
			data['after_score'] = row['after_score']
			data['after_score_rate'] = row['after_score_rate']
			data['pre_score'] = row['pre_score']
			data['pre_score_rate'] = row['pre_score_rate']
			data['dealer_status'] = row['dealer_status']

			ret = item.AddDealer(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['dealer_code'], data['dealer_name']

def DealerSeries():	# Todo: 签名方式修改
	print '\n[INFO]', '开始更新经销商推荐车系数据...'

	rows = True
	pos = 0
	index = 0
	item = Dealers()
	while rows:
		sql = '''
SELECT
	STORE_ID dealer_id,
	CAR_SERISE_ID series_id,
	DESCRIPTION word,
	HAS_SELECTED istop,
	'' lowest_price
FROM
	t_e4s_db_recommend_car_series_setting
WHERE
	CAR_SERISE_ID=101401 
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			if not row['series_id']: continue
			data['series_id'] = row['series_id']
			data['word'] = row['word']
			data['istop'] = row['istop']
			tmp = "SELECT MIN(t.PUBLIC_OFFER_PRICE) min_price FROM t_e4s_bu_offer_price t LEFT JOIN car_type c ON t.car_type = c.UUID "
			tmp += "WHERE c.CAR_SERIES_ID='"+data['series_id']+"' AND t.STORE_ID='" + data['dealer_id'] + "' AND t.PUBLIC_OFFER_PRICE>10000"
			tmp = json.loads(rec2json(tmp))
			if not tmp: continue
			data['lowest_price'] = 0
			if tmp[0]['min_price']: data['lowest_price'] = int(tmp[0]['min_price']) * 100
			if data['lowest_price'] == 0: continue

			ret = item.DealerSeries(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['dealer_id'], data['series_id'], data['lowest_price'], ret

def InsertActivity(last_update = None):
	print '\n[INFO]', '开始更新活动数据...'

	rows = True
	pos = 0
	index = 0
	item = Activities()
	while rows:
		sql = '''
SELECT
	activities_id activity_id,
	activities_type type,
	dlr_id dealer_id,
	active_title title,
	short_active_title title_short,
	home_picture pic,
	action_begin_date start_date,
	action_end_date end_date,
	contact_phone phone,
	'' activity_discount,
	address activity_address,
	active_desc detail,
	'' package,
	'' car_model,
	audit_status activity_status
FROM
	t_e4s_bu_activities
WHERE ACTIon_TYPE = '8' and audit_status='1' 
		'''
		if last_update: sql += "and LAST_UPDATED_DATE>= '" + last_update + "' "
		sql += "limit " + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['activity_id']: continue
			data['activity_id'] = row['activity_id']
			data['type'] = row['type']
			if data['type']=='' or data['type']==None: data['type']='1'
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			if not row['title']: continue
			if u'测试' in row['title']: continue
			data['title'] = row['title']
			data['title_short'] = row['title_short']
			if not row['pic'] or row['pic']==u' ': continue
			if not row['pic'] or row['pic']==u'' or row['pic']==u'无': continue
			data['pic'] = buildurl(row['pic'])
			if not row['start_date']: continue
			data['start_date'] = row['start_date']
			if not row['end_date']: continue
			data['end_date'] = row['end_date']
			data['phone'] = row['phone']
			if row['activity_discount']: data['activity_discount'] = int(row['activity_discount']) * 100
			data['activity_address'] = row['activity_address']
			data['detail'] = row['detail']
			tmp = "SELECT POLICY_TITILE FROM t_e4s_bu_activities_policy_rel WHERE activities_id='"+str(row['activity_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp: data['package'] = tmp
			tmp = "SELECT OBJECT_ID FROM activity_object_rel WHERE activity_id='"+str(row['activity_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp: data['car_model'] = tmp
			data['activity_status'] = row['activity_status']

			ret = item.AddActivity(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['type'], data['dealer_id'], data['title']

def InsertPromotion(last_update):
	print '\n[INFO]', '开始更新车型促销活动数据...'

	rows = True
	pos = 0
	index = 0
	item = Activities()
	while rows:
		sql = '''
SELECT
	activities_id activity_id,
	activities_type type,
	dlr_id dealer_id,
	active_title title,
	short_active_title title_short,
	home_picture pic,
	action_begin_date start_date,
	action_end_date end_date,
	contact_phone phone,
	'' activity_discount,
	address activity_address,
	active_desc detail,
	'' package,
	'' car_model,
	audit_status activity_status,
	last_updated_date
FROM
	t_e4s_bu_activities
WHERE ACTIon_TYPE = '10' and audit_status='1' and LAST_UPDATED_DATE>=
		'''
		sql += "'" + last_update + "' limit " + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['activity_id']: continue
			data['promotions_id'] = row['activity_id']
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			tmp = "SELECT OBJECT_ID FROM activity_object_rel WHERE TYPE = '1' AND ACTIVITY_ID = '"+row['activity_id']+"'"
			tmp = rec2json(tmp)
			if not tmp: continue
			tmp = json.loads(tmp)
			data['series_id'] = tmp[0]['OBJECT_ID']
			if not row['title']: continue
			data['title'] = row['title']
			data['title_short'] = row['title_short']
			#data['pic'] = buildurl(row['pic'])
			#data['price'] = row['price']	# 暂时先从报价表读取
			#data['dealer_price'] = row['dealer_price']
			if not row['start_date']: continue
			data['start_time'] = row['start_date']
			data['end_time'] = row['end_date']
			data['status'] = row['activity_status']

			ret = item.AddPromotion(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['title'], row['last_updated_date']

def InsertFinancial():
	print '\n[INFO]', '开始更新金融产品数据...'

	rows = True
	pos = 0
	index = 0
	item = Financial()
	while rows:
		sql = '''
SELECT
	a.id financial_id,
	a.financial_corp_id brand_id,
	a.financial_product_name `name`,
	a.FIRST_PAY_PERCENT initial,
	'' apply_requirement,
	'' apply_document,
	'' package,
	'0' repayment_mode,
	a.pass_percent pass_rate,
	0 period_rate,
	a.REPAYMENT_TYPE type
FROM
	t_e4s_db_financial_product a WHERE a.IS_ENABLE = '1'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['financial_id']: continue
			data['financial_id'] = row['financial_id']
			if not row['brand_id']: continue
			data['brand_id'] = row['brand_id']
			if not row['name']: continue
			data['name'] = row['name']
			data['initial'] = row['initial']
			tmp = "SELECT corp_condition FROM t_e4s_db_financial_condition WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['apply_requirement'] = tmp
			tmp = "SELECT material FROM t_e4s_db_financial_material WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['apply_document'] = tmp
			tmp = "SELECT finacial_product_package FROM t_e4s_db_financial_pro_package WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp and tmp != 'None': data['package'] = tmp
			data['repayment_mode'] = int(row['repayment_mode']) + 1
			data['pass_rate'] = row['pass_rate']
			tmp = "SELECT sku_item, sku_rate FROM t_e4s_db_financial_pro_sku WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = json.loads(rec2json(tmp))
			if not tmp: continue
			data['period_rate'] = json.JSONEncoder().encode(calc(int(row['initial']), tmp, row['financial_id'], 1))
			data['type'] = row['type']

			ret = item.AddFinancial(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['name']

def InsertPrice():
	print '\n[INFO]', '开始更新经销商车型报价数据...'

	rows = True
	pos = 0
	index = 0
	item = Dealers()
	while rows:
		sql = '''
SELECT
	ID price_id,
	CAR_TYPE model_id,
	CAR_SERIES series_id,
	STORE_ID dealer_id,
	PUBLIC_OFFER_PRICE dealer_price,
	LAST_UPDATED_DATE last_date
FROM
	t_e4s_bu_offer_price '''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['price_id'] = row['price_id']
			if not row['model_id']: continue
			data['model_id'] = row['model_id']
			if not row['series_id']: continue
			data['series_id'] = row['series_id']
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			if not row['dealer_price']: continue
			data['dealer_price'] = int(row['dealer_price']) * 100
			data['last_date'] = row['last_date']

			ret = item.AddPrice(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['model_id'], data['dealer_price']

def FinancialSeries():
	print '\n[INFO]', '开始更新经销商车系关联数据...'

	rows = True
	pos = 0
	index = 0
	item = Financial()
	while rows:
		sql = '''
SELECT
	a.id financial_id,
	s.car_series_id series_id
FROM
	t_e4s_db_financial_series s,
	t_e4s_db_financial_product a
WHERE
	a.id = s.financial_id '''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['financial_id']: continue
			data['financial_id'] = row['financial_id']
			if not row['series_id']: continue
			data['series_id'] = row['series_id']

			ret = item.FinancialSeries(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['financial_id'], data['series_id']

def FinancialDealer():
	print '\n[INFO]', '开始更新经销商车型报价数据...'

	rows = True
	pos = 0
	index = 0
	item = Financial()
	while rows:
		sql = '''
SELECT
	a.id financial_id,
	r.dlr_code dealer_id,
	s.CITY_ID city
FROM
	t_e4s_db_financial_dlr r,
	t_e4s_db_financial_product a,
	store s
WHERE
	a.id = r.financial_id
AND s.STORE_ID = r.dlr_code AND s.CITY_ID != '0'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['financial_id']: continue
			data['financial_id'] = row['financial_id']
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			if not row['city']: continue
			data['city'] = row['city']

			ret = item.FinancialDealer(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['financial_id'], data['dealer_id'], data['city'], ret

def FinancialBrand():
	print '\n[INFO]', '开始更新金融机构数据...'

	rows = True
	pos = 0
	index = 0
	item = Financial()
	while rows:
		sql = '''
SELECT
	ID brand_id,
	CORP_NAME `name`,
	CORP_LOGO logo,
	LOAN_HOUR loan_time,
	IS_ONLINE_AUDIT online_approval,
	'' features,
	'' apply_requirement,
	SUCCESS_NUM apply_person
FROM
	t_e4s_db_financial_corp WHERE IS_ENABLE='1'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['brand_id']: continue
			data['brand_id'] = row['brand_id']
			if not row['name']: continue
			data['name'] = row['name']
			data['logo'] = buildurl(row['logo'])
			data['loan_time'] = row['loan_time']
			data['online_approval'] = row['online_approval']
			tmp = "SELECT FEATURE FROM t_e4s_db_financial_corp_feature WHERE FINACIAL_CORP_ID='"+str(row['brand_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['features'] = tmp
			tmp = "SELECT CORP_CONDITION FROM t_e4s_db_financial_corp_condition WHERE FINACIAL_CORP_ID='"+str(row['brand_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['apply_requirement'] = tmp
			data['apply_person'] = row['apply_person']

			ret = item.FinancialBrand(data)
			print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['brand_id'], data['name']

def SMSMinutely():
	print '\n[INFO]', '开始定时发送短信...'

	item = Debug()
	ret = item.sms(url, data)
	print index, int(ret['error'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', data['brand_id'], data['name']

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	if DEBUG: db = connect(host='', db='', user='', passwd='')
	else: db = connect(host='', db='', user='', passwd='')

	# InsertSeries()
	# InsertModel()
	# InsertActivity('2015-10-27 11:00:00')
	# InsertPromotion('2015-12-30 00:00:00')
	# InsertDealer()
	# InsertFinancial()
	# FinancialBrand()
	# FinancialSeries()
	# FinancialDealer()
	# DealerSeries()
	# InsertPrice()
	# SMSMinutely()
