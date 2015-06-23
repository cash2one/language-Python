# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class AutohomePriceItem(scrapy.Item):
    dealer = scrapy.Field()
    dealerid = scrapy.Field()
    brand = scrapy.Field()
    brandid = scrapy.Field()
    model = scrapy.Field()
    modelid = scrapy.Field()
    oprice = scrapy.Field()
    price = scrapy.Field()

class AutohomeArticleItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    series_name = scrapy.Field()
    brand_id = scrapy.Field()
