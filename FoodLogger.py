#!/usr/bin/env python

from Common import *

from FoodList import FoodList
from Yemek import Yemek
from copy import copy
from PieChart import PieChart

class FoodLogger:
	def __init__(self, file=abspath("../")+"/logs/keto_foodlog.txt",
						file2=abspath("../")+"/logs/keto_target_macros.txt"):
		self.foodlog=[]
		self.path= file
		self.foodlist = FoodList() # i.e. ref FoodList cobj
		self.date = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]

	# any date
	def read(self,date):
		try:
			f=open(self.path,'r')
		except IOError:
			f=open(self.path,'w')
			f.write("Date             \tAmn\tFood Name\n")
			f.close()
			return
		
		f.readline()   # Strip Header

		for line in f:
			if len(line) < 5:
				continue
			ddate, amount, name = line.split('\t')

			if date[0:10] == ddate[0:10]:
				#Find food if date matches
				food = copy(self.foodlist.foodmap[name.strip()])
				food.amount = amount
				self.foodlog.append(food)
		f.close()


	def showTotals(self,date):
		self.read(date)
		
		kC_total=0
		carb_total=0
		protein_total=0
		fat_total=0

		if len(self.foodlog)==0:
			print >> sys.stderr, "nothing logged for that day!"
			exit(-1)

		maxlen_foodname=len(reduce(lambda x,y: ( x if (len(x.name) > len(y.name)) else y ), self.foodlog).name)
		print >> sys.stderr, '\n'*10


		print >> sys.stderr, Yemek.printheader(buffer=maxlen_foodname)
		print >> sys.stderr, '-'*70
		
		for y in self.foodlog:
			scyem = y.scaled()
		
			kC_total += scyem.kC
			carb_total += scyem.carb
			protein_total += scyem.prot
			fat_total += scyem.fat

			print >> sys.stderr, scyem.printout(buffer=maxlen_foodname)

		PieChart(carb_total, protein_total, fat_total, kC_total, 
			maxlen_foodname-8, 8)
		
		self.foodlog = [] # clear until next


	def log(self, name=""):
		if name=="":
			name = raw_input("Food: ").strip().lower()
		name = self.foodlist.info(name) # find match
		
		am_amount = raw_input("\nAmount Consumed? ").strip()
		try:
			am = float(am_amount)
		except ValueError:
			spl = am_amount.split('/')
			am = float(spl[0])/float(spl[1])

		dater = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]

		f=open(self.path,'a')
		print >> f, "%s\t%.1f\t%s" % (dater,am,name)
		f.close()
		
		print >> sys.stderr, "\n\n"
		self.showTotals(self.date)

#w=FoodLogger()
#w.log()
#w.showTotals(w.date)
