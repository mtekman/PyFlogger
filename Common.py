#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from os import stat
from time import localtime, time, mktime
from Yemek import Yemek


__unit_converter_premap = [
	# grams
	(('grams', 'gram','g'), (1,'g')),
	(('kilogram','kilograms','kgs','kg'), (1000, 'g')),
	(('miligram', 'milligram', 'mg'), (0.001,'g')),
	(('oz', 'ounce', 'ounces'), (28,'g')),
	(('pound','pounds','lb','lbs'), (454,'g')),
	# litres
	(('cup', 'cups'), (237,'ml')),
	(('pint', 'pints'), (472,'ml')),
	(('quart', 'quarts'), (948, 'ml')),
	(('gallon', 'gallons'), (3792, 'ml')),
	(('litres', 'litre', 'liter', 'liters', 'l'), (1000,'ml')),
	(('millilitres','millilitre','milliliters','millilitre', 'ml'),(1,'ml')),
	(('teaspoon','tsp','teaspoons','tsps'), (5, 'ml')),
	(('tablespoon', 'tbsp', 'tablespoons', 'tbsps'), (15,'ml')),
	(('fluid ounce', 'fluid ounces', 'fluid oz'), (30,'ml')),
	# joules
	(('kilojoules', 'kj'), (1, 'kj')),
	(('joules'), (0.001, 'kj')),
	# cals
	(('kilocals', 'kCal', 'kcal', 'kc', 'kC'), (1, 'kC')),
	# serving
	(('serving','servings'), (1,'serving'))
]

# Premake
unit_converter = {}
for unit_types in __unit_converter_premap:
	for unit in unit_types[0]:
		unit_converter[unit] = unit_types[1]



############################ Prompts ###################################

def ynprompt(message):
	ans = 'g'
	while ans not in ['y','n']:
		ans = input(message+' (y/n):').strip()[0].lower()
	return ans == 'y'

	return (ans[0].lower()=='y')


'''Returns a list of items initially offered to user'''
def userlistprompt(message, str_array):
	opts = input("%s : %s\n" % (message,','.join(str_array)))
	opts = opts.strip()
	if opts == "":return -1
	return opts.split(',')


'''Returns a single item from an assosciative array'''
def userSingleListPrompt(pretext, message_array, str_array):
	opts = None
	lowr_str_array = [x.lower() for x in str_array]

	max_tries = 3
	while opts == None and max_tries > 0:
		inp = input("%s - %s : [%s]? " % (pretext,
			' / '.join(message_array),
			'/'.join(str_array)
			))

		inp += ' '
		inp = inp[0].lower()

		if inp not in lowr_str_array:
			RESULT("Invalid input.", end="")
			max_tries -= 1
		else:
			opts = inp

	return inp



def getIndexInput(max, multiple=False):
	ind_array = ""
	isNum = False
	inRange = False
	while not (isNum and inRange):
		try:
			if multiple:
				ind_array = [int(x)-1 for x in input('Please pick numbers (with spaces)(0 to cancel): ').split()]
			else:
				ind_array = [int(input('Please pick a number (0 to cancel): '))-1]
			isNum = True

			for ind in ind_array:
				if ind < max:inRange = True
				else:
					inRange = False
					RESULT("Out of range, please try again")
					break

		except ValueError:
			isNum = False
			RESULT("Not a number, please try again")

	if len(ind_array)==1:return ind_array[0]
	return ind_array





'''Takes any array and return chosen item(s)'''
def choice(array, compare_to=0, multiple=False):

	# Encaps.
	'''Takes a list of objects and returns one'''
	def def_choice(array, compare_to, isTuple=False, isYem=True):

		choose = 1
		if isYem:
			print(Yemek.printFullHeader())

		for x in array:
			scale = 1

			if isTuple:
					scale = x[1]
					x = x[0]

			choose_s= "%2d: " % choose
			sobj = x

			if isYem:
				sobj = x.scaled(scale)
				print(sobj.printout(pre=choose_s))
			else:
				print("%s%s" % (choose_s, (sobj if not isTuple else sobj+' '+str(scale))))

			if compare_to!=0:
				# Whatever is compared MUST have equality method overloaded, else standard type
				if sobj == compare_to:
					result("Found definite match!")
					return x
			choose +=1

		ind = getIndexInput(len(array), multiple)
		if ind==-1:return -1

		res = array[ind]
		if isTuple:
			res = array[ind][0]  # dont want scale
		print("")
		RESULT(("Chose: %s" % res) if not isYem else res.printout(pre="Chose: "))
		return res

	# Main
	print("")

	if len(array)==0:
		RESULT("No matches")
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


# write unit cases
def amountsplit(text, resolve_unit=False):

	text = text.split('(')[0]  # handle cases like 100ml (100ml)
	text = text.strip()

	lower = 46 # 46 = '.'

	num_builder = amount_builder=""
	num_encounter = float_encounter = False

	for a in range(len(text)):
		chor = text[a]

		if lower <= ord(chor) <= 57:
			if chor == '.':
				if float_encounter:continue				#Already seen a dot, skip
				else:float_encounter=True

			num_builder += chor
			num_encounter = True
		else:
			#NAN
			if num_encounter:
				amount_builder += chor

	try:
		unit = amount_builder.splitlines()[0].strip()
	except IndexError:
		unit = ""


	amount = fraction(num_builder)

	if resolve_unit:
		try:
			multi, unit = unit_converter[unit]
			amount *= multi
		except KeyError:
			error("Not encountered", unit, "before", file=sys.stderr)

	return amount , unit






###################### File Handling ###################################

def backup(path):
	backup_path = path+".backup"

	try:
		curr_bytes = stat(path).st_size
	except OSError:
		RESULT("No file to backup...")
		return 0

	try:
		back_bytes = stat(backup_path).st_size
	except OSError:
		RESULT("No backup file, creating one")
		b=open(backup_path,'w');b.write("");b.close()
		back_bytes = stat(backup_path).st_size

	if curr_bytes > back_bytes:
		back = open(backup_path,'w')
		curr = open(path,'r')
		# Copy current into backup if gt
#		print "Backing", path, "into", backup_path
		for line in curr:
			print(line, file=back)
		back.close()
		curr.close()



##################### Time functions ##########################
def ymd2secs(xxx_todo_changeme):
	(y,m,d) = xxx_todo_changeme
	if str(d).find('-')!=-1:
		d = d.split('-')[0]
	return mktime((int(y),int(m),int(d),0,0,0,0,0,-1))


def daysSince(date1,date2):
	y1,m1,d1 = [int(x) for x in date1.split('/')]
	y2,m2,d2 = [int(x) for x in date2.split('/')]

	seconds1 = ymd2secs((y1,m1,d1))
	seconds2 = ymd2secs((y2,m2,d2))

	diff = seconds2 - seconds1
	return float(diff)/(24*60*60)


def tomorrow():
	return nextDay(time())

def yesterday():
	return previousDay(time())

def today():
	return "%04d/%02d/%02d" % localtime(time())[0:3]

def now():
	return "%04d/%02d/%02d--%02d:%02d" % localtime(time())[0:5]


def previousDay(date):
	try:
		date_sec = ymd2secs( date.split('/') )
	except AttributeError:
		date_sec = date
		pass
	return "%04d/%02d/%02d" % localtime(date_sec-(24*60*60))[0:3]

def nextDay(date):
	try:
		date_sec = ymd2secs( date.split('/') )
	except AttributeError:
		date_sec = date
		pass
	return "%04d/%02d/%02d" % localtime(date_sec+(24*60*60))[0:3]



##################### String handling #################################

def stripAll(list):
	return [x.strip() for x in list]


def makewhitespace(lbuff):
	return (' '*lbuff)
