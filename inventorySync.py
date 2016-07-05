#!/usr/bin/env python
# coding: utf-8

import sys, logging
import requests

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.ERROR, format='%(asctime)s [%(levelname)s]: %(message)s', filename='inventorySync.py.log', filemode='a')
	console = logging.StreamHandler()
	console.setFormatter(logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s'))
	logging.getLogger('').addHandler(console)

	try:
		logging.info(requests.post(url='http:///webservice/webservice.php/webservice/tmall/inventorySync', data=None).text)
	except Exception, e:
		logging.error(e)
