#!/usr/bin/env python

import threading, suds, sys, time, random

WSDL = 'http://www.webservicex.net/whois.asmx?WSDL'
DICT = 'domains.dict'

class GetWhois(threading.Thread):
	def __init__(self, index, data):
		threading.Thread.__init__(self)
		self.index = index   # thread index number
		self.data = data	 # one task

	def run(self):
		if len(self.data) == 0: system.exit()
		fd1 = open(str(self.index) + 'success.log', 'w')
		fd2 = open(str(self.index) + 'failed.log', 'w')
		for item in self.data:
			item = item[0 : len(item) - 2]
			result = suds.client.Client(WSDL).service.GetWhoIS(item)
			if len(result) == 0: fd1.write('\r\n' + item + '===' + result + '\r\n')
			else: fd2.write('\r\n' + item + '\r\n')
			print str(self.index), item		# print current domain name
			time.sleep(random.randint(0, 20))
		fd1.write('finished')
		fd2.write('finished')
		fd1.close()
		fd2.close()

if __name__ == '__main__':
	fd = open(DICT, 'r')
	data = fd.readlines()
	length = len(data)
	index = 0
	range1 = 0
	range2 = 0
	step = 50

	try:
		while length > 0:
			range1 = range2
			range2 = range1 + step
			if range2 > length: range2 = length
			worker = GetWhois(index, data[range1 : range2])
			index = index + 1
			worker.start()
			if range2 == length: break
			time.sleep(random.randint(10, 200))
	except Exception, e:
		print str(e)

	fd.close()
