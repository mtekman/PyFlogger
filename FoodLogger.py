#!/usr/bin/env python

from Common import *

from FoodList import FoodList
from Yemek import Yemek, Carb
from copy import copy
from PieChart import PieChart

class FoodLogger:
	def __init__(self, 	file=abspath("../")+"/logs/keto_foodlog.txt",
				file2=abspath("../")+"/logs/targets.txt"):
		self.foodlog=[]
		self.path= file
		self.macrofile=file2
		self.foodlist = FoodList() 		# i.e. ref FoodList cobj
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

		datelist=[] # Not really used
		
		date = date[0:10]

		for line in f:
			if len(line) < 5:
				continue
			ddate, amount, name = line.split('\t')
			ddate = ddate[0:10]
			
			datelist.append(ddate)

			if date == ddate:
				#Find food if date matches
				food = copy(self.foodlist.foodmap[name.strip()])			
				food.amount = amount
				self.foodlog.append(food)
		f.close()
		
		return datelist
	
	

	def showTotals(self,date, showPie=True):
		self.makeTotals(date, showPie, printme=True)		


	def makeTotals(self,date, showPie=False, printme=False):
		self.read(date)
		
		kC_total=0
		carb_total=Carb(0,0,0)
		protein_total=0
		fat_total=0

		if len(self.foodlog)==0:
			print >> sys.stderr, "nothing logged for date: %s" % date
			prevD = previousDay(ymd2secs(date.split('/')))
			if ynprompt("Print day before that (%s)? " % prevD):
				return self.makeTotals(prevD, showPie, printme)

		if printme:
			print >> sys.stderr, '\n'*10
			Yemek.printFullHeader()
		
		for y in self.foodlog:
			scyem = y.scaled()
			
			kC_total += scyem.kC
			carb_total.add(scyem.carb)
			protein_total += scyem.prot
			fat_total += scyem.fat

			if printme:
				print >> sys.stderr, scyem.printout()

		self.pie = PieChart(carb_total, protein_total, fat_total, kC_total, self.macrofile,
			Yemek.buffer-8, 8, printme=showPie)

		return kC_total, carb_total, protein_total, fat_total



	def log(self, name=""):
		if name=="":
			name = raw_input("Food: ").strip().lower()
		name = self.foodlist.info(name) # find match
		
		am = -1
		unit_set = -1
		yem_obj = self.foodlist.foodmap[name]
		init_per = equiv_per = float(yem_obj.per)

		if len(yem_obj.portions.avail)!=0:
			if ynprompt("\nNote: Portions Available -- View?"):
			
				ports = yem_obj.portions.avail.keys()
				port_res = -1
	
				happy = False
				while not happy:
					port_res = choice(ports)
					if port_res == -1:break
					happy = ynprompt("Accept this portion?")

				if port_res!=-1:
					kC = yem_obj.portions.avail[port_res]
					unit_set = float(kC)/yem_obj.kC
					equiv_per *= unit_set
					print "kc for this:", kC, "yem kc:",yem_obj.kC, "fract:", unit_set, "equiv per=", equiv_per


		# Am is set by port_res, so no need to check port_res here
		if unit_set!=-1 or am==-1:
			am_amount = fraction(raw_input("\nAmount consumed (fraction or amount in g)? ").strip())
			scale = am_amount/equiv_per if am_amount > 20 else am_amount

			am = scale * equiv_per


			print "unit_set=", unit_set, " am_amount=", am_amount

		dater = "%04d/%02d/%02d--%02d:%02d" % localtime()[0:5]

		f=open(self.path,'a')
		print >> f, "%s\t%.1f\t%s" % (dater,am,name)
		f.close()
		
		print >> sys.stderr, "\n\n"
		self.showTotals(self.date)
