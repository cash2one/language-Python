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

class AutohomeAllPriceItem(scrapy.Item):
    city = scrapy.Field()
    dealer = scrapy.Field()
    dealerid = scrapy.Field()
    brand = scrapy.Field()
    brandid = scrapy.Field()
    model = scrapy.Field()
    modelid = scrapy.Field()
    oprice = scrapy.Field()
    price = scrapy.Field()
    manu = scrapy.Field()

class AutohomePromotionItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    prices = scrapy.Field()
    series_name = scrapy.Field()
    series_id = scrapy.Field()
    dealer = scrapy.Field()
    dealerid = scrapy.Field()
    datefrom = scrapy.Field()
    dateto = scrapy.Field()

class AutohomeAllPromotionItem(scrapy.Item):
    city = scrapy.Field()
    brand = scrapy.Field()
    pageurl = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    prices = scrapy.Field()
    series_name = scrapy.Field()
    series_id = scrapy.Field()
    brand_id = scrapy.Field()
    dealer = scrapy.Field()
    dealerid = scrapy.Field()
    datefrom = scrapy.Field()
    dateto = scrapy.Field()
