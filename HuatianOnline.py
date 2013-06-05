#coding=utf-8

import time
import urllib
import lxml.html
import json
import sys

def getDateTime():
	return time.strftime('%Y-%m-%d %X', time.localtime())

def methods(type):
	result = getDateTime() + ' - [' + type + ']: '
	status = ['OFF', 'Web Client', 'Android Client']
	if int(type) < len(status):
		return result + status[int(type)]
	return result + 'unknown'

if __name__ == '__main__':
	uid = ''		# You could add an id here that you want to monitor
	reload(sys)
	sys.setdefaultencoding('utf-8')
	output = open(uid + '.log', 'a')
	old_online = '0'

	print getDateTime() + ' - monitoring...'

	try:
		while 1:
			url = 'http://love.163.com/' + uid
			dom = urllib.urlopen(url).read()
			tree = lxml.html.fromstring(dom)
			tre = tree.xpath("//script[@id='data_userProfile']")
			s = json.loads(tre[0].text)

			result = getDateTime() + '\n'

			for i in s:
				result += i + ': ' + str(s[i]) + '\n'

			if old_online != s['isOnline']:
				output.write(result + '\n')
				old_online = s['isOnline']
				print methods(old_online)

			time.sleep(30)
	except (KeyboardInterrupt):
		error = getDateTime() + ' Error Message: Stopped by user.\n'
	except Exception, e:
		error = getDateTime() + ' Error Message: ' + str(e) + '\n'

	print error
	output.write(error)
	output.close()
	print getDateTime() + ' - END'
