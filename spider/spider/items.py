# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class SpiderItem(scrapy.Item):
    dealer = scrapy.Field()
    brand  = scrapy.Field()
    saleto  = scrapy.Field()
    phone  = scrapy.Field()
    address= scrapy.Field()
