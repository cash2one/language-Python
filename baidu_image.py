#!/usr/bin/env python
# coding: utf-8

import requests, time
import simplejson as json

headers = {}
headers['Cookie'] = 'BDqhfp=%E8%87%AA%E6%8B%8D%26%260-10-1undefined%26%265478%26%2610; BDUSS=ViM1U3UTRiTjVwdW5CdlBrNkxONFV2clJhZkcwbVhhNWdDZFhiNUFBWXZPeHBYQVFBQUFBJCQAAAAAAAAAAAEAAAA2YzYAdG9tdHpoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC-u8lYvrvJWa0; BAIDUID=0FC3E7B0E3CE93AC80B1D3F6EE16011E:FG=1; BIDUPSID=0FC3E7B0E3CE93AC80B1D3F6EE16011E; PSTM=1467040612; pgv_pvi=2950408192; cflag=15%3A3; MCITY=-257%3A; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; firstShowTip=1; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm'
headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.8 Safari/537.36'

def download(url):
	if not url or len(url) < 10: return -1
	img_name = str(time.time()) + '.' + url.split('.')[-1]
	with open('img/' + img_name, 'wb') as f:
		f.write(requests.get(url, headers=headers).content)
	print u'\t得到文件：', img_name
	return 0

if __name__ == '__main__':
	step = 30
	url0 = u'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&word=自拍&face=1'
	loop = 0
	while loop >= 0:
		url = url0 + '&pn=%d&rn=%d' % (step * loop, step)
		data = None
		print u'开始下载：', url
		try:
			data = json.loads(requests.get(url, headers=headers).content, encoding='utf-8')
			for pic in data['data']:
				if pic.has_key('hoverURL'):
					if download(pic['hoverURL']) < 0: break
				break
			loop += 1
		except Exception, e:
			print e, data
			break
