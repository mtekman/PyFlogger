#!/usr/bin/env python

import sys
from Yemek import Yemek

class FoodList:
	def __init__(self,file="/home/user/.config/keto/foodlist.txt"):
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
	
		# Strip Header
		f.readline()
		for foodentry in f:
			if len(foodentry)< 5:
				continue
			food = Yemek(foodentry.split('\t'))
			self.foodmap[food.name]= food
		f.close()

	def write(self):
		f=open(self.path,'w')

		print >> f, Yemek('a','1','2','3','4','5','6','7').printout(headeronly=True)

		for food in sorted(self.foodmap.keys()):
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(header=False)
		f.close()


	def printlist(self):
		keys = sorted(self.foodmap.keys())
		print >> sys.stderr, self.foodmap[keys[0]].printout(headeronly=True)	

		for food in keys:
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(header=False)

	@staticmethod
	def amountsplit(text):
		index_let=0
		for a in text:
		        if not(ord(a) >= 48 and ord(a) <= 57):
		                break
        	index_let +=1
		return text[0:index_let], text[index_let:]


	def insert(self,name):
		per,unit = FoodList.amountsplit(raw_input("Per,Unit (e.g. '100g'): ").strip())
		kc, carb, prot, fat = raw_input("kCal, Carb, Protein, Fat: ").split(',')
			
		self.foodmap[name] = Yemek(name,kc,carb,prot,fat,per,unit)
		print >> sys.stderr, "Inserted", name
		self.write()


	def removeprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			self.foodmap.remove(name)
			print >> sys.stderr, "Removed"
		else:
			print >> sys.stderr, "does not exist"
		write()

	def insertprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			print >> sys.stderr, "Food already exists!\n"
			print >> sys.stderr,  self.foodmap[name].printout()
			exit(-1)
		self.insert(name)


	def updateprompt(self):
		name = raw_input('Food Name:').strip()

		if name in self.foodmap:
			print >> sys.stderr, "Currently:"
			print >> sys.stderr,  self.foodmap[name].printout()
		else:
			print >> sys.stderr, "New Food:"
		self.insert(name)
	
	def info(self,name):
		if name in self.foodmap:
			print >> sys.stderr,  self.foodmap[name].printout()
		else:
			print >> sys.stderr, "Cannot find:", name
			ans = raw_input('insert?').strip()
			if ans[0].lower() == 'y':
				self.insert(name)


w = FoodList()
w.write()
exit(0)
#w.insertprompt()
print >> sys.stderr, w.foodmap
#w.printlist()
