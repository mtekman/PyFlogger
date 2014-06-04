#!/usr/bin/env python

from FoodList import FoodList

class Suggest:
	def __init__(self, foodlist_obj, kc, carb, prot, fat):
		self.flist = foodlist_obj.foodmap
		self.allowed_kc = kc
		self.allowed_carb = carb
		self.allowed_prot = prot
		self.allowed_fat = fat

		

		self.suggestSomething()


	def suggestSomething(self):
		suggestSingles()
		suggestPortions()


	def suggestSingles(self):
		# Filter singles again for kc limit
		self.singles = dict((x,v) for x,v in singles.iteritems()\
 if len(v.unit)>2\
 and v.kC < self.allowed_kc\
 and v.carb < self.allowed_carb\
 and v.fat < self.allowed_fat\
 and v.prot < self.allowed_prot)
		
		for x,v in self.singles.iteritems():
			print x, v.printout()


	def suggestPortions(self):
		portions = dict((x,v) for x,v in self.flist.iteritems()\
 if len(v.unit)<=2)\
 


	def checkAvail(self, perc):
		found=[]

w = FoodList()
s = Suggest(w, 100,5,50,50)
