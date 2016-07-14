#!/usr/bin/env python
# coding: utf-8

import requests, json, os

if __name__ == '__main__':
	url = 'http://...../servlet/SysVphServlet?action=getVphList&currentPageIndex=0&pageSize=500'
	items = json.loads(requests.get(url).text)['result']
	for item in items:
		os.mkdir(item['fnArticleTitle'])
		imgs = ['img1', 'img2', 'img3', 'img4', 'img5', 'img6', 'smallImg']
		print 'crawling', item['fnArticleTitle'], '...'
		for img in imgs:
			i = requests.get(item[img])
			with open(item['fnArticleTitle'] + '/' + item[img].split('/')[-1], 'wb') as stream:
				stream.write(i.content)
