#!/usr/bin/env python

import sys
from time import localtime as time
from os.path import abspath

class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night

class WeightLog:

	def __init__(self,file=abspath("../")+"/logs/keto_weightlog.txt"):
		self.weightlogmap={}
		self.path = file
		self.date = "%04d/%02d/%02d" % time()[0:3]
		self.read()
		
	def read(self):
                f=open(self.path,'r')
                
		f.readline()	#Skip header
		for weight in f:
			if len(weight)< 5:
				continue
			date, morn, nigh = weight.split('\t')
			self.weightlogmap[date] = Weight(int(morn),int(nigh))
		f.close()

	def write(self):
		f=open(self.path,'w')
		print >> f, "Date     \tMorn\tNight\n"	#header

		for date in sorted(self.weightlogmap.keys()):
			w = self.weightlogmap[date]
			print >> f, "%s\t%s\t%s" % (date, w.morn, w.night)
		f.close()


	def display(self):
		w = self.weightlogmap[self.date]
		print >> sys.stderr, '='*39
		print >> sys.stderr, "Date     \tMorn\tNight"	#print header
		print >> sys.stderr, "%s\t%d\t%d" % (self.date, w.morn, w.night)


	def log(self,lbls):
		#Weight exists for that date
		if self.date in self.weightlogmap:
			w = self.weightlogmap[self.date]

			if w.night==-1 and w.morn==-1:
        				self.weightlogmap[self.date].morn = lbls
	        			print >> sys.stderr, "[Logged Morning lb]"

			if w.night==-1 and w.morn!=-1:
					self.weightlogmap[self.date].night = lbls
	        			print >> sys.stderr, "[Logged Night lb]"
			else:
			        self.display()
				print >> sys.stderr, "Already logged weight for today!",
				ans = raw_input(" Remove? ")
				if ans[0].lower() == 'y':
					self.weightlogmap.pop(self.date)
					print >> sys.stderr, "\rDeleted record"
					self.log(lbls)
					return
				else:
					print >> sys.stderr, "\rUnchanged"


		#Weight does not exist for that date
		else:
			self.weightlogmap[self.date] = Weight(lbls)
      			print >> sys.stderr, "[Logged Morning lb]"

		self.write()
		self.display()

wl = WeightLog()
wl.log(50)
