#!/usr/bin/env python

# Each Yemek object has a single Carb and Portion class attached to it
import sys

class Carb:
	def __init__(self, carb, fibre, sugar):
		self.fibre = float(fibre)
		self.sugar = float(sugar)

		self.total = float(carb)
		real_total = self.fibre + self.sugar
		
		if self.total < real_total:
			self.total = real_total
		
		self.bad = self.total - self.fibre
		
#		diff = total - carb
#		if diff<0:diff *=-1
#		diff = float(diff)/self.total
#		
#		if diff>0.1:
#			print >> sys.stderr, "DOES NOT ADD UP", carb, fibre, sugar, diff
#			exit(-1)

	# override multiplier
	def multiply(self, x):
		self.fibre *= x
		self.sugar *= x
		self.total *= x
		self.bad *= x
	
#	__rmul__ = __lmul__

	def add(self, other):
		self.fibre += other.fibre
		self.sugar += other.sugar
		self.total += other.total
		self.bad += other.bad
	
#	__radd__ = __ladd__
	
	def sub(self, other):
		self.fibre -= other.fibre
		self.sugar -= other.sugar
		self.total -= other.total
		self.bad -= other.bad
	
#	__rsub__ = __lsub__



class Portion:
	def __init__(self):
		self.avail = {}
	
	def insert(self, name, calorie):
		
		name = name.strip()

		if name in self.avail:
			if self.avail[name] != calorie:
				print >> sys.stderr, "Portion contradiction:", name, self.avail[name], calorie
		else:
			self.avail[name] = calorie


class Yemek:
	buffer = 30
	outformat = "%5d  %5.1f [%5.1f,%5.1f] = %4.1f  %4.1f  %4.1f  %5.1f %s"
	
	headformat = ""
	c = 0
	while c < len(outformat):
		out = outformat[c]
		if out=='.':
			c += 2
			continue
			
		elif out in ['d','f']:
			out = "s"

		headformat += out
		c += 1
	
#	print headformat
	
	def __init__(self, name, kC, (carb, fibre, sugar), prot, fat, per, unit, amount=0, url=""):
		self.name = name
		self.kC = int(kC)
		self.carb = Carb(carb, fibre, sugar)
		self.prot = float(prot)
		self.fat = float(fat)
		self.portions = Portion()

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

	def printout(self,header=False, buffer=0, pre="*", carbinfo=True):
		if buffer ==0:
			buffer=Yemek.buffer

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

			while len(joiner+fword) < buffer:
				joiner += fword+' '
				del words[0]
				if len(words)==0:break
				fword = words[0]

			name_split.append( '  '+joiner )
		name_split[0] = (pre+name_split[0][1:]).strip()

		fill = buffer-len(name_split[0])+1
		outname = name_split[0]+(' '*fill)

		if carbinfo:
			form = "%s|"+Yemek.outformat
			text += form % (
				outname, int(self.kC), self.carb.total, 
				self.carb.fibre, self.carb.sugar, self.carb.bad,
				self.prot, self.fat, self.per, self.unit)
#		else:
#			text += "%s\t%d\t%.1f\t%.1f\t%.1f\t%.1f\t%s" % (
#				outname, int(self.kC), self.carb.total,
#				self.prot, self.fat, self.per, self.unit)

		if len(name_split)>0:
			del name_split[0]
		while len(name_split)>0:
			text += "\n%s" % name_split[0]
			del name_split[0]

		return text


	@staticmethod
	def printFullHeader(buffer=0, carbinfo=True):
		if buffer ==0:buffer=Yemek.buffer
		hhh = Yemek.printheader(buffer, carbinfo)
		print hhh
		print '-' * buffer, '|', '-' * (len(hhh)-buffer)
		print ' ' * buffer, '|'


	@staticmethod
	def printheader(buffer=0, carbinfo=True):
		if buffer ==0:buffer=Yemek.buffer
		
		return ("%s |" + Yemek.headformat) % (
			(' '*buffer), "kC", "Carb", "Fibre", "Sugar", "Bad", "Prot", "Fat", "per", "unit"
			)


	def scaled(self, multip=1):
		if multip==1:
			multip = float(self.amount)/self.per

		# Dupe, never edit self
		selfy = Yemek(self.name, self.kC, (self.carb.total,self.carb.fibre,self.carb.sugar), self.prot, self.fat, self.per, self.unit)
		
		selfy.kC = int( selfy.kC * multip)
		selfy.carb.multiply(multip)
		selfy.prot *= multip
		selfy.fat *= multip
		selfy.per *= multip

		return selfy
