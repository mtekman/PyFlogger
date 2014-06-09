#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from time import localtime, time


#Taken from r/slowcooking
conversion = {}
conversion['teaspoon'] = conversion['tsp'] = conversion['teaspoons'] = conversion['tsps'] = float(5) #ml
conversion['tablespoon'] = conversion['tbsp'] = conversion['tablespoons'] = conversion['tbsps'] = float(15) #ml
conversion['fluid ounce'] = conversion['fluid ounces'] = conversion['fluid oz'] = float(30) #ml
conversion['oz'] = conversion['ounce'] = conversion['ounces'] = float(28) #grams
conversion['pound'] = conversion['pounds'] = conversion['lb'] = conversion['lbs'] = float(454) #grams
conversion['cup'] = conversion['cups'] = float(237) #ml
conversion['pint'] = conversion['pints'] = 2*conversion['cups']
conversion['quart'] = conversion['quarts'] = 4*conversion['cups']
conversion['gallon'] = 4*conversion['quart']


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
