#!/usr/bin/env python

import sys
from FoodLogger import FoodLogger
from Weight import WeightLog
from Plotter import *

class Args:

	def usage(self):
		print >> sys.stderr, '''
Records progress during keto; weight and food consumption
		
		%s <command> <task> [OPT]

commands:  	insert, remove, list, plot
tasks:    	weight, food

OPTS:		foodname, lbs

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
	
		arg=self.argv[2].lower()	
		if arg.startswith('food'):
			self.food=True
		elif arg.startswith('weight'):
			self.weight=True
	


	def callProgs(self):
		if self.weight:
			wl = WeightLog()
		
			if self.insert:
				wl.checkGaps()
				return
			
			if self.remove:
				print "Do nothing"
				return

			if self.list:
				wl.display( wl.weightlogmap.keys()[0] )
				return
			
			if self.plot:
				xy = XYGraph()

				startdate=""
				for date in sorted(wl.weightlogmap.keys()):
				
					if startdate=="":
						startdate=date
						continue
				               
					days_since = wl.daysSince(startdate,date)
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
			fl = FoodLogger()
			
			if self.insert:
				fl.log()
				return
			
			if self.remove:
				print "TODO"
				return
			
			if self.list:
				fl.showTotals(fl.date)
				return


a = Args(sys.argv)
