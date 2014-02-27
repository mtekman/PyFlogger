#!/usr/bin/env python

class Yemek:

	def __init__(self, name, kC, carb, prot, fat, per, unit, amount=0, url=""):
		self.name = name
		self.kC = int(kC)
		self.carb = float(carb)
		self.prot = float(prot)
		self.fat = float(fat)
		self.per = float(per)
		self.unit = unit.strip()
		self.amount = float(amount)
		self.url = url

	@staticmethod
	def printheader():
		return "\tkC\tC\tP\tF\tper\tunit\n"

	def printout(self,header=False, buffer=0):
		text=""
		outname=self.name
		
		if header:
			text=Yemek.printheader()+'\n'

		if buffer!=0:
			fill = buffer-len(self.name)
			outname = self.name+(' '*fill)

#		text += "%s\t%d\t%4f\t%4f\t%4f\t%3f\t%s" % (
		text += "%s\t%d\t%s\t%s\t%s\t%s\t%s" % (
			outname, int(self.kC), self.carb,
			self.prot, self.fat, self.per, self.unit)
		return text
	
	def scaled(self):
		multip = float(self.amount)/self.per
		# Dupe, never edit self
		selfy = Yemek(self.name, self.kC, self.carb, self.prot, self.fat, self.per, self.unit)
		
		selfy.kC = int( selfy.kC * multip)
		selfy.carb *= multip
		selfy.prot *= multip
		selfy.fat *= multip
		selfy.per *= multip

		return selfy
