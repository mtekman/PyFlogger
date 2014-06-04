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
#		self.suggestSingles()
		self.suggestPortions()


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
		
		def perSort(x):
			return float(x[1].per)
		
		portions = dict((x,v) for x,v in self.flist.iteritems() if len(v.unit)<=2)	# g, ml, etc
		self.portions = {}
		
		#scale portions to a minimum, and then chuck out the unrealistic ones
		for name in portions:
			yem = portions[name]
			
			amount_to_scale = float(self.allowed_kc)/yem.kC
			#nearest round fraction
			temp_scale = int(float(1)/amount_to_scale)
			amount_to_scale = float(1)/temp_scale
			
			new_scale = yem.scaled(amount_to_scale)
			
			if new_scale.per < 20.0:
				continue
			
			self.portions[name] = new_scale

		sorted_ports = sorted(self.portions.iteritems(), key=perSort, reverse=True)

		for x,v in sorted_ports:
			print v.printout()


	def checkAvail(self, perc):
		found=[]

w = FoodList()
s = Suggest(w, 100,5,50,50)
