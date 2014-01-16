#!/usr/bin/env python

class Yemek:
	def __init__(self, name, kC, carb, prot, fat, per, unit, amount=0):
		self.settokens([name, kC, carb, prot, fat, per, unit, amount])

	def __init__(self, line_data):
		self.settokens(line_data.split('\t'))

	def settokens(self, tokes):
		self.name = tokes[0].strip()
		self.kC = int(tokes[1].strip())
		self.carb = int(tokes[2].strip())
		self.prot = int(tokes[3].strip())
		self.fat = int(tokes[4].strip())
		self.per = int(tokes[5].strip())
		self.unit = tokes[6].strip()
		self.amount = "  "
		if len(tokes) == 8:
			self.amount = int(tokes[7].strip())

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

