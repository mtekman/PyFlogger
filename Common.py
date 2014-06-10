#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from time import localtime, time
from Yemek import Yemek


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
	ans = raw_input(message+' ').strip()
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
	
	num_builder = amount_builder=""
	num_encounter = float_encounter = False
	
	for a in xrange(len(text)):
		chor = text[a]
			
		if lower <= ord(chor) <= 57:
			if floater and chor == '.':
				if float_encounter:continue				#Already seen a dot, skip
				else:float_encounter=True
				
			num_builder += chor
			num_encounter = True
		else:
			#NAN
			if num_encounter:
				amount_builder += chor
		
	try:
		amount = amount_builder.splitlines()[0].strip()
	except IndexError:
		amount = ""
	
	if floater:return fraction(num_builder),amount
	else:return int(num_builder),amount


def stripAll(list):
	return map(lambda x: x.strip(), list)


'''Takes a list of yem objects and returns one'''
def choice(yem_array, compare_to=0):
	
	if len(yem_array)==0:
		print "No matches"
		return -1
	
	print ""
	choose = 1
	print Yemek.printFullHeader()

	for x in yem_array:
		scale = 1
		try:
			if len(x)>1:
				scale = x[1]
				x = x[0]
		except AttributeError:
			pass # Not a tuple
		
		choose_s= "%2d: " % choose
		
		sobj = x.scaled(scale)
		print sobj.printout(pre=choose_s)
		
		if compare_to!=0:
			if sobj.isEqual(compare_to):
				print "Found definite match!"
				return x
		
#		print x.scaled(scale).printout(pre=choose_s)
		choose +=1
	
	ind = ""
	isNum = False
	while not isNum:
		try:
			ind = int(raw_input('Please pick a number (0 to cancel): '))-1
			isNum = True
		except ValueError:
			print "Not a number, please try again"
	
	if ind==-1:return -1
	
	res = yem_array[ind]
	try:
		res = yem_array[ind][0]  # dont want scale
	except AttributeError:
		pass
	return res


def makewhitespace(lbuff):
	return (' '*lbuff)
