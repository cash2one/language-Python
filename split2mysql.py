#!/usr/bin/env python
# coding: utf-8

import sys
from simplemysql import SimpleMysql

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print sys.argv[1]
    db = SimpleMysql(host='127.0.0.1', user='root', passwd='root', db='databank')
    for i in open(sys.argv[1]):
        try:
            t = i.strip('\r\n').split('\t')
            r = {}
            r['username'] = t[0]
            r['password'] = t[1]
            r['email'] = t[2]
            db.insert('aipai', r)
        except Exception, e:
            continue
    db.commit()

