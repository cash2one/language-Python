# -*- coding: gb18030 -*-

# ԭʼĿ����Ϊ���滻��ǰĿ¼�������ļ����ض�һ�仰
# ֵ�òο��ľ����ı�����������滻

import os
import sys
import re

def dir(path):
	files = []
	for f in os.listdir(path):
		if not os.path.isdir(f):
			files.append(f)
	return files

def remove(f):
	fd = open(f, 'r')
	raw_data = fd.read()
	fd.close()

	new_fd = open('new_' + f, 'wb')
	
	reg = re.compile('\d{4}��\d+��\d+������')
	raw_data = re.sub(reg, '', raw_data)
	
	new_fd.write(raw_data)
	new_fd.close()

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('gb18030')

	files = dir('.')
	for f in files:
		remove(f)
		print 'stripped: ', f
