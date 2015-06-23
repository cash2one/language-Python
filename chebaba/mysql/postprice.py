# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, json, sys
from simplemysql import SimpleMysql

STEP = 100
AUTOHOMEPRICE_API = ''
TABLE = 'autohome_price'
MYSQL_HOST = '127.0.0.1'
MYSQL_DB = 'wholenetwork'
MYSQL_USER = 'root'
MYSQL_PASS = 'root'
FROM_DATE = '2015-06-23'

def doPost(url, item):
    data = {}
    data['dealer_id'] = item.dealerid
    data['dealer_name'] = item.dealer
    data['id'] = item.modelid
    data['title'] = item.model
    data['zprice'] = item.oprice
    data['price'] = item.price
    print data['dealer_id'], data['dealer_name'], data['id'], data['title'], data['zprice'], data['price'],
    request = urllib2.Request(url, urllib.urlencode(data))
    response = urllib2.urlopen(request).read()
    return data, json.loads(response)

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
    count = 0
    while rows:
        rows = db.getAll(table=TABLE, fields='*', limit=[pos1, STEP], where=("current > %s", [FROM_DATE]))
        if not rows: exit()
        pos1 += STEP
        for row in rows:
            count += 1
            try:
                data, result = doPost(AUTOHOMEPRICE_API, row)
                print '\t', count, result['error'], result['msg']
            except Exception, e:
                print e
                continue
