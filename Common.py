#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from os import stat
from time import localtime, time, mktime
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


############################ Prompts ###################################

def ynprompt(message):
	ans = 'g'
	while ans not in ['y','n']:
		ans = raw_input(message+' (y/n):').strip()[0].lower()
	return ans == 'y'
	


	return (ans[0].lower()=='y')


def userlistprompt(message, str_array):
	opts = raw_input("%s : %s\n" % (message,','.join(str_array)))
	opts = opts.strip()
	if opts == "":return -1
	return opts.split(',')
	


def getIndexInput(max, multiple=False):
	ind_array = ""
	isNum = False
	inRange = False
	while not (isNum and inRange):
		try:
			if multiple:
				ind_array = map(lambda x: int(x)-1, raw_input('Please pick numbers (with spaces)(0 to cancel): ').split())
			else:
				ind_array = [int(raw_input('Please pick a number (0 to cancel): '))-1]
			isNum = True
		
			for ind in ind_array:
				if ind < max:inRange = True
				else:
					inRange = False
					print "Out of range, please try again"
					break

		except ValueError:
			isNum = False
			print "Not a number, please try again"

	if len(ind_array)==1:return ind_array[0]
	return ind_array
	




'''Takes any array and return chosen item(s)'''
def choice(array, compare_to=0, multiple=False):
	
	# Encaps.
	'''Takes a list of objects and returns one'''
	def def_choice(array, compare_to, isTuple=False, isYem=True):
		
		choose = 1
		if isYem:print Yemek.printFullHeader()

		for x in array:
			scale = 1
			
			if isTuple:
					scale = x[1]
					x = x[0]
			
			choose_s= "%2d: " % choose
			sobj = x
			
			if isYem:
				sobj = x.scaled(scale)
				print sobj.printout(pre=choose_s)
			else:
				print "%s%s" % (choose_s, (sobj if not isTuple else sobj+' '+str(scale)))
			
			if compare_to!=0:
				# Whatever is compared MUST have equality method overloaded, else standard type
				if sobj == compare_to:
					print "Found definite match!"
					return x
			choose +=1
		
		ind = getIndexInput(len(array), multiple)
		if ind==-1:return -1
		
		res = array[ind]
		if isTuple:
			res = array[ind][0]  # dont want scale
		print ""
		print ("Chose: %s" % res) if not isYem else res.printout(pre="Chose: ")
		return res
	
	# Main
	print ""

	if len(array)==0:
		print "No matches"
		return -1
	
	isTuple = isinstance(array[0], tuple)
	isYem = isinstance( array[0][0] if isTuple else array[0], Yemek)
	
	return def_choice(array, compare_to, isTuple, isYem)






###################### Str to Num ######################################

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





###################### File Handling ###################################

def backup(path):
	backup_path = path+".backup"

	try:
		curr_bytes = stat(path).st_size
	except OSError:
		print "No file to backup..."
		return 0

	try:
		back_bytes = stat(backup_path).st_size
	except OSError:
		print "No backup file, creating one"
		b=open(backup_path,'w');b.write("");b.close()
		back_bytes = stat(backup_path).st_size

	if curr_bytes > back_bytes:
		back = open(backup_path,'w')
		curr = open(path,'r')
		# Copy current into backup if gt
#		print "Backing", path, "into", backup_path
		for line in curr:
			print >> back, line
		back.close()
		curr.close()



##################### Time functions ##########################
def ymd2secs((y,m,d)):
	if d.find('-')!=-1:
		d = d.split('-')[0]
#	print y,m,d
	return mktime((int(y),int(m),int(d),0,0,0,0,0,-1))


def daysSince(date1,date2):
	y1,m1,d1 = map(lambda x: int(x), date1.split('/'))
	y2,m2,d2 = map(lambda x: int(x), date2.split('/'))
	
	seconds1 = ymd2secs((y1,m1,d1))
	seconds2 = ymd2secs((y2,m2,d2))
	
	diff = seconds2 - seconds1
	return float(diff)/(24*60*60)


def tomorrow():
	return nextDay(time())

def yesterday():
	return previousDay(time())
     
def previousDay(date_sec):
	return "%04d/%02d/%02d" % localtime(date_sec-(24*60*60))[0:3]
	
def nextDay(date_sec):
	return "%04d/%02d/%02d" % localtime(date_sec+(24*60*60))[0:3]



##################### String handling #################################

def stripAll(list):
	return map(lambda x: x.strip(), list)


def makewhitespace(lbuff):
	return (' '*lbuff)
