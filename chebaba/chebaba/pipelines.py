# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import urllib, urllib2
import sys, json

AUTOHOME_PRICE_URL = 'http://xxxxxx/api/price'

def doPost(url, item):
	data = {}
	data['dealer_id'] = item['dealerid']
	data['dealer_name'] = item['dealer']
	data['id'] = item['modelid']
	data['title'] = item['model']
	data['zprice'] = item['oprice']
	data['price'] = item['price']
	request = urllib2.Request(url, urllib.urlencode(data))
	response = urllib2.urlopen(request).read()
	return json.loads(response)

class AutohomePricePipeline(object):
    def process_item(self, item, spider):
    	reload(sys)
    	sys.setdefaultencoding('utf-8')

        result = doPost(AUTOHOME_PRICE_URL, item)
        print '| RESULT:', item['dealer'], item['brand'], item['model'], item['price'], '\t[', result['error'], result['msg'], ']'
