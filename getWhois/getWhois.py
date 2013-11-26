#!/usr/bin/env python

import suds

WSDL = 'http://www.webservicex.net/whois.asmx?WSDL'
LISTFILE = 'domains.dict'
TARGETFILE = 'result.log'

def getWhois(url):
	return suds.client.Client(WSDL).service.GetWhoIS(url)

if __name__ == '__main__':
	fp = open(LISTFILE, 'r')
	rf = open(TARGETFILE, 'w')

	try:
		for item in fp:
			item = item[0:len(item) - 2]
			print item
			rf.write('[ ' + item + ' ] =================\r\n' + getWhois(item))
	except Exception, e:
		print str(e)

	rf.close()
	fp.close()
