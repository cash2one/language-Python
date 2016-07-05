#!/usr/bin/env python
# coding: utf-8

import sys, logging
import jieba
import jieba.analyse

SOURCE_FILE = 'src.txt'
USER_DICT_FILE = 'user.dict'

if __name__ == '__main__':
	reload(sys)
	sys.setdefaultencoding('utf-8')

	logging.basicConfig(level=logging.INFO, format='[%(asctime)s] %(filename)s %(levelname)s: %(message)s')#, filename='wordfreq.py.log', filemode='a')

	# 并行线程
	jieba.enable_parallel(4)

	# 加载用户自定义字典
	jieba.load_userdict(USER_DICT_FILE)

	# print '/'.join(jieba.cut(open(SOURCE_FILE).read()))

	# 关键词提取
	find_word = jieba.analyse.extract_tags(open('src.txt').read(), topK=100, withWeight=True)
	for wd, weight in find_word:
		print wd, ',', int(weight * 100)
