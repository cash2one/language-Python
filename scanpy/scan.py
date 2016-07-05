#!/usr/bin/env python
# coding: utf-8

import sys, socket, threading, time, logging

socket.setdefaulttimeout(60)

class CSocketPort(threading.Thread):
	def __init__(self, cond, host):
		super(CSocketPort, self).__init__()
		self.cond = cond
		self.cond.set()
		self.HOST = host

	def run(self):
		lip = ip2num(self.HOST) & 0x000000FF
		try:
			if lip == 1: print self.HOST, '\t',
			print ('%3d' % lip), lip == 255 and '\n' or '\b' * 5,
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			s.connect((self.HOST, 22))
			self.cond.set()
			print '\n',
			logging.info(self.HOST)
			print self.HOST, '\t',
		except Exception, e:
			self.cond.set()

def ip2num(ip):
	ip = [int(x) for x in ip.split('.')]
	return ip[0] << 24 | ip[1] << 16 | ip[2] << 8 | ip[3]

def num2ip(num):
	return '%s.%s.%s.%s' % ((num & 0xFF000000) >> 24, (num & 0x00FF0000) >> 16, (num & 0x0000FF00) >> 8, (num & 0x000000FF))

def buildip(ip1, ip2):
	if ip1 > ip2: return []
	return [num2ip(num) for num in range(ip1, ip2) if num & 0xFF]

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.INFO, format='%(message)s', filename='22.log', filemode='a')
	console = logging.StreamHandler()
	console.setLevel(logging.INFO)
	console.setFormatter(logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s'))
	logging.getLogger('').addHandler(console)

	for ip in open('us.txt', 'r'):
		ips = ip.split(' ')
		ip1 = ips[0].strip()
		ip2 = ips[1].strip()

		iplist = buildip(ip2num(ip1), ip2num(ip2))
		I1 = 0

		while I1 < len(iplist):
			time.sleep(0.1)
			CSocketPort(threading.Event(), iplist[I1]).start()
			I1 += 1
