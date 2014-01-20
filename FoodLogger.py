#!/usr/bin/env python

from os import path
from time import localtime as time
import sys

from FoodList import FoodList
from Yemek import Yemek
from copy import copy

class FoodLogger:
	def __init__(self, file=path.expanduser("~/")+".config/keto_foodlog.txt"):
		self.foodlog=[]
		self.path= file
		self.foodlist = FoodList() # i.e. ref FoodList cobj
		self.date = "%04d/%02d/%02d--%02d:%02d" % time()[0:5]
		self.read(self.date)

	# any date
	def read(self,date):
		try:
			f=open(self.path,'r')
		except IOError:
			f=open(self.path,'w')
			f.write(" ")
			f.close()
			return
		
		f.readline()   # Strip Header

		for line in f:
			if len(line) < 5:
				continue
			ddate, amount, name = line.split('|')
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

		print >> sys.stderr, Yemek.printheader()

		for y in self.foodlog:
			scale = y.amount 

			kC_total += y.kC
			carb_total += y.carb
			protein_total += y.prot
			fat_total += y.fat

			print >> sys.stderr, y.printout(False)
		print >> sys.stderr, "Totals:\t%s\t%s\t%s\t%s" % (kC_total, carb_total, protein_total, fat_total)


	def log(self):
		name = raw_input("Food: ").strip()
		name = self.foodlist.info(name) # find match
		
		am = float(raw_input("amount consumed? ").strip())
		dater = "%04d/%02d/%02d--%02d:%02d" % time()[0:5]

		f=open(self.path,'a')
		print >> f, "%s|%f|%s" % (dater,am,name)
		f.close()
		
		self.showTotals(self.date)

w=FoodLogger()
w.log()
#w.showTotals(w.date)
