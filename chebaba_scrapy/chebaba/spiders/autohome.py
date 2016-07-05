#!/usr/bin/env python
# coding: utf-8

import sys, re, json, urllib2
from scrapy.spiders import BaseSpider
from scrapy.selector import Selector
from scrapy.http import Request
import requests, oss2
from PIL import Image

DEBUG = True

G_INCLUDE_QICHEN=True
G_INCLUDE_JINKOU=True

R_CHEXINGBAOJIA = True
R_YOUHUICUXIAO = False#True
R_ZIXUNXINXI = False#True

postCheXingBaoJia = 'http://mgt.chebaba.com/e4s-mp/api/service/offerPrice'
postYouHuiCuXiao = 'http://mgt.chebaba.com/e4s-mp/api/service/activityPublish'
postZiXunXinXi = 'http://mgt.chebaba.com/e4s-mp/api/service/dealerActivityPublish'
if DEBUG:
    postCheXingBaoJia = 'http://e4s.stg.dongfeng-nissan.com.cn/e4s-mp/api/service/offerPrice'
    postYouHuiCuXiao = 'http://e4s.stg.dongfeng-nissan.com.cn/e4s-mp/api/service/activityPublish'
    postZiXunXinXi = 'http://e4s.stg.dongfeng-nissan.com.cn/e4s-mp/api/service/dealerActivityPublish'

def re_digital(param):
    if param:
        pat = re.search(r'\d+(\.\d+)?', str(param), re.M|re.I)
        if pat:
            return pat.group()
    return -1

def filt(string, start, end):
    i = string.find(start) + len(start)
    j = string[i:].find(end)
    return string[i : i + j]

def oss_process_img(url):
    try:
        f = urllib2.urlopen(url)
        fn = url.split('/')[-1]
        with open(fn, 'wb') as flow: flow.write(f.read())
        img = Image.open(fn)
        w, h = img.size
        img.crop((0, 0, w, h - 20)).save(fn)

        auth = oss2.Auth('jYjKbRaKYyR8Nopw', '84TsXz7CFrU94zR9mqxGWNYTsG0BGA')
        tmp_bucket = 'img-chebaba'
        if DEBUG: tmp_bucket = 'test-chebaba'
        bucket = oss2.Bucket(auth, 'oss-cn-hangzhou.aliyuncs.com', tmp_bucket)
        with open(fn, 'rb') as f: bucket.put_object(fn, f)
        return 'http://%s.oss.aliyuncs.com/%s' % (tmp_bucket, fn)
    except Exception, e:
        logger.error('ProcessImageError.{}'.format(e))
        return url

class AutohomeSpider(BaseSpider):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    name = 'autohome'
    allowed_domains = ['dealer.autohome.com.cn']
    start_urls = ['http://dealer.autohome.com.cn/china/0_63_0_92_1.html']
    if G_INCLUDE_QICHEN: start_urls.append('http://dealer.autohome.com.cn/china/0_122_0_92_1.html')
    if G_INCLUDE_JINKOU: start_urls.append('http://dealer.autohome.com.cn/china/0_63_0_73_1.html')

    countCheXingBaoJia = 0
    countYouHuiCuXiao = 0
    countZiXunXinXi = 0

    def doPost(self, url, item):
        ex = ''
        try:
            kind = item.pop('type')
            ex = requests.post(url, item).text
            result = json.loads(ex)
            if result['results']:
                eval('self.count' + kind + '= self.count' + kind + '+ 1')
                self.logger.info('No.%d Spider.%s Result.%s' % (eval('self.count' + kind), kind, json.dumps(result, ensure_ascii=False)))
            else:
                self.logger.error('Spider.%s Result.%s Data.%s' % (kind, json.dumps(result, ensure_ascii=False), json.dumps(item, ensure_ascii=False)))
        except Exception, e:
            self.logger.error('ServerError.{} Result.%s Data.%s'.format(e) % (ex, json.dumps(item, ensure_ascii=False)))

    def parse(self, response):
        sel = Selector(response)
        dlrs = sel.xpath('//h3[@class="dealer-cont-title"]/a[1]/@href').extract()

        for dlr in dlrs:
            if R_CHEXINGBAOJIA:
                url = response.urljoin('price.html').replace('china', filt(dlr, '.cn/', '/'))
                yield Request(url, self.parseCheXingBaoJia)

            if R_YOUHUICUXIAO:
                url = response.urljoin('newslist_c2_s0.html').replace('china', filt(dlr, '.cn/', '/'))
                yield Request(url, self.parseYouHuiCuXiao)

            if R_ZIXUNXINXI:
                url = response.urljoin('informationList_c0_s0.html').replace('china', filt(dlr, '.cn/', '/'))
                yield Request(url, self.parseZiXunXinXi)

        if R_CHEXINGBAOJIA or R_YOUHUICUXIAO or R_ZIXUNXINXI:
            np = sel.xpath('//a[@class="page-item-next"]/@href').extract()
            if np: yield Request(response.urljoin(np[0]), self.parse)

    def parseCheXingBaoJia(self, response):
        sel = Selector(response)

        item = {}
        item['type'] = 'CheXingBaoJia'
        item['page_url'] = response.url
        item['city_name'] = sel.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['city_code'] = sel.xpath('//div[@class="breadnav"]/a[2]/@href').extract()[0].strip('/')
        item['dealer_name'] = sel.xpath('//div[@class="breadnav"]/a[3]/text()').extract()[0]
        item['dealer_id'] = sel.xpath('//div[@class="breadnav"]/a[3]/@href').extract()[0].strip('/')
        tmp_series = sel.xpath('//dl[@class="price-dl"]')
        for s in tmp_series:
            item['series_name'] = s.xpath('dt/div[@class="name"]/p/a/text()').extract()[0]
            item['series_id'] = filt(s.xpath('dt/div[@class="name"]/p/a/@href').extract()[0], '.cn/', '/')
            tmp_models = s.xpath('dd/table/tr')
            for m in tmp_models:
                if m.xpath('th/text()'): continue
                item['model_id'] = filt(m.xpath('td[1]/a/@href').extract()[0], 'spec_', '.')
                item['model_name'] = m.xpath('td[1]/a/text()').extract()[0]
                item['model_name'] = '%s %s' % (item['series_name'], item['model_name']) # 车型名称前加车系
                item['guide_price'] = re_digital(m.xpath('td[2]/p/text()').extract()[0])#m.xpath('td[2]/p/text()').extract()[0].strip(u'万').strip()
                z = m.xpath('td[3]/div[@class="this-number red"]/a/text()').extract()
                if not z: z = m.xpath('td[3]/p/a/text()').extract()
                item['dealer_price'] = re_digital(z[0])#z[0].strip(u'万').strip()
                if item['dealer_price'] == -1 or item['guide_price'] == -1:
                    self.doPost(postCheXingBaoJia, item)

    def parseYouHuiCuXiao(self, response):
        sel = Selector(response)

        ls = sel.xpath('//dl[@class="promot-dl "]/dt/a/@href')
        for l in ls: yield Request(response.urljoin(l.extract()), self.parseYouHuiCuXiao_process)

        # np = sel.xpath('//a[@class="page-next "]/@href').extract()
        # if np: yield Request(response.urljoin(np[0]), self.parseYouHuiCuXiao)

    def parseYouHuiCuXiao_process(self, response):
        sel = Selector(response)

        item = {}
        item['type'] = 'YouHuiCuXiao'
        item['page_url'] = response.url
        tmp = sel.xpath('//p[@class="cont-time"]/text()')
        if not tmp: tmp = sel.xpath('//span[@class="red"]/text()')
        if not tmp: return
        tmp = tmp.extract()[0].replace(u'促销时间', '')
        if u'.' in tmp: tmp = tmp.split(u'-')   # 2015.05.31-2015.06.04
        else: tmp = tmp.split(u' - ')           # 2015-05-31 - 2015-06-04
        item['date_from'] = tmp[0].replace(u' ', '')
        item['date_to'] = tmp[1].replace(u' ', '')

        tmp = sel.xpath('//div[@class="dealertext"]/p[2]')
        if tmp: item['content'] = tmp.extract()[0]
        else: return

        item['city_name'] = tmp.xpath('//div[@class="breadnav"]/a[2]/text()').extract()[0]
        item['city_code'] = tmp.xpath('//div[@class="breadnav"]/a[2]/@href').extract()[0].strip('/')
        item['dealer_name'] = tmp.xpath('//div[@class="breadnav"]/a[3]/text()').extract()[0]
        item['dealer_id'] = tmp.xpath('//div[@class="breadnav"]/a[3]/@href').extract()[0].strip('/')
        item['title'] = sel.xpath('//p[@class="title-text"]/text()').extract()[0]
        item['pub_date'] = sel.xpath('//span[@class="fn-right"]/text()').extract()[0].strip(u'日期：')

        tmp = sel.xpath('//input[@id="SeriesName"]/@value').extract()
        if tmp: item['series_name'] = tmp[0]
        else: tmp = sel.xpath('//p[@class="name-text font-yh"]/a/text()').extract()
        if not tmp: return
        item['series_name'] = tmp[0]

        tmp = sel.xpath('//input[@id="SeriesId"]/@value').extract()
        if tmp: item['series_id'] = tmp[0]
        else:
            tmp = sel.xpath('//p[@class="name-text font-yh"]/a/@href').extract()
            if tmp: item['series_id'] = filt(tmp[0], 'b_', '.')
            else: return

        tables = sel.xpath('//div[@class="dealertext"]/table/tbody/tr')
        ts = []
        for table in tables:
            t = {}
            if table.xpath('th'): continue
            if table.xpath('td/@width'): continue
            if len(table.xpath('td').extract()) < 5: continue

            t['model_name'] = table.xpath('td[1]/text()').extract()[0].strip()
            t['guide_price'] = table.xpath('td[2]/text()').extract()[0].strip()
            t['reduction'] = table.xpath('td[3]/text()').extract()[0].replace(u'↓', '').strip()
            t['dealer_price'] = table.xpath('td[4]/text()').extract()[0].replace(u'询价', '').strip()
            t['total_price'] = table.xpath('td[5]/text()').extract()[0].replace(u'详情', '').strip()
            ts.append(t)
        item['prices'] = json.dumps(ts, ensure_ascii=False)

        self.doPost(postYouHuiCuXiao, item)

    def parseZiXunXinXi(self, response):
        sel = Selector(response)

        ls = sel.xpath('//dl[@class="promot-dl new-dl"]/dd/p[@class="text"]/a/@href')
        for l in ls: yield Request(response.urljoin(l.extract()), self.parseZiXunXinXi_process)

        # np = sel.xpath('//a[@class="page-next "]/@href').extract()
        # if np: yield Request(response.urljoin(np[0]), self.parseZiXunXinXi)

    def parseZiXunXinXi_process(self, response):
        sel = Selector(response)
        item = {}
        item['type'] = 'ZiXunXinXi'
        item['page_url'] = response.url

        tmp = sel.xpath('//div[@class="breadnav"]')
        item['city_name'] = tmp.xpath('a[2]/text()').extract()[0]
        item['city_code'] = tmp.xpath('a[2]/@href').extract()[0].strip('/')
        item['dealer_name'] = tmp.xpath('a[3]/text()').extract()[0]
        item['dealer_id'] = tmp.xpath('a[3]/@href').extract()[0].strip('/')

        tmp = sel.xpath('//div[@class="inforcont-title"]')
        item['title'] = tmp.xpath('p[@class="title-text"]/text()').extract()[0]
        item['pub_date'] = tmp.xpath('p[@class="title-source fn-clear"]/span[@class="fn-right"]/text()').extract()[0].strip(u'日期：')

        tmp = sel.xpath('//div[@class="dealermain"]')
        if not tmp: return
        item['content'] = tmp.extract()[0]

        imgs = tmp.xpath('p/img/@src').extract()
        for img in imgs:
            item['content'] = item['content'].replace(img, oss_process_img(img))

        self.doPost(postZiXunXinXi, item)

    def closed(self, reason):
        self.logger.info('%s: CheXingBaoJia.%d YouHuiCuXiao.%d ZiXunXinXi.%d' %
            (reason, self.countCheXingBaoJia, self.countYouHuiCuXiao, self.countZiXunXinXi))
