#!/usr/bin/env python

import sys
from FoodLogger import FoodLogger
from Weight import WeightLog

class Args:

	def usage(self):
		print >> sys.stderr, '''
Records progress during keto; weight and food consumption
		
		%s <command> <task> [OPT]

commands:  	insert, remove, list, plot
tasks:    	weight, food

OPTS:		foodname, lbs

''' % sys.argv.split('/')[-1]
	exit(-1)

	def __init__(self,argv):
		self.insert = False
		self.remove = False
		self.list = False
		self.task = ""

		arg=sys.argv[0]	
		if arg.startswith('insert'):
			self.insert=True
		elif arg.startswith('remove') or arg.startswith('delete'):
			self.remove=True
		elif arg.startswith('list'):
			self.list=True
		elif arg.startswith('plot'):
			self.plot=True
	
		arg=sys.argv[1].lower()	
		if arg.startswith('food'):
			self.insert=True
		elif arg.startswith('weight'):
			self.insert=True
		


	def parse(self):
		for arg in self.argv:
			if arg=="insert":
