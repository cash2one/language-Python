#!/usr/bin/env python
# coding: utf-8

import sys, logging, json, time
import requests

def get_stream(station, page_no = 1):
	url = u'http://map.baidu.com/?newmap=1&qt=nb&wd=住宅区&pn=' + str(page_no) + '&l=16&b=' + station + '&t=' + str(int(time.mktime(time.localtime())))
	logging.info(url)
	j = json.loads(requests.get(url).text)
	if 'content' in j: return j['content']
	return None

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.INFO, format='%(message)s', filename='baidu_house.log', filemode='a')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	sts = [
		{'name': '凤凰新村', 'poi': '(12606740.91,2626491.4;12610212.91,2628035.4)'},
		{'name': '沙园', 'poi': '(12608017.99,2625791.71;12611489.99,2627335.71)'},
		{'name': '宝岗大道', 'poi': '(12609040.98,2625489.18;12612512.98,2627033.18)'},
		{'name': '昌岗', 'poi': '(12609836.95,2626062.78;12613308.95,2627606.78)'},
		{'name': '晓港', 'poi': '(12610398.01,2626351.35;12613870.01,2627895.35)'},
		{'name': '中大', 'poi': '(12611646.72,2626225.98;12615118.72,2627769.98)'},
		{'name': '鹭江', 'poi': '(12613338.23,2626594.34;12616810.23,2628138.34)'},
		{'name': '客村', 'poi': '(12614714.1,2626684.12;12618186.1,2628228.12)'},
		{'name': '赤岗', 'poi': '(12616322.2,2626683.33;12619794.2,2628227.33)'},
		{'name': '磨碟沙', 'poi': '(12617042.64,2626947.07;12620514.64,2628491.07)'},
		{'name': '新港东', 'poi': '(12618786.72,2626968.89;12622258.72,2628512.89)'},
		{'name': '琶洲', 'poi': '(12619841.03,2626971.86;12623313.03,2628515.86)'},
		{'name': '万胜围', 'poi': '(12621848.05,2626906.75;12625320.05,2628450.75)'},
	]

	logging.info('地铁站,名称,地址,百度经度,百度纬度,区域,开发商,类型,特色,均价,波动,评分,物业公司,物业费,年限,租金,搜房网链接,搜房网房源数,搜房网均价,安居客链接,安居客房源数,安居客均价')

	for st in sts:
		pn = 1
		rs = True
		while rs:
			rs = get_stream(st['poi'], pn)
			if not rs: break
			pn += 1

			for r in rs:
				tmp = []
				tmp.append('name' in st and st['name'] or '')
				tmp.append('name' in r  and r['name']  or '')
				tmp.append('addr' in r and r['addr'] or '')
				tmp.append('navi_x' in r and r['navi_x'] or '')
				tmp.append('navi_y' in r and r['navi_y'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'aoi' in r['ext']['detail_info'] and r['ext']['detail_info']['aoi'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'developers' in r['ext']['detail_info'] and r['ext']['detail_info']['developers'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'house_type' in r['ext']['detail_info'] and r['ext']['detail_info']['house_type'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'new_tag' in r['ext']['detail_info'] and r['ext']['detail_info']['new_tag'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'price' in r['ext']['detail_info'] and r['ext']['detail_info']['price'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'price_change_rate' in r['ext']['detail_info'] and r['ext']['detail_info']['price_change_rate'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'overall_rating' in r['ext']['detail_info'] and r['ext']['detail_info']['overall_rating'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'property_company' in r['ext']['detail_info'] and r['ext']['detail_info']['property_company'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'property_management_fee' in r['ext']['detail_info'] and r['ext']['detail_info']['property_management_fee'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'property_right' in r['ext']['detail_info'] and r['ext']['detail_info']['property_right'] or '')
				tmp.append('ext' in r and 'detail_info' in r['ext'] and 'rent_price' in r['ext']['detail_info'] and r['ext']['detail_info']['rent_price'] or '')

				p = ['', '', '', '', '', '']
				if 'ext' in r and 'detail_info' in r['ext'] and 'sales_info' in r['ext']['detail_info']:
					for info in r['ext']['detail_info']['sales_info']:
						if info['src'] == 'soufang':
							p[0] = info['url'] and info['url'] or ''
							p[1] = info['onsale_num'] and info['onsale_num'] or ''
							p[2] = info['selling_price'] and info['selling_price'] or ''
						elif info['src'] == 'anjuke':
							p[3] = info['url'] and info['url'] or ''
							p[4] = info['onsale_num'] and info['onsale_num'] or ''
							p[5] = info['selling_price'] and info['selling_price'] or ''
				else: continue

				tmp += p
				try:
					logging.info(','.join(tmp))
				except Exception, e:
					print tmp
					continue

			time.sleep(1)
			if pn > 10: rs = False
