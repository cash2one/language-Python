#-*- coding: utf-8 -*-
import os

if __name__ == '__main__':
	p = 'E:/nginx/www/ec/ebak/bdata/wxmiqi_20150127070825/'
	fs = os.listdir(p)
	r = open('result.sql', 'w')
	index = 0
	for f in fs:
		index += 1
		print str(index), '/', len(fs), p + f
		ls = open(p + f, 'r').readlines()
		for l in ls:
			# 生成 create table
			if l[:3] != 'E_D': continue
			else: l = l.replace('E_D("', '').replace('");', '')
			if l[:7] != 'replace': continue
			else: l = l.replace('replace', 'insert')
			'''
			# 生成 insert into
			if l == '': continue
			if l[:2] == '<?': continue
			if l[:2] == '?>': continue
			if l[:2] == '/*': continue
			if l[:2] == '*/': continue
			if l[:1] == '	': continue
			if l[:1] == '/n': continue
			if l[:3] == '$tb': continue
			if l[:7] == 'require': continue
			if l[:7] == 'Baktime': continue
			if l[:11] == 'DoSetDbChar': continue
			if l[:3] == 'E_D': l = l.replace('E_D("', '').replace('");', '')
			if l[:3] == 'E_C': l = l.replace('E_C("', '').replace('");', '')
			if l[:7] == 'replace': continue
			if l[-16:-1] == 'CHARSET=utf8");': l = l.replace('CHARSET=utf8");', 'CHARSET=utf8;')
			'''
			r.write(l)
	r.close()
