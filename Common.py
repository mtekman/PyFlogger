#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from time import localtime, time




#Global method
def ynprompt(message):
	ans = raw_input(message)
	return (ans[0].lower()=='y')



def amountsplit(text):
	text= text.strip()
	index_let=0
	for a in text:
		if not(47 <= ord(a) <= 57):
			break
		index_let +=1
	return text[0:index_let].strip(), text[index_let:].splitlines()[0].strip()


def stripAll(list):
	return map(lambda x: x.strip(), list)
