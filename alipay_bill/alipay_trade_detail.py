#!/usr/bin/env python
# coding: utf-8

import sys
import re
import time
import requests
import hashlib
import xmltodict
import json
import logging
from simplemysql import SimpleMysql
from collections import OrderedDict

class Alipay:
    def __init__(self, email, partner, md5str):
        self.__domain = 'https://mapi.alipay.com/gateway.do'
        self.__account = email
        self.__partner = partner
        self.__md5key = md5str

    def get_api(self):
        return ''

    def get_account(self):
        return self.__account

    def response_field(self):
        return self.get_api().replace('.', '_') + '_result'

    def encode_sorted(self, data):
        string = ''
        for k in sorted(data.keys()):
            if data[k]: # 去除空值参数
                string += '%s=%s&' % (k, data[k])
        return string[:-1]

    def get_params(self):
        params = {}
        for k, v in self.__dict__.iteritems():
            if not k.startswith('__') and not k.startswith('_Alipay__') and v: # 去除空值参数
                params[k] = v
        return params

    def get_response(self):
        params = {}
        params['service'] = self.get_api()
        params['partner'] = self.__partner
        params['_input_charset'] = 'utf-8'
        params.update(self.get_params())
        params['sign'] = self.sign(params)
        params['sign_type'] = 'MD5'
        try:
            response = requests.get(self.__domain, params).text
            od = self.xml2json(response)['alipay']
            if od['is_success'] == 'T': # 如果请求成功，返回response字段
                logging.info('successfully got %d bytes from remote' % (len(response)))
                return od['response'][self.response_field()]

            logging.error('failed to query: ' % (response))
            logging.error(od['error']) # 如果请求失败，打印错误码
        except Exception as e:
            logging.error(e)

    def xml2json(self, string):
        # 简单粗暴，直接按字符串长度去掉头部声明
        string = string.strip().startswith('<?xml') and string[38:] or string
        return xmltodict.parse(string, encoding='utf-8', process_namespaces=False)

    def sign(self, data):
        md5 = hashlib.md5()
        md5.update(self.encode_sorted(data) + self.__md5key)
        return md5.hexdigest()

class AccountPage(Alipay):
    def __init__(self, email, partner, md5str):
        Alipay.__init__(self, email, partner, md5str)
        self.page_no = '' # 查询页号，必填
        self.gmt_start_time = '' # 账务查询开始时间
        self.gmt_end_time = '' # 账务查询结束时间
        self.logon_id = '' # 交易收款账户
        self.iw_account_log_id = '' # 账务流水号
        self.trade_no = '' # 业务流水号
        self.merchant_out_order_no = '' # 商户订单号
        self.deposit_bank_no = '' # 充值网银流水号
        self.page_size = '' # 分页大小
        self.trans_code = '' # 交易类型代码

    def get_api(self):
        return 'account.page.query'

class Tom:
    def __init__(self):
        self.db = SimpleMysql(host='127.0.0.1', charset='utf8', db='nissan_group', user='root', passwd='dndcadmin88*..', autocommit=True, keep_alive=False)

    def reg_tid(self, string):
        string = string.strip()
        if not string or (string.isdigit() and len(string)>16): return None
        found = re.findall(re.compile(r'\d{16}', re.IGNORECASE), string)
        return found and found[-1] or None

    def addAccountPageQuery(self, data):
        try:
            for d in data:
                if d == 'merchant_out_order_no' and data[d]:
                    data['tid'] = self.reg_tid(data[d])

            return self.db.insertOrUpdate(table='alipay_bill', data=data, keys=('iw_account_log_id'))
        except Exception as e:
            logging.error(e)
            return 0

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s', filename='alipay_trade_detail.log', filemode='a')
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('[%(asctime)s] %(filename)s[%(lineno)d] %(levelname)s: %(message)s'))
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)

    users = [
        {
            'email': '',
            'partner': '',
            'md5str': ''
        }
    ]

    for user in users:
        account = AccountPage(email=user['email'], partner=user['partner'], md5str=user['md5str'])
        account.page_no = '1'
        tmp = time.mktime(time.strptime(sys.argv[1], '%Y-%m-%d'))
        account.gmt_start_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp - 24*60*60))
        account.gmt_end_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(tmp))
        account.logon_id = ''
        account.iw_account_log_id = ''
        account.trade_no = ''
        account.merchant_out_order_no = ''
        account.deposit_bank_no = ''
        account.page_size = ''
        account.trans_code = ''

        while True:
            try:
                tom = Tom()
                resp = account.get_response()
                logging.info('querying time span of %s: %s - %s' % (user['email'], account.gmt_start_time, account.gmt_end_time))

                count = 0
                items = resp['account_log_list'] and resp['account_log_list'].has_key('AccountQueryAccountLogVO') and resp['account_log_list']['AccountQueryAccountLogVO'] or None

                if type(items) == list:
                    for item in items:
                        item['username'] = account.get_account()
                        count += tom.addAccountPageQuery(item)
                    logging.info('got %d row(s), effected %d row(s)' % (len(items), count))
                elif type(items) == OrderedDict:
                    items['username'] = account.get_account()
                    logging.info('got 1 row(s), effected %d row(s)' % (tom.addAccountPageQuery(items)))
                else:
                    logging.error('cannot specify the type(%s) of result: %s' % (type(items), json.dumps(items, ensure_ascii=False)))
                    break

                if resp.has_key('has_next_page') and resp['has_next_page'] == 'T':
                    account.page_no = str(int(account.page_no) + 1)
                else:
                    break
            except Exception as e:
                logging.error(e)
