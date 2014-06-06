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
			
#			if amount_to_scale == 0:
#				continue

			#nearest round fraction
			if amount_to_scale < 1:
				temp_scale = int(float(1)/amount_to_scale)
				print >> sys.stderr, amount_to_scale
				amount_to_scale = float(1)/temp_scale
			
			new_scale = yem.scaled(amount_to_scale)
			
			if new_scale.unit == 'g':
				if new_scale.per < 20.0 or new_scale.per > 350:
					continue

			if new_scale.unit == 'ml':
				if new_scale.per < 100.0 or new_scale.per > 1000:
					continue
			
			self.portions[name] = new_scale



	def sortOpts(self):

		def perSort(x):
			yem = x[1]
			f = float(yem.fat)
			c = float(yem.carb)

			if f == 0:f = 0.0001
			if c == 0:c = 0.0001

			p_f_rat = float(yem.prot)/f
			return p_f_rat/c


		for x,v in self.singles.iteritems():
			self.portions[x] = v

		sorted_ports = sorted(self.portions.iteritems(), key=perSort, reverse=True)

		print Yemek.printheader()
		for x,v in sorted_ports:
			print v.printout()





#w = FoodLogger()
#w.makeTotals(w.date)
#p = w.pie
#s = Suggest(w.foodlist, p.macro_kc, p.macro_carb, p.macro_prot, p.macro_fat)
#s = Suggest(w.foodlist, 300, p.carb_total, p.protein_total, p.fat_total)
