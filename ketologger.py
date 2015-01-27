#!/usr/bin/env python

import sys
from FoodLogger import FoodLogger
from Weight import WeightLog
from Plotter import *
from Suggest import Suggest
from Common import daysSince, previousDay

class Args:

	def usage(self):
		print >> sys.stderr, '''
Records progress during keto; weight and food consumption
		
		%s <command> <task> [OPTS]

commands:  	insert, remove, list, plot, suggest, lookup, test, cleartest
tasks:    	weight, food

OPTS:		foodname, lbs, lowcal, tag

''' % sys.argv[0].split('/')[-1]
		exit(-1)

	def __init__(self, argv):

		if len(argv)<3:
			self.usage()
		
		self.argv = argv
		self.parse()
		self.callProgs()


	def parse(self):
		self.insert = False
		self.remove = False
		self.list = False
		self.plot = False
		self.suggest = False
		self.test = 0
		self.food = self.weight = False
		self.task = ""
		
		
		arg=self.argv[1].lower()
		if arg.startswith('insert') or arg.startswith('log'):
			self.insert=True
		elif arg.startswith('remove') or arg.startswith('delete'):
			self.remove=True
		elif arg.startswith('list'):
			self.list=True
		elif arg.startswith('plot'):
			self.plot=True
		elif arg.startswith('suggest'):
			self.suggest=True
		elif arg.startswith('test'):
			self.test=1
			self.insert=True
		elif arg.startswith('cleartest'):
			self.test=2
	
		arg=self.argv[2].lower()	
		if arg.startswith('food'):
			self.food=True
		elif arg.startswith('weight'):
			self.weight=True

		self.opts = " ".join(self.argv[3:])
	
	
	
	def callProgs(self):

		if self.weight:
			wl = WeightLog()
		
			if self.insert:
				wl.checkGaps()
				return
			
			if self.remove:
				print "Not implemented"
				return

			if self.list:
				wl.display( wl.weightlogmap.keys()[0] )
				return
			
			if self.plot:
				xy = XYGraph(False)

				startdate=""
				for date in sorted(wl.weightlogmap.keys()):
				
					if startdate=="":
						startdate=date
						continue
				               
					days_since = daysSince(startdate,date)
					total = days_since

#					print date,total
				                     
					w = wl.weightlogmap[date]
					if w.morn>0:
						xy.addPoint(total,w.morn,"x")
					if w.night>0:
						xy.addPoint(total+.5,w.night,"x")
				                                          
				Printer(xy)
				return                                       

			print "Nothing to do"
			return


		if self.food:
			fl = FoodLogger(testmode=self.test)
			
			if self.insert:
				fl.log(self.opts)
				return
			
			if self.remove:
				print "Not implemented"
				return
			
			if self.list:
				date = fl.date
				if self.opts!="":
					count = int(self.opts)
					while count >0:
						date = previousDay(date)
						count -= 1

				fl.showTotals(date, showPie=True)
				return

			if self.plot:
				print "Not implemented"
				return                                       


			if self.suggest:
				fl.makeTotals(fl.date)
				p = fl.pie
				lowcal=False
				tag=""
				try:
					p.allow_kc = int(self.opts)
				except ValueError:
					opts = self.opts.lower().split()
					if len(opts)!=1:
						tag= ' '.join(opts[:-1])
						p.allow_kc = int(opts[-1])
					else:
						tag=self.opts

					if tag=="lowcal":
						lowcal=True
					pass

				s = Suggest(fl.foodlist,
					p.allow_kc, 
					p.allow_carb,
					p.allow_prot, 
					p.allow_fat, 
					tag)

				if lowcal:s.lowCalHighPF()
				else:s.suggestSomething()
				return


try:
	Args(sys.argv)
except KeyboardInterrupt:
	print "\nQuit"
	exit(-1)
