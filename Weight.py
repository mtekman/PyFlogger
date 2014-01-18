#!/usr/bin/env python

import sys
from time import localtime as time

class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night

class WeightLog:

	def __init__(self,path="/home/user/.config/keto/weightlog.txt"):
		self.weightlogmap={}
		self.path = path
		self.date = "%04d/%02d/%02d" % time()[0:3]
		self.read()
		
	def read(self):
                f=open(self.path,'r')
                
		f.readline()	#Skip header
		for weight in f:
			date, morn, nigh = weight.split('\t')
			self.weightlogmap[date] = Weight(int(morn),int(nigh))
		f.close()

	def write(self):
		f=open(self.path,'w')
		print >> f, "\tDate\tMorn\tNight"	#print header

		for date in sorted(self.weightlogmap.keys()):
			w = self.weightlogmap[date]
			print >> f, "%s\t%s\t%s" % (date, w.morn, w.night)
		f.close()


	def display(self):
		w = self.weightlogmap[self.date]
		print >> sys.stderr, "\n\n%s\t%s\t%s" % (self.date, w.morn, w.night)


	def log(self,lbls):
		#Weight exists for that date
		if self.date in self.weightlogmap:
			w = self.weightlogmap[self.date]

			if w.night==-1 and w.morn==-1:
        				self.weightlogmap[self.date].morn = lbls
	        			print >> sys.stderr, "Morning lb:", lbls

			if w.night==-1 and w.morn!=-1:
					self.weightlogmap[self.date].night = lbls
	        			print >> sys.stderr, "Night lb:", lbls
			else:
				print >> sys.stderr, "\
Already logged weight for today!:",\
 self.weightlogmap[self.date].morn,\
 self.weightlogmap[self.date].night
				ans = input("Remove?\n")
				if ans[0].lower() == 'Y':
					self.weightlogmap.remove(self.date)

		#Weight does not exist for that date
		else:
			self.weightlogmap[self.date] = Weight(lbls)
       			print >> sys.stderr, "Morning lb:", lbls

		self.write()
		self.display()

wl = WeightLog()
wl.log(50)
