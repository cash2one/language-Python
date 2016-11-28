#!/usr/bin/env python
# coding: utf-8

from alipay.api.base import RestApi

class DataserviceBillDownloadQuery(RestApi):
    def __init__(self):
        RestApi.__init__(self)
        self.bill_type = ''
        self.bill_date = ''

    def getapiname(self):
        return 'alipay.data.dataservice.bill.downloadurl.query'
