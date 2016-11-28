#!/usr/bin/env python
# coding: utf-8

import alipay.api
import json

if __name__ == '__main__':
    bill = alipay.api.DataserviceBillDownloadQuery()
    bill.bill_type = 'trade,signcustomer'
    bill.bill_date = '2016-04-05'
    print(json.dumps((bill.getResponse()), ensure_ascii=False))
