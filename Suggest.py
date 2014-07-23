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


	def minimumScale(self, yem):
		kc_scale = float(self.allowed_kc)/yem.kC
		yem = yem.scaled(kc_scale)

		if yem.carb.bad > self.allowed_carb.bad:
			carb_scale = float(self.allowed_carb.bad)/yem.carb.bad
			try:
				scale = float(1)/( int( float(1)/carb_scale ) )
			except ZeroDivisionError:
				scale = 0.1
			yem = yem.scaled(scale)
		if yem.fat > self.allowed_fat:
			fat_scale = float(self.allowed_fat)/yem.fat
			scale = float(1)/( int( float(1)/fat_scale ) )
			yem = yem.scaled(scale)
		if yem.prot > self.allowed_prot:
			protein_scale = float(self.allowed_prot)/yem.prot
			scale = float(1)/( int( float(1)/protein_scale ) )
			yem = yem.scaled(scale)

		return yem


	def suggestSingles(self):
		# Filter singles again for kc limit
		singles1 = dict((x,v) for x,v in self.flist.iteritems()\
 if len(v.unit)>2 and (
  (  (v.fat/v.carb.bad > 1) or (v.prot/v.carb.bad > 1) )  
  if (self.wanted_tag=="")\
  else (self.wanted_tag in v.tags.tags)
  ))

		self.singles={}
		for x,y in singles1.iteritems():
			v = self.minimumScale(y)

#			if (v.kC < self.allowed_kc 
#				 and v.carb.bad < self.allowed_carb.bad
#				 and v.fat < self.allowed_fat
#				 and v.prot < self.allowed_prot):
			self.singles[x]=v

	
	
	

	def suggestPortions(self):
		
		portions = dict((x,v) for x,v in self.flist.iteritems() if len(v.unit)<=2)	# g, ml, etc
		self.portions = {}
		
		#scale portions to a minimum, and then chuck out the unrealistic ones
		for name in portions:
			yem = portions[name]

			if self.wanted_tag!="":
				if not self.wanted_tag in yem.tags.tags:continue

			new_scale = self.minimumScale(yem)
						
			if new_scale.prot <= 0.1 and self.allowed_prot >=0:continue
			
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
