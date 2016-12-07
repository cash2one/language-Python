#!/usr/bin/env python
# coding: utf-8

from baidu.api.base import ApiSDKJsonClient

class ReportService(ApiSDKJsonClient):
    def __init__(self):
        ApiSDKJsonClient.__init__(self, 'sms', 'service', 'ReportService')

    def getRealTimeData(self, getRealTimeDataInfoRequest=None):
        return self.execute('getRealTimeData', getRealTimeDataInfoRequest)

    def getRealTimeQueryData(self, getRealTimeQueryDataInfoRequest=None):
        return self.execute('getRealTimeQueryData', getRealTimeQueryDataInfoRequest)
