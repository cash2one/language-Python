#!/usr/bin/env python
# coding: utf-8

import time, json
import urllib
import requests

from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
import base64

def sign(data):
    h = SHA.new()
    h.update(json.dumps(data, ensure_ascii=False))
    signature = PKCS1_v1_5.new(RSA.importKey('''

    ''')).sign(h)
    return base64.b64encode(signature)

class RestApi:
    def __init__(self, domain='https://openapi.alipay.com/gateway.do'):
        self.__domain = domain
        self.__app_id = ''

    def set_app_info(self, app_id):
        self.__app_id = app_id

    def getapiname(self):
        return ''

    def getMultipartParas(self):
        return [];

    def getTranslateParas(self):
        return {};

    def encode_sorted(self, data):
        string = ''
        for k in sorted(data.keys()):
            string += '%s=%s&' % (k, data[k])
        return string[:-1]

    def getApplicationParameters(self):
        application_parameter = {}
        for key, value in self.__dict__.iteritems():
            if not key.startswith("__") and not key in self.getMultipartParas() and not key.startswith("_RestApi__") and value:
                key = key.startswith('_') and key[1:] or key
                application_parameter[key] = value
        translate_parameter = self.getTranslateParas()
        for key, value in application_parameter.iteritems():
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter.pop(key)
        return application_parameter

    def getResponse(self):
        sys_parameters = {
            'app_id': self.__app_id,
            'method': self.getapiname(),
            'format': 'JSON',
            'charset': 'utf-8',
            'sign_type': 'RSA',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            'version': '1.0',
            'app_auth_token': '',
            'biz_content': json.dumps(
                self.getApplicationParameters(),
                ensure_ascii=False,
                sort_keys=True
            ).replace(' ', ''),
        }
        sys_parameters['sign'] = sign(self.encode_sorted(sys_parameters))
        return requests.post(self.__domain, sys_parameters).json()
