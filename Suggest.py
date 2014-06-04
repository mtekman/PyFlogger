#!/usr/bin/env python

from FoodLogger import *

class Suggest:

	def __init__(self, foodlist_obj, kc, carb, prot, fat):
		self.flist = foodlist_obj.foodmap
		self.allowed_kc = kc
		self.allowed_carb = carb
		self.allowed_prot = prot
		self.allowed_fat = fat

		self.suggestSomething()


	def suggestSomething(self):
		self.suggestSingles()
		self.suggestPortions()
		self.sortOpts()


	def suggestSingles(self):
		# Filter singles again for kc limit
		self.singles = dict((x,v) for x,v in self.flist.iteritems()\
 if len(v.unit)>2\
 and v.kC < self.allowed_kc\
 and v.carb < self.allowed_carb\
 and v.fat < self.allowed_fat\
 and v.prot < self.allowed_prot)
		

	def suggestPortions(self):
		
		portions = dict((x,v) for x,v in self.flist.iteritems() if len(v.unit)<=2)	# g, ml, etc
		self.portions = {}
		
		#scale portions to a minimum, and then chuck out the unrealistic ones
		for name in portions:
			yem = portions[name]
			amount_to_scale = float(self.allowed_kc)/yem.kC
			
#			if amount_to_scale < 0:
#				continue

			#nearest round fraction
			if amount_to_scale < 1:
				temp_scale = int(float(1)/amount_to_scale)
				amount_to_scale = float(1)/temp_scale
			
			new_scale = yem.scaled(amount_to_scale)
			
			if new_scale.per < 20.0:
				continue
			
			self.portions[name] = new_scale



	def sortOpts(self):

		def perSort(x):
			return float(x[1].prot)

		for x,v in self.singles.iteritems():
			self.portions[x] = v

		sorted_ports = sorted(self.portions.iteritems(), key=perSort, reverse=True)

		print Yemek.printheader()
		for x,v in sorted_ports:
			print v.printout()





#w = FoodLogger()
#w.makeTotals(w.date)
#p = w.pie
#s = Suggest(w.foodlist, p.kc_total, p.carb_total, p.protein_total, p.fat_total)
#s = Suggest(w.foodlist, 300, p.carb_total, p.protein_total, p.fat_total)
