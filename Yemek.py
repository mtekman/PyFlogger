#!/usr/bin/env python

class Yemek:
	buffer = 30

	def printout(self,header=False, buffer=0):
		pre=""
		if buffer ==0:
			buffer=Yemek.buffer
			pre="* "

		text=""
		outname=self.name

		if header:
			text=Yemek.printheader(buffer)+'\n'

		name_split=[]
		printname = self.name
		words = printname.split()

		while len(words) > 0:
			fword = words[0]
			joiner = ""

			while len(joiner+fword+' ') < buffer:
				joiner += fword+' '
				del words[0]
				if len(words)==0:break
				fword = words[0]

			name_split.append( '  '+joiner )
		name_split[0] = (pre+name_split[0][1:]).strip()

		fill = buffer-len(name_split[0])
		outname = name_split[0]+(' '*fill)

		text += "%s\t%d\t%.1f\t%.1f\t%.1f\t%.1f\t%s" % (
			outname, int(self.kC), self.carb,
			self.prot, self.fat, self.per, self.unit)

#		text += "%s\t%.3s\t%.3s\t%.3s\t%.3s\t%.3s\t%.2s" % (
#			outname, int(self.kC), self.carb,
#			self.prot, self.fat, self.per, self.unit)

		if len(name_split)>0:
			del name_split[0]
		while len(name_split)>0:
			text += "\n%s" % name_split[0]
			del name_split[0]

		return text
	

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
		if buffer ==0:buffer=Yemek.buffer
		return (' '*buffer)+"\tkC\tC\tP\tF\tper\tunit\n"


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
