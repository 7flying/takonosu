# -*- coding: utf-8 -*-
from config import DEBUG

def debug(code, string):
	if DEBUG:
		print '[' + code + ']: ' + str(string)
