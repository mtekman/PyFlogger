#!/usr/bin/env python

class Yemek:

	def __init__(self, name, kC, carb, prot, fat, per, unit, amount=0):
		self.name = name
		self.kC = int(kC)
		self.carb = int(carb)
		self.prot = int(prot)
		self.fat = int(fat)
		self.per = int(per)
		self.unit = unit
		self.amount = int(amount)

	def printout(self,header=True, headeronly=False):
		text=""
		if header:
			text="\t\tkCal\tCarb\tProt\tFat\tPer\n"
			if headeronly:
				return text

		text += "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
			self.name, self.kC, self.carb,
			self.prot, self.fat, self.per, self.unit)
		return text
	
	def scaled(self):
		scalef = Yemek(self) # dupe
		multip = float(amount)/self.per	
		
		scalef.kC *= multip
		scalef.carb *= multip
		scalef.prot *= multip
		scalef.fat *= multip
		scalef.per *= multip

		return scalef;

