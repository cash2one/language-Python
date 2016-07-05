#!/usr/bin/env python
# coding: utf-8

import requests
import json, os, sys, logging, threading, time
from simplemysql import SimpleMysql
from ConfigParser import RawConfigParser

INI_PATH = 'sync.cfg'
DEBUG = False
LOG_LEVEL = logging.INFO

class Ini():
    def __init__(self):
        self.config = RawConfigParser()

    def get_items(self, section='MySQL'):
        self.config.read(INI_PATH)
        return dict(self.config.items(section))

    def get_value(self, section, option):
        self.config.read(INI_PATH)
        return self.config.get(section, option)

    def set_updatedate(self, function):
        self.config.read(INI_PATH)
        self.config.set(function, 'updateddate', time.strftime('%Y-%m-%d %H:%M:%S'))

        with open(INI_PATH, 'wb') as fp:
            self.config.write(fp)

    def get_all_biz(self):
        self.config.read(INI_PATH)
        sections = self.config.sections()

        ini = Ini()
        result = {}
        for section in sections:
            if section not in ('MySQL', 'API'):
                result[section] = ini.get_items(section)

        return result

class GetData():
    url = ''

    def __init__(self, url=None):
        if url:
            self.url = url
        else:
            ini = Ini()
            urls = dict(ini.get_items(section='API'))
            self.url = DEBUG and urls['debug'] or urls['production']

    def from_e4s(self, function, kwargs):
        api_url = self.url % (function)
        logging.info(api_url)
        return requests.post(url=api_url, data=kwargs).text

class SetData():
    def __init__(self):
        dbc = ini.get_items('MySQL')
        self.db = SimpleMysql(host=dbc['host'], db=dbc['db'], user=dbc['user'], passwd=dbc['passwd'])

    def to_mysql(self, function, kwargs):
        ini = Ini()
        table = ini.get_value(function, 'targetTable')

        if not table: return
        result = self.db.insert(table, dict(kwargs))
        logging.info('Complete sync - function: %s, table: %s, result: %s' % (function, table, result))

        # 完成保存时间
        ini.set_updatedate(function)

class Process(threading.Thread):
    def __init__(self, function, kwargs, channel='mysql'):
        super(Process, self).__init__()
        self.function = function
        self.kwargs = kwargs
        self.channel = channel

    def run(self):
        logging.info('Starting to sync - channel: %s, function: %s, args: %s' % (self.channel, self.function, self.kwargs))

        gd = GetData()
        data = gd.from_e4s(self.function, dict(self.kwargs))
        data = dict(data)

        if int(data['retnCode']) != 0:
            logging.error(data)

        data = data['results']
        sd = SetData()
        if self.channel == 'tmall':
            return sd.to_api(self.function, data)
        return sd.to_mysql(self.function, data)

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')

    logging.basicConfig(level=LOG_LEVEL, format='[%(asctime)s] %(levelname)s: %(message)s', filename='sync.py.log', filemode='a')
    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
    logging.getLogger('').addHandler(console)

    try:
        ini = Ini()

        apis = ini.get_all_biz()
        for api in apis:
            if apis[api].pop('enable') != 'True':
                apis[api].pop('targettable')
                Process(api, apis[api]).start()
                time.sleep(1)

    except Exception, e:
       logging.error(e)
