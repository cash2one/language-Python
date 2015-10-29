# -*- coding: utf-8 -*-
#!/usr/bin/env python

import sys, json, urllib, logging
from simplemysql import SimpleMysql

db_chebaba = None
chebaba_host = ''
chebaba_user = ''
chebaba_pass = ''
chebaba_base = ''

db_cbb = None
cbb_host = '127.0.0.1'
cbb_user = ''
cbb_pass = ''
cbb_base = ''

STEP = 50

def connect(host, db, user, passwd):
	logging.info('Connecting to host ' + host + '...')
	tmp = SimpleMysql(host=host, db=db, user=user, passwd=passwd)
	if tmp: logging.info('Connected to host ' + host + '.')
	return tmp

def doSave(table, data, keys = None):
	return db_cbb.insertOrUpdate(table, data, keys)

def doSave1(table, data):
	return db_cbb.insert(table, data)

def rec2json(sql):
	if not sql: return None

	try:
		rows = db_chebaba.query(sql).fetchall()
		if not rows: return
		result = []
		for row in rows:
			data = {}
			for col in row:
				data[col] = row[col]
			result.append(data)
		if result: return result
	except Exception, e:
		logging.error(e)

def rec2jsonlist(sql):
	if not sql: return None

	try:
		rows = db_chebaba.query(sql).fetchall()
		if not rows: return
		result = []
		for row in rows:
			tmp = row.values()[0].strip()
			if tmp: result.append(tmp)
		if result: return result#json.JSONEncoder().encode(result)
	except Exception, e:
		logging.error(e)

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
	table = 'car_series'
	keys = ['series_id']
	logging.info('>>> Starting to update ' + table + '...')

	rows = True
	pos = 0
	index = 0
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
	s.START_GUIDEPRICE price_min,
	s.END_GUIDEPRICE price_max,
	s.IS_ENABLE isactive
FROM
	t_e4s_db_ve_car_series s
WHERE
	s.IS_ENABLE='1' 
	'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
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
			tmp_result = rec2json(tmp)
			data['discount_min'] = tmp_result[0]['max_price']
			data['discount_max_pid'] = tmp_result[0]['discount_min_pid']

			tmp = "SELECT MIN(PUBLIC_OFFER_PRICE) min_price, CAR_TYPE discount_max_pid FROM t_e4s_bu_offer_price t LEFT JOIN car_type c ON t.car_type = c.UUID WHERE c.CAR_SERIES_ID = '" + data['series_id'] + "';"
			tmp_result = rec2json(tmp)
			data['discount_max'] = tmp_result[0]['min_price']
			data['discount_min_pid'] = tmp_result[0]['discount_max_pid']

			data['price_min'] = int(row['price_min']) * 100
			data['price_max'] = int(row['price_max']) * 100
			data['isactive'] = row['isactive']

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['name'] + ', ' + data['en_name'])

def InsertModel():
	table = 'car_model'
	keys = ['model_id']
	logging.info('>>> Starting to update ' + table + '...')
	# 特色参数：203 205 206，搜索表名：proper，两个表有关联
	rows = True
	pos = 0
	index = 0

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
	car_type 
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['series_id'] = row['series_id']
			data['model_id'] = row['model_id']
			if not row['model_name']: continue
			data['model_name'] = row['model_name']
			if not row['model_price']: row['model_price'] = 0
			data['model_price'] = int(row['model_price']) * 100
			data['price_Discount'] = 0
			tmp = "SELECT a.CAR_COLOR_CODE color_name, b.RGB ascii_code FROM t_e4s_db_car_series_color a LEFT JOIN t_e4s_base_color b ON a.CAR_COLOR_CODE = b.`NAME` WHERE CAR_SERIES_ID='"+row['series_id']+"'"
			tmp = rec2json(tmp)
			if tmp: data['model_color'] = json.JSONEncoder().encode(tmp)
			tmp = '''
SELECT DISTINCT PROPERTY_VALUE FROM t_e4s_bu_car_type_property
WHERE PROPERTY_ID IN ( SELECT id FROM t_e4s_bu_property_template WHERE `name` IN ('车型特色参数I', '车型特色参数II', '车型特色参数III') )
AND IS_ENABLE = '1' AND CAR_TYPE_ID=
			'''
			tmp += "'" + row['model_id'] + "' LIMIT 3"
			tmp = rec2jsonlist(tmp)
			if tmp: data['model_attrib'] = json.JSONEncoder().encode(tmp)
			data['model_status'] = row['model_status']
			data['all_money'] = int(row['all_money']) * 100
			data['tax_and_insurance'] = int(row['tax_and_insurance']) * 100
			data['purchase_tax'] = int(row['purchase_tax']) * 100
			data['vehicle_tax'] = int(row['vehicle_tax']) * 100
			data['traffic_tax'] = int(row['traffic_tax']) * 100
			data['commerce_insurance'] = int(row['commerce_insurance']) * 100

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['model_name'] + ', ' + str(data['model_price']))

def InsertDealer():
	table = 'dealer_base'
	keys = ['dealer_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

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
		rows = db_chebaba.query(sql).fetchall()
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
			data['after_score'] = float(row['after_score'])
			data['after_score_rate'] = float(row['after_score_rate'])
			data['pre_score'] = float(row['pre_score'])
			data['pre_score_rate'] = float(row['pre_score_rate'])
			data['dealer_status'] = row['dealer_status']

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['dealer_id'] + ', ' + str(data['dealer_name_short']))

def DealerSeries():
	table = 'dealer_series'
	keys = ['dealer_id', 'series_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

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
		rows = db_chebaba.query(sql).fetchall()
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
			tmp = rec2json(tmp)
			if not tmp: continue
			data['lowest_price'] = 0
			if tmp[0]['min_price']: data['lowest_price'] = int(tmp[0]['min_price']) * 100
			if data['lowest_price'] == 0: continue

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['dealer_id'] + ', ' + str(data['series_id']))

def InsertActivity(last_update = None):
	table = 'dealer_activity'
	keys = ['activity_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	activities_id activity_id,
	activities_type activity_type,
	dlr_id dealer_id,
	active_title title,
	short_active_title title_short,
	home_picture picture,
	action_begin_date start_date,
	action_end_date end_date,
	contact_phone phone,
	address activity_address,
	active_desc detail,
	audit_status activity_status,
	CREATED_DATE createtime,
	LAST_UPDATED_DATE updatetime
FROM
	t_e4s_bu_activities
WHERE ACTIon_TYPE = '8' and audit_status='1' and LAST_UPDATED_DATE>=
		'''
		sql += "'" + last_update + "' limit " + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['activity_id']: continue
			data['activity_id'] = row['activity_id']
			data['activity_type'] = row['activity_type']
			if data['activity_type']=='' or data['activity_type']==None: data['activity_type']='1'
			if not row['dealer_id']: continue
			data['dealer_id'] = row['dealer_id']
			if not row['title']: continue
			if u'测试' in row['title']: continue
			data['title'] = row['title']
			data['title_short'] = row['title_short']
			if not row['picture'] or row['picture']==u' ' or row['picture']==u'' or row['picture']==u'无': continue
			data['picture'] = buildurl(row['picture'])
			if not row['start_date']: continue
			data['start_date'] = row['start_date']
			if not row['end_date']: continue
			data['end_date'] = row['end_date']
			data['phone'] = row['phone']
			data['activity_address'] = row['activity_address']
			data['detail'] = row['detail']
			tmp = "SELECT POLICY_TITILE FROM t_e4s_bu_activities_policy_rel WHERE activities_id='"+str(row['activity_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp: data['packages'] = json.JSONEncoder().encode(tmp)
			tmp = "SELECT OBJECT_ID FROM activity_object_rel WHERE activity_id='"+str(row['activity_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp: data['car_model'] = json.JSONEncoder().encode(tmp)
			data['activity_status'] = row['activity_status']
			tmp = "SELECT CITY_ID FROM store WHERE STORE_ID='" + data['dealer_id'] + "';"
			data['city_id'] = rec2jsonlist(tmp)[0]
			data['createtime'] = str(row['createtime'])
			data['updatetime'] = str(row['updatetime'])
			data['ext_info'] = ''

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['activity_id'] + ', ' + data['title'])

def InsertPromotion(last_update = None):
	table = 'promotions'
	keys = ['promotions_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	ACTIVITIES_ID promotions_id,
	DLR_ID dealer_id,
	ACTIVE_TITLE title,
	SHORT_ACTIVE_TITLE title_short,
	ACTIVE_DESC content,
	ACTION_BEGIN_DATE start_time,
	ACTION_END_DATE end_time
FROM
	t_e4s_bu_activities
WHERE ACTIon_TYPE = '10' and audit_status='1' and LAST_UPDATED_DATE>=
		'''
		sql += "'" + last_update + "' limit " + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['promotions_id'] = row['promotions_id']
			data['dealer_id'] = row['dealer_id']
			data['title'] = row['title']
			data['title_short'] = row['title_short']
			data['content'] = row['content']
			data['start_time'] = row['start_time']
			data['end_time'] = row['end_time']
			tmp = "SELECT OBJECT_ID FROM activity_object_rel WHERE activity_id='"+row['promotions_id']+"'"
			data['series_id'] = rec2jsonlist(tmp)[0]

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['promotions_id'] + ', ' + data['title'])

def InsertFinancial():
	table = 'financial'
	keys = ['financial_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	a.id financial_id,
	a.financial_corp_id corp_id,
	a.financial_product_name finanicial_name,
	a.FIRST_PAY_PERCENT initial,
	'' apply_requirement,
	'' apply_document,
	'' packages,
	'0' repayment_mode,
	a.pass_percent pass_rate,
	0 period_rate
FROM
	t_e4s_db_financial_product a WHERE a.IS_ENABLE = '1'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			if not row['financial_id']: continue
			data['financial_id'] = row['financial_id']
			if not row['corp_id']: continue
			data['corp_id'] = row['corp_id']
			if not row['finanicial_name']: continue
			data['finanicial_name'] = row['finanicial_name']
			data['initial'] = row['initial']
			tmp = "SELECT corp_condition FROM t_e4s_db_financial_condition WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['apply_requirement'] = json.JSONEncoder().encode(tmp)
			tmp = "SELECT material FROM t_e4s_db_financial_material WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if not tmp: continue
			data['apply_document'] = json.JSONEncoder().encode(tmp)
			tmp = "SELECT finacial_product_package FROM t_e4s_db_financial_pro_package WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2jsonlist(tmp)
			if tmp and tmp != 'None': data['packages'] = tmp
			data['repayment_mode'] = int(row['repayment_mode']) + 1
			data['pass_rate'] = row['pass_rate']
			tmp = "SELECT sku_item, sku_rate FROM t_e4s_db_financial_pro_sku WHERE FINACIAL_PRODUCT_ID='"+str(row['financial_id'])+"'"
			tmp = rec2json(tmp)
			if not tmp: continue
			data['period_rate'] = json.JSONEncoder().encode(calc(int(row['initial']), tmp, row['financial_id'], 1))

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + str(data['financial_id']) + ', ' + data['finanicial_name'])

def InsertPrice():
	table = 'dealer_price'
	keys = ['dealer_id', 'model_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	CAR_TYPE model_id,
	CAR_SERIES series_id,
	STORE_ID dealer_id,
	PUBLIC_OFFER_PRICE dealer_price,
	LAST_UPDATED_DATE last_date
FROM
	t_e4s_bu_offer_price '''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['model_id'] = row['model_id']
			data['series_id'] = row['series_id']
			data['dealer_id'] = row['dealer_id']
			data['dealer_price'] = int(row['dealer_price']) * 100
			data['last_date'] = row['last_date']

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + data['dealer_id'] + ', ' + data['model_id'])

def FinancialSeries():
	table = 'financial_series'
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	a.id financial_id,
	s.car_series_id series_id
FROM
	t_e4s_db_financial_series s
LEFT JOIN t_e4s_db_financial_product a ON a.id = s.financial_id 
	'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['financial_id'] = row['financial_id']
			data['series_id'] = row['series_id']

			doSave1(table, data)
			logging.info(str(index) + ', ' + str(data['financial_id']) + ', ' + data['series_id'])

def FinancialDealer():
	table = 'financial_dealer'
	keys = ['dealer_id', 'financial_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	a.id financial_id,
	r.dlr_code dealer_id,
	s.CITY_ID city_id
FROM
	t_e4s_db_financial_dlr r,
	t_e4s_db_financial_product a,
	store s
WHERE
	a.id = r.financial_id AND s.STORE_ID = r.dlr_code AND s.CITY_ID != '0'
		'''
		sql += 'limit ' + str(pos) + ', ' + str(STEP)
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['financial_id'] = row['financial_id']
			data['dealer_id'] = row['dealer_id']
			data['city_id'] = row['city_id']

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + str(data['financial_id']) + ', ' + data['dealer_id'])

def FinancialBrand():
	table = 'financial_brand'
	keys = ['corp_id']
	logging.info('>>> Starting to update ' + table + '...')
	rows = True
	pos = 0
	index = 0

	while rows:
		sql = '''
SELECT
	ID corp_id,
	CORP_NAME corp_name,
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
		rows = db_chebaba.query(sql).fetchall()
		if not rows: break
		pos += STEP
		for row in rows:
			index += 1
			data = {}
			data['corp_id'] = row['corp_id']
			data['corp_name'] = row['corp_name']
			data['logo'] = buildurl(row['logo'])
			data['loan_time'] = row['loan_time']
			data['online_approval'] = row['online_approval']
			tmp = "SELECT FEATURE FROM t_e4s_db_financial_corp_feature WHERE FINACIAL_CORP_ID='"+str(row['corp_id'])+"'"
			tmp = rec2jsonlist(tmp)
			data['features'] = json.JSONEncoder().encode(tmp)
			tmp = "SELECT CORP_CONDITION FROM t_e4s_db_financial_corp_condition WHERE FINACIAL_CORP_ID='"+str(row['corp_id'])+"'"
			tmp = rec2jsonlist(tmp)
			data['apply_requirement'] = json.JSONEncoder().encode(tmp)
			data['apply_person'] = row['apply_person']

			doSave(table, data, keys)
			logging.info(str(index) + ', ' + str(data['corp_id']) + ', ' + data['corp_name'])

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s', filename='cbb.py.log', filemode='w')
	#定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	formatter = logging.Formatter('[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s')
	console.setFormatter(formatter)
	logging.getLogger('').addHandler(console)

	try:
		db_chebaba = connect(host=chebaba_host, db=chebaba_base, user=chebaba_user, passwd=chebaba_pass)
		db_cbb = connect(host=cbb_host, db=cbb_base, user=cbb_user, passwd=cbb_pass)

		if not db_chebaba or not db_cbb:
			logging.error('Database connection was failed to established.')
			return

		# InsertSeries()
		# InsertModel()
		# InsertDealer()
		# DealerSeries()
		# InsertActivity('2015-10-19 11:00:00')		# 手动增量更新
		# InsertActivity()							# 自动全量更新
		# InsertPromotion('2015-10-19 11:00:00')	# 手动增量更新
		# InsertPromotion()							# 自动全量更新
		# InsertFinancial()
		# InsertPrice()
		# FinancialSeries()
		# FinancialDealer()
		# FinancialBrand()

	except Exception, e:
		raise e
