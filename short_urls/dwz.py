# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, json

def post(api, data):
	if not data or not api: return

	try:
		request = urllib2.Request(api, urllib.urlencode(data))
		print '[INFO]', api, '[POST]', request.data,
		response = urllib2.urlopen(request).read()
		return json.loads(response)
	except Exception, e:
		return 'ERROR:', e, data,

if __name__ == '__main__':
	data = {}
	data['url'] = 'http://nissan.ie9.org/'
	data['alias'] = 'nissan_ie9'
	ret = post('http://dwz.cn/create.php', data)
	print int(ret['status'])==0 and '\033[32m成功\033[0m' or '\033[31m失败\033[0m', ret['err_msg']
