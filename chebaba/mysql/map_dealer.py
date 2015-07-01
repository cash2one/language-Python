# -*- coding: utf-8 -*-
#!/usr/bin/env python

import urllib, urllib2, sys
from simplemysql import SimpleMysql

def to_dict(n):
	return dict(zip(n._fields, n))

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    db_old = SimpleMysql(host = '127.0.0.1', db = 'old', user = 'root', passwd = 'root')
    db_new = SimpleMysql(host = '127.0.0.1', db = 'new', user = 'root', passwd = 'root')
    if not db_old or not db_new:
        print 'Connected to database failed.'
        exit()

    old_map = db_old.getAll(table='ca_map', fields=['source_id', 'target_id'])
    results = {}
    for item in old_map:
    	tmp = db_old.getOne(table='ca_dealer', fields=['identifier'], where=('dealer_id=%s', [item.target_id]))
    	if tmp: results[tmp.identifier] = item.source_id

    for result in results:
    	print result, results[result]
    	tmp = db_new.getOne(table='ca_dealer', fields=['dealer_id'], where=('identifier=%s', [result]))
    	if tmp: db_new.update(table='ca_map', data={'target_id': tmp.dealer_id}, where=('source_id=%s', [results[result]]))
