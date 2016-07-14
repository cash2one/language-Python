#!/usr/bin/env python
# coding: utf-8

import requests, json, os, sys
from PIL import Image, ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

if __name__ == '__main__':
	url = 'http://m.htxq.net/servlet/SysVphServlet?action=getVphList&currentPageIndex=0&pageSize=500'
	items = json.loads(requests.get(url).text)['result']
	for item in items:
		print 'crawling', item['fnArticleTitle'], '...'
		file_type = '.' + item['img1'].split('.')[-1]
		file_old_name = item['fnArticleId'] + file_type
		file_new_name = item['fnArticleTitle'] + '_thumb' + file_type
		with open(file_old_name, 'wb') as stream:
			stream.write(requests.get(item['img1']).content)
			Image.open(file_old_name).resize((200, 300), Image.ANTIALIAS).save(file_new_name)
			os.remove(file_old_name)
