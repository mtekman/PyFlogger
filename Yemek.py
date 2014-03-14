#!/usr/bin/env python

class Yemek:

	def __init__(self, name, kC, carb, prot, fat, per, unit, amount=0, url=""):
		self.name = name
		self.kC = int(kC)
		self.carb = float(carb)
		self.prot = float(prot)
		self.fat = float(fat)
		try:
			self.per = float(per)
		except ValueError:
			up,down = map(lambda x: float(x), per.split('/'))
			self.per = up/down

		self.unit = unit.strip()
		for word in self.name.split():
			subword = word[1:-2]
			if len(subword)>4:
				tokes = self.unit.split()
				for u in xrange(len(tokes)):
					if subword in tokes[u]:
						tokes[u] = ""
				self.unit = " ".join(tokes).strip()

		self.amount = float(amount)
		self.url = url

	@staticmethod
	def printheader(buffer=0):
		return (' '*buffer)+"\tkC\tC\tP\tF\tper\tunit\n"

	def printout(self,header=False, buffer=0, maxsplit=-1):
		text=""
		outname=self.name
		
		if header:
			text=Yemek.printheader()+'\n'

		name_split=[]
		ind=0
		printname = self.name

		if maxsplit!=-1:
			while len(printname) > maxsplit:
				name_split.append( printname[ind:ind+maxsplit] )
				ind = maxsplit
				printname = printname[ind:]
			name_split.append(printname)
		else:	
			name_split.append(printname)

		if buffer!=0:
			fill = buffer-len(name_split[0])
			outname = name_split[0]+(' '*fill)

		text += "%s\t%d\t%.1f\t%.1f\t%.1f\t%.1f\t%s" % (
			outname, int(self.kC), self.carb,
			self.prot, self.fat, self.per, self.unit)

		if len(name_split)>0:
			del name_split[0]
		while len(name_split)>0:
			text += "\n%s" % name_split[0]
			del name_split[0]

		return text
	
	def scaled(self, multip=1):
		if multip==1:
			multip = float(self.amount)/self.per

		# Dupe, never edit self
		selfy = Yemek(self.name, self.kC, self.carb, self.prot, self.fat, self.per, self.unit)
		
		selfy.kC = int( selfy.kC * multip)
		selfy.carb *= multip
		selfy.prot *= multip
		selfy.fat *= multip
		selfy.per *= multip

		return selfy
