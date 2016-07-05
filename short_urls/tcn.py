# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, json

def post(api, data):
	if not data or not api: return

	try:
		request = urllib2.Request(api, urllib.urlencode(data))
		response = urllib2.urlopen(request).read()
		return json.loads(response)
	except Exception, e:
		return 'ERROR:', e, data,

if __name__ == '__main__':
	data = {}
	data['url_long'] = ''
	ret = post('https://api.weibo.com/2/short_url/shorten.json', data)
	print data['url_long'], '>', ret

# 身份证：年龄，性别，地域，
