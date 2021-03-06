#!/usr/bin/env python

# Each Yemek object has a single Carb, Portion, and Tag class attached to it
import sys
import Common

#
# TODO:Maybe create a tag map, that for each insert points to a specific Yemek object? Filtering would be easier...
#

class Tags:
	delim='##'

	global_tags={}

	def __init__(self):
		self.tags={}

	def insertList(self, lists):
		for tag in lists:self.insert(tag)


	def insert(self, tag):
		if len(tag)==0:return
		if not tag in self.tags:
			self.tags[tag] = 1
		if not tag in Tags.global_tags:
			Tags.global_tags[tag] = 1
		else:
			Tags.global_tags[tag] += 1

	def printout(self):
		return Tags.delim.join(list(self.tags.keys()))


	@staticmethod
	def tagprompt():
		get_avail_tags = Tags.popcon()
		if len(get_avail_tags) == 0:
			return -1

		return Common.userlistprompt("Attach a tag? Avail:", get_avail_tags)


	@staticmethod
	def popcon():
		def treas(keyd):
			return Tags.global_tags[keyd]

		return [x for x in sorted(list(Tags.global_tags.keys()), key=treas, reverse=True) if Tags.global_tags[x]>1]


class Carb:
	def __init__(self, carb, fibre, sugstar):
		self.fibre = float(fibre) + Yemek.nonz
		self.sugstar = float(sugstar) + Yemek.nonz

		self.total = float(carb) + Yemek.nonz
		real_total = self.fibre + self.sugstar

		if self.total < real_total:
			self.total = real_total

		self.bad = (self.total - self.fibre) + Yemek.nonz


	# override multiplier
	def multiply(self, x):
		self.fibre *= x
		self.sugstar *= x
		self.total *= x
		self.bad *= x

#	__rmul__ = __lmul__

	def add(self, other):
		self.fibre += other.fibre
		self.sugstar += other.sugstar
		self.total += other.total
		self.bad += other.bad

#	__radd__ = __ladd__

	def sub(self, other):
		self.fibre -= other.fibre
		self.sugstar -= other.sugstar
		self.total -= other.total
		self.bad -= other.bad

#	__rsub__ = __lsub__



class Portion:
	start_delim="$$"
	end_delim="::"

	def __init__(self):
		self.avail = {}


	@staticmethod
	def printheader(lbuff):
		return Common.makewhitespace(lbuff)+"| Other Portions"


	def printout(self, lbuff):
		strr = Common.makewhitespace(lbuff)+'|'
		for p,v in self.avail.items():
			strr += Portion.start_delim + p + Portion.end_delim +str(v)
		return strr


	def insert(self, name, calorie):
		name = name.strip()

		if name in self.avail:
			if self.avail[name] != calorie:
				RESULT("Portion contradiction:", name, self.avail[name], calorie, file=sys.stderr)
		else:
			self.avail[name] = calorie


class Yemek:
	nonz = 0.00001
	buffer = 30
	outformat = "%5d  %6.1f [%6.1f,%6.1f] = %5.1f  %5.1f  %5.1f  %5.1f %s"

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

	def __init__(self, name, kC, carb_obj, prot, fat, per, unit, amount=0, url=""):

		self.name = name
		self.kC = int(kC)
		self.carb = carb_obj
		self.prot = float(prot) + Yemek.nonz
		self.fat = float(fat) + Yemek.nonz

		self.portions = Portion()
		self.tags = Tags()

		try:
			self.per = float(per)
		except ValueError:
			up,down = [float(x) for x in per.split('/')]
			self.per = up/down

		self.unit = unit.strip()
		for word in self.name.split():
			subword = word[1:-2]
			if len(subword)>4:
				tokes = self.unit.split()
				for u in range(len(tokes)):
					if subword in tokes[u]:
						tokes[u] = ""
				self.unit = " ".join(tokes).strip()

		self.amount = float(amount)
		self.url = url
		self.hour = -1


	def printout(self,header=False, buffer=0, pre="*",
			portions_buff=0, tags=False):
		if buffer ==0:
			buffer=Yemek.buffer

		text=""
		outname=self.name

		if header:
			text=Yemek.printheader(buffer)+'\n'

		name_split=[]
		printname = self.name
		words = printname.split()

		first_pre = pre
		pre = ' '*len(pre)

		# Fit words on a line, rather than an uneven split
		while len(words) > 0:
			fword = words[0]
			joiner = ""

			while len(pre+joiner+fword) < buffer:
				joiner += fword+' '
				del words[0]
				if len(words)==0:break
				fword = words[0]

			line = pre+(joiner.strip())
			name_split.append(line)

		#first line
		name_split[0] = first_pre+(name_split[0].strip())

		#Fill remainder of first line until data
		fill = buffer-len(name_split[0])+1
		outname = name_split[0]+(' '*fill)

		form = "%s|"+Yemek.outformat  #template formatting
		text += form % (
				outname, int(self.kC), self.carb.total,
				self.carb.fibre, self.carb.sugstar, self.carb.bad,
				self.prot, self.fat, self.per, self.unit)

		if portions_buff!=0:
			text += self.portions.printout(portions_buff)

		if tags:
			text += '|'+self.tags.printout()

		if len(name_split)>0:
			del name_split[0]
		while len(name_split)>0:
			text += "\n%s%s|" % (name_split[0], (' '*(buffer-len(name_split[0])+1)))
			del name_split[0]

		return text


	@staticmethod
	def printFullHeader(buffer=0):
		if buffer ==0:buffer=Yemek.buffer
		hhh = Yemek.printheader(buffer)
		print(hhh)
		print('-' * buffer, '|', '-' * (len(hhh)-buffer))
		print(' ' * buffer, '|')


	@staticmethod
	def printheader(buffer=0, portions_buff=0, tags=False):
		if buffer ==0:buffer=Yemek.buffer

		strr= ("%s |" + Yemek.headformat) % (
			(' '*buffer), "kC", "Carb", "Fibre", "Sg/St", "Bad", "Prot", "Fat", "per", "unit"
			)

		if portions_buff!=0:
			strr += Portion.printheader(portions_buff)

		if tags:
			strr += "| Tags"
		return strr


	def scaled(self, multip=1):
		if multip==1 and self.amount!=0:
			multip = float(self.amount)/self.per

		# Dupe, never edit self
		selfy = Yemek(self.name, self.kC, Carb(self.carb.total,self.carb.fibre,self.carb.sugstar), self.prot, self.fat, self.per, self.unit)

		selfy.kC = int( selfy.kC * multip)
		selfy.carb.multiply(multip)
		selfy.prot *= multip
		selfy.fat *= multip
		selfy.per *= multip

		return selfy

	@staticmethod
	def roughlyEqual(one,two, thresh=0.1):
		three = one - two
		if three < 0:three *=-1
		return three < thresh

	# Overload method
	def __eq__(self, other):
		if isinstance(other, Yemek):
           #Debug
	#		print Yemek.roughlyEqual(self.kC, other.kC)
	#		print Yemek.roughlyEqual(self.prot, other.prot)
	#		print Yemek.roughlyEqual(self.fat, other.fat)
	#		print Yemek.roughlyEqual(self.carb.fibre, other.carb.fibre)
	#		print Yemek.roughlyEqual(self.carb.sugstar, other.carb.sugstar)

			return (Yemek.roughlyEqual(self.kC, other.kC)
				and Yemek.roughlyEqual(self.prot, other.prot)
				and Yemek.roughlyEqual(self.fat, other.fat)
				and Yemek.roughlyEqual(self.carb.fibre, other.carb.fibre)
				and Yemek.roughlyEqual(self.carb.sugstar, other.carb.sugstar) )

		return False
