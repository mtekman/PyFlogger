#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from time import localtime, time




#Global method
def ynprompt(message):
	ans = raw_input(message)
	return (ans[0].lower()=='y')


def fraction(am_amount):
	try:
		am = float(am_amount)
	except ValueError:
		spl = am_amount.split('/')
		am = float(spl[0])/float(spl[1])
	return am


def amountsplit(text,floater=False):
	text= text.strip()
	
	lower = 47
	if floater:lower=46 # '.' allowed
	
	index_let=0
	for a in text:
		if not(lower <= ord(a) <= 57):
			break
		index_let +=1
	
	num = text[0:index_let].strip()
	try:
		amount = text[index_let:].splitlines()[0].strip()
	except IndexError:
		amount = ""
	
	if floater:
		return fraction(num),amount
	else:
		return int(num),amount


def stripAll(list):
	return map(lambda x: x.strip(), list)
