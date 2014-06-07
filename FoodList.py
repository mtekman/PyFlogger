#!/usr/bin/env python

import sys
from Yemek import Yemek
from os.path import abspath
import Common
import MiniFSChecker

class FoodList:
	def __init__(self,file=abspath("../")+"/logs/keto_foodlist.txt"):
		self.foodmap={}
		self.path= file
		self.read()

	def read(self):
		try:
			f=open(self.path,'r')
		except IOError:
			f=open(self.path,'w')
			f.write(" ")
			f.close()
			return

		# Strip Headers
		f.readline(); f.readline()
		
		for foodentry in f:
			if len(foodentry)< 5:
				continue

#                                                             |   kC   Carb [Fibre,Sugar] =   Bad   Prot    Fat    per unit
#almond milk unsweetened                                      |   13    0.1 [  0.0,  0.0] =   0.1    0.4    1.1  100.0 ml
			name, data = foodentry.split('|')
			name = name.strip().lower()
			
			# No sscanf in python :(
			tokes = data.split()
			kC = tokes[0]
			carb_total = tokes[1]
			fibre = tokes[3].rsplit(',')[0]
			sugar=tokes[4].rsplit(']')[0]
			#carb_bad = tokes[6] # unused
			prot = tokes[7]
			fat = tokes[8]
			per = tokes[9]
			unit = ' '.join(tokes[10:])

			food = Yemek(name, kC, (carb_total, fibre, sugar), prot, fat, per, unit)
			self.foodmap[food.name]= food
		f.close()


	def write(self):
		f=open(self.path,'w')
		
		maxlen_name = reduce(lambda x,y: x if len(x) > len(y) else y, self.foodmap.keys())
		maxlen_name = len(maxlen_name)+5
		print "max:", maxlen_name

		print >> f, Yemek.printheader(buffer=maxlen_name)
		print >> f, ""
		
		for food in sorted(self.foodmap.keys()):
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(buffer=maxlen_name, pre="")
		f.close()



	def printlist(self):
		keys = sorted(self.foodmap.keys())
		print >> sys.stderr, Yemek.printheader()
		for food in keys:
			fooditem = self.foodmap[food]
			print >> sys.stderr, fooditem.printout() #.strip()



	def insertAll(self, name, kc, carb_info , prot, fat ,per, unit):
		name = name.strip().lower()
		self.foodmap[name] = Yemek(name,kc, carb_info, prot,fat,per,unit)
		print >> sys.stderr, "Inserted", name
		self.write()


	def insert(self,name):
		print "Inserting new food:", name
		per,unit = Common.amountsplit(raw_input("Per Unit (e.g. '100g'): ").strip())
		kc, carb_total, carb_sugar, carb_fibre , prot, fat = raw_input("kCal Carb Sug Fibr Prot Fat: ").split()
		
		self.insertAll(name, kc, (carb_total, carb_fibre, carb_sugar), prot, fat, per, unit)


	def removeprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			del self.foodmap[name]
			print >> sys.stderr, "[Removed]"
		else:
			print >> sys.stderr, "[Does not exist!]"
		self.write()


	def insertprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			print >> sys.stderr, "[Food already exists!]"
			print >> sys.stderr,  self.foodmap[name].printout(header=True)
			exit(-1)
		self.insert(name)


	#This is the main insertion method
	def updateprompt(self):
	
	   # Print details if exists, else insert, else return close match
		name = self.info(raw_input('Food: ').strip())
		
		# Name exists by now, or prog exited
      
		if name in self.foodmap:
			edit = raw_input('\nEdit? ')
			if edit[0].lower() != 'y':
				exit(-1)
		else:
			print >> sys.stderr, "\n[New Food: \"%s\"]" % name
		self.insert(name)
	
	def search(self,name):
		foods = self.foodmap.keys()
		searchfoods = map(lambda x: x.split(), foods)
		searchname = name.split()[0].strip()
		#print searchfoods, searchname
			
		found=[]; index=0;
		for sf in searchfoods:
			for s in sf:
				if searchname.strip() in s.strip():
					found.append(foods[index])
			index +=1
		return found

	
	def info(self,name):
		if name in self.foodmap:
			print >> sys.stderr,  self.foodmap[name].printout(header=True)
			return name

		#Search keys for closest match
		found = self.search(name)
		res = len(found)

		if res == 0:
			print >> sys.stderr, "\nCannot find:", "\"%s\"" % name,
			ans = raw_input(', insert? ').strip()
			if ans[0].lower() == 'y':
				self.insert(name)
				return name
			if raw_input('Search online? ').strip()[0].lower()=='y':
				f = MiniFSChecker.FHandler(name).found
				
				self.insertAll(f.name, f.kC, (f.carb.total, f.carb.fibre, f.carb.sugar), f.prot, 
					f.fat , f.per, f.unit)
				return f.name
			exit(0)
			
		# Found
		print >> sys.stderr, "\nDid you mean ",
		
		# One result
		if res==1:
			print >> sys.stderr, "\"%s\"" % found[0],
			ans = raw_input(' ? ')
			if ans[0].lower()=='y':
				name = found[0]
				print >> sys.stderr,  self.foodmap[name].printout(header=True)
			elif raw_input('Search online? ').strip()[0].lower()=='y':
				f = MiniFSChecker.FHandler(name).found
				print f.carb.total
				
				if f==-1:
					exit(-1)
				
				self.insertAll(f.name, f.kC, (f.carb.total, f.carb.fibre, f.carb.sugar), f.prot, 
					f.fat , f.per, f.unit)
				name = f.name
			else:
				self.insert(name)
			return name
	
		# Multiple results
		print >> sys.stderr, ": "
		
		cnt=1
		for f in found:
			print >> sys.stderr, ' *%d:' % cnt, f
			cnt += 1

		ans = int(raw_input('Enter Number (0 to cancel): '))
		if ans != 0:
			name = found[ans-1]
			print >> sys.stderr,  self.foodmap[name].printout(header=True)
		elif raw_input('Search online? ').strip()[0].lower()=='y':
			f = MiniFSChecker.FHandler(name).found
			self.insertAll(f.name, f.kC, f.carb, f.prot, 
				f.fat , f.per, f.unit)
			name = f.name
		else:
				self.insert(name)
		return name
				

#w = FoodList()
#w.updateprompt()
#  w.removeprompt()
#w.printlist()
