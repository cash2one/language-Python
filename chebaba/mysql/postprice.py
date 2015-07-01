# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, sys
from simplemysql import SimpleMysql

STEP = 100
AUTOHOMEPRICE_API = 'http://localhost/api/price'
AUTOHOMEPRICE_API = 'http://localhost/api/price'
AUTOHOMEPRICE_API = 'http://localhost/api/price'
TABLE = 'autohome_allprice'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'wholenetwork'
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
FROM_DATE = '2015-06-30'
BRANDS = "'骊威','楼兰','玛驰','奇骏','骐达','天籁','逍客','轩逸','阳光','碧莲','贵士','日产370Z','日产GT-R','途乐','启辰D50','启辰R30','启辰R50','启辰R50X','启辰T70','晨风'"

def doPost(url, item):
    data = {}
    data['dealer_name'] = item.dealer
    data['dealer_id'] = item.dealerid
    data['series_name'] = item.brand
    data['series_id'] = item.brandid
    data['title'] = item.model
    data['id'] = item.modelid
    data['zprice'] = item.oprice
    data['price'] = item.price
    print data['dealer_name'], data['series_name'], data['title'], data['zprice'], data['price'], '\t',
    request = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(request).read()
    return response

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    db = SimpleMysql(
        host = MYSQL_HOST,
        db = MYSQL_DB,
        user = MYSQL_USER,
        passwd = MYSQL_PASS)
    if not db:
        print 'Connected to database failed.'
        exit()

    pos1 = 0
    rows = True
    while rows:
        rows = db.getAll(table=TABLE, fields='*', limit=[pos1, STEP], where=("current>%s and brand in (" + BRANDS + ")", [FROM_DATE]))
        if not rows: exit()
        pos1 += STEP
        for row in rows:
            try:
                print doPost(AUTOHOMEPRICE_API, row)
            except Exception, e:
                print e
                continue

