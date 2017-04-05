# -*- coding: utf-8 -*-
import scrapy
import re
import json
from scrapy.selector import Selector
from scrapy.http import Request
from simplemysql import SimpleMysql

def regx(patern, string):
    regx = re.findall(re.compile(patern, re.IGNORECASE), string.strip())
    return regx and regx[0] or None

_db = SimpleMysql(host='127.0.0.1', db='autohome', user='root', passwd='root', autocommit=True)

class CarSpider(scrapy.Spider):
    name = "car"
    allowed_domains = ['www.autohome.com.cn', 'k.autohome.com.cn']
    start_urls = [
        # 'http://www.autohome.com.cn/grade/carhtml/R.html',
        'http://www.autohome.com.cn/grade/carhtml/'+C+'.html' for C in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    ]

    def parse(self, response):
        # yield Request('http://k.autohome.com.cn/121/', self.parse_koubei)
        # return
        sel = Selector(response)
        brands = sel.xpath('//dl')
        item = {}
        for brand in brands:
            brand_name = brand.xpath('dt/div/a/text()').extract()
            item['brand_name'] = brand_name and brand_name[0] or None

            tmp = brand.xpath('dt/div/a/@href').extract()
            tmp = tmp and tmp[0] or None
            item['brand_id'] = regx(r'-\d+\.', tmp).lstrip('-').rstrip('.')

            groups = brand.xpath('dd')
            for group in groups:
                serieses = group.xpath('ul/li/h4')
                for series in serieses:
                    series_name = series.xpath('a/text()').extract()
                    item['series_name'] = series_name and series_name[0] or None

                    tmp = series.xpath('a/@href').extract()
                    tmp = tmp and tmp[0] or None
                    item['series_id'] = regx(r'\/\d+\/', tmp).strip('/')

                    # print json.dumps(item, ensure_ascii=False) # insert
                    _db.insertOrUpdate(table='series', data=item, keys=('series_id'))

                    yield Request('http://www.autohome.com.cn/'+item['series_id']+'/', self.parse_factory)
                    yield Request('http://www.autohome.com.cn/'+item['series_id']+'/', self.parse_models)
                    yield Request('http://www.autohome.com.cn/'+item['series_id']+'/sale.html', self.parse_unsalemodels)
                    yield Request('http://k.autohome.com.cn/'+item['series_id']+'/', self.parse_koubei)
                    yield Request('http://k.autohome.com.cn/'+item['series_id']+'/stopselling/', self.parse_koubei)

    def parse_factory(self, response):
        sel = Selector(response)
        factory = sel.xpath('//div[@class="subnav-title-name"]/a/text()').extract()
        series_id = regx(r'\d+', response.url)
        factory_name = factory and factory[0].split('-')[0] or None
        _db.update(table='series', data={'factory_name': factory_name}, where=("series_id=%s", [series_id]))

    def parse_models(self, response):
        sel = Selector(response)

        model = {}
        model['series_id'] = regx(r'\d+', response.url)

        lists = sel.xpath('//ul[@class="interval01-list"]/li')
        for lst in lists:
            tmp = lst.xpath('div[@class="interval01-list-cars"]/div/p[1]/a/text()').extract()
            model['model_name'] = tmp and tmp[0] or None

            tmp = lst.xpath('div[@class="interval01-list-cars"]/div/p[1]/a/@href').extract()
            tmp = tmp and tmp[0] or None
            model['model_id'] = regx(r'\/\d+\/', tmp).strip('/')

            tmp = lst.xpath('div[@class="interval01-list-guidance"]').extract()
            model['model_price'] = tmp and regx(ur'\d+.\d+万', tmp[0]).rstrip(u'万') or None

            # print json.dumps(model, ensure_ascii=False)
            _db.insertOrUpdate(table='models', data=model, keys=('model_id'))

    def parse_unsalemodels(self, response):
        sel = Selector(response)

        model = {}
        model['series_id'] = regx(r'\d+', response.url)

        items = sel.xpath('//div[@class="tabwrap"]/div/table/tr')
        for item in items:
            tmp = item.xpath('td[@class="name_d"]/a/text()').extract()
            model['model_name'] = tmp and tmp[0] or None

            tmp = item.xpath('td[@class="name_d"]/a/@href').extract()
            model['model_id'] = tmp and regx(r'\d+', tmp[0]) or None

            tmp = item.xpath('td[@class="price_d"][1]/text()').extract()
            model['model_price'] = tmp and tmp[0].rstrip(u'万') or None

            # print json.dumps(model, ensure_ascii=False)
            _db.insertOrUpdate(table='models', data=model, keys=('model_id'))

    def parse_koubei(self, response):
        sel = Selector(response)

        kou = {}
        kou['series_id'] = regx(r'\d+', response.url)

        groups = sel.xpath('//div[@class="mouthcon"]')
        for group in groups:
            left = group.xpath('div/div[@class="mouthcon-cont-left"]/div[@class="choose-con mt-10"]')
            right = group.xpath('div/div[@class="mouthcon-cont-right commentParentBox"]/div[@class="mouth-main"]/div[@class="mouth-item"]/div[@class="cont-title fn-clear"]/div')

            tmp = left.xpath('dl[@class="choose-dl"][2]/dd/text()').extract()
            kou['location'] = tmp and tmp[0].strip() or None

            tmp = left.xpath('dl[@class="choose-dl"][3]/dd/a/@data-val').extract()
            kou['from_dealer_id'] = tmp and tmp[0].split(',')[0] or None
            kou['model_id'] = tmp and tmp[0].split(',')[1] or None

            tmp = left.xpath('dl[@class="choose-dl"][4]/dd/text()').extract()
            kou['ondate'] = tmp and tmp[0].strip() or None

            tmp = left.xpath('dl[@class="choose-dl"][5]/dd/text()').extract()
            kou['onprice'] = tmp and tmp[0].strip() or None

            tmp = left.xpath('dl[@class="choose-dl"][6]/dd/p[1]/text()').extract()
            kou['consumption'] = tmp and tmp[0].strip() or None

            tmp = right.xpath('b/a/@href').extract()
            kou['kid'] = tmp and regx(r'_\d+_', tmp[0]).strip('_') or None

            tmp = right.xpath('a/text()').extract()
            kou['ktitle'] = tmp and tmp[0] or None

            # print json.dumps(kou, ensure_ascii=False)
            if not kou['kid']: continue
            _db.insertOrUpdate(table='koubei', data=kou, keys=('kid'))

            next_url = sel.xpath('//a[@class="page-item-next"]/@href').extract()
            if next_url: yield Request('http://k.autohome.com.cn' + next_url[0], self.parse_koubei)
