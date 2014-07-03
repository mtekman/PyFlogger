#!/usr/bin/env python

from FoodLogger import *

class Suggest:

	def sortOpts(self, num=15):
		
		def perSort(x):
			yem = x[1]
			f = float(yem.fat)
			p = float(yem.prot)
			

			pff = (f - self.allowed_fat)/f
			ppp = (p - self.allowed_prot)/p

			return pff + ppp

#			input_ratio = self.allowed_fat / self.allowed_prot
			
#			ratio = ((f/p)/input_ratio) if self.allowed_fat >= self.allowed_prot else ((p/f)*input_ratio)
#			return ratio + 0.1*yem.carb.fibre


		for x,v in self.singles.iteritems():
			self.portions[x] = v

		sorted_ports = sorted(self.portions.iteritems(), key=perSort, reverse=True)

		Yemek.printFullHeader()
		count = 0
		for x,v in sorted_ports:
			if count==num:break
			count += 1
			print v.printout(pre="%2d: " % count)



	def __init__(self, foodlist_obj, kc, carb_obj, prot, fat, tag=""):
		self.flist = foodlist_obj.foodmap
		self.allowed_kc = kc
		self.allowed_carb = carb_obj
		self.allowed_prot = prot
		self.allowed_fat = fat
		self.wanted_tag = tag



	#This is more for my own curiousity
	def lowCalHighPF(self, num=15):
		
		def makeit(x):
			yem = x[1]
			f = float(yem.fat)
			p = float(yem.prot)
			kc = float(yem.kC)

			return 1/((kc/p) + (kc/f))


		sorted_ports = sorted(self.flist.iteritems(), key=makeit, reverse=True)

		Yemek.printFullHeader()
		count = 0
		for x,v in sorted_ports:
			if count==num:break
			count += 1
			print v.printout(pre="%2d: " % count)
	



	def suggestSomething(self):
		outnow = (' '*(Yemek.buffer-8)) + "Allow :   %s" % Yemek.outformat
		outnow = '\n'+'%'.join(outnow.split('%')[:-2])+'\n'
			
		print outnow % (
				int(self.allowed_kc), 
				self.allowed_carb.total, self.allowed_carb.fibre, self.allowed_carb.sugar, self.allowed_carb.bad,
				self.allowed_prot,
				self.allowed_fat)
		
		self.suggestSingles()
		self.suggestPortions()
		self.sortOpts()


	def suggestSingles(self):
		# Filter singles again for kc limit
		self.singles = dict((x,v) for x,v in self.flist.iteritems()\
 if len(v.unit)>2\
 and ((
       ( (self.wanted_tag in v.tags.tags) and (  (v.fat/v.carb.bad > 1) or (v.prot/v.carb.bad > 1)  )   )
      )\
 if (self.wanted_tag!="") else True)\
 and v.kC < self.allowed_kc\
 and v.carb.bad < self.allowed_carb.bad\
 and v.fat < self.allowed_fat\
 and v.prot < self.allowed_prot)
		

	def suggestPortions(self):
		
		portions = dict((x,v) for x,v in self.flist.iteritems() if len(v.unit)<=2)	# g, ml, etc
		self.portions = {}
		
		#scale portions to a minimum, and then chuck out the unrealistic ones
		for name in portions:
			yem = portions[name]

			if self.wanted_tag!="":
				if self.wanted_tag not in yem.tags.tags:continue

			amount_to_scale = float(self.allowed_kc)/yem.kC
			
#			if amount_to_scale == 0:
#				continue

			#nearest round fraction
			if amount_to_scale < 1:
				temp_scale = int(float(1)/amount_to_scale)
				amount_to_scale = float(1)/temp_scale
			
			new_scale = yem.scaled(amount_to_scale)
			
			
#			if new_scale.carb.bad > self.allowed_carb.bad:continue
			
			if new_scale.prot <= 0.1 and self.allowed.prot >=0:continue
			
			if new_scale.unit == 'g':
				if new_scale.per < 20.0 or new_scale.per > 350:
					continue

			if new_scale.unit == 'ml':
				if new_scale.per < 100.0 or new_scale.per > 1000:
					continue
			
			self.portions[name] = new_scale






#w = FoodLogger()
#w.makeTotals(w.date)
#p = w.pie
#s = Suggest(w.foodlist, p.macro_kc, p.macro_carb, p.macro_prot, p.macro_fat)
#s = Suggest(w.foodlist, 300, p.carb_total, p.protein_total, p.fat_total)
