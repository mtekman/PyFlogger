#!/usr/bin/env python

class Yemek:

	def __init__(self, name, kC, carb, prot, fat, per, unit, amount=0):
		self.name = name
		self.kC = float(kC)
		self.carb = float(carb)
		self.prot = float(prot)
		self.fat = float(fat)
		self.per = float(per)
		self.unit = unit.strip()
		self.amount = float(amount)

	@staticmethod
	def printheader():
		return "     \tkC\tC\tP\tF\tper\tunit\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

	def printout(self,header=False):
		text=""
		if header:
			text=Yemek.printheader()+'\n'

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
