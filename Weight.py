#!/usr/bin/env python

import sys
from time import localtime, time
from os.path import abspath

#Global method
def ynprompt(message):
	ans = raw_input(message)
	return (ans[0].lower()=='y')

class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night
		
	def overwriteprompt(self,morning, lbls):
		print "Weight already exists for", ("morning" if morning else "night"),":"
		print >> sys.stderr, self.printout()
		if ynprompt("Overwrite?"):
			if morning:
				self.morn = lbls
			else:
				self.night = lbls
			print >> sys.stderr, self.printout()
		else:
			print "not overwritten"

	def set(self,lbls, night):
		if not(night):
			if self.morn==-1:
				self.morn = lbls
			else:
				self.overwriteprompt(night,lbls)
		else:
			if self.night==-1:
				self.night = lbls
			else:
				self.overwriteprompt(not(night),lbls)
#		print self.printout(True)
	
	####Public Methods ####
	@staticmethod
	def printheader():
		return '\n'+('='*39)+\
			"\nDate     \tMorn\tNight"	#print header

	def printout(self, header=False):
		resil=""
		if header:
			resil=Weight.printheader()+'\n'
		return resil+("%d\t%d" % (self.morn, self.night))
				
	def update(self,lbls,isNighttime):
		if isNighttime:
			if self.morn==-1:
				print "Daytime Weight not set"
				if ynprompt("Set morning lbls instead? "):
					self.set(lbls,False)
					return
					
			self.set(lbls,True)
			return
			
		#Otherwise it's daytime
		self.set(lbls,True)
		return
		
		
class WeightLog:
	def __init__(self,file=abspath("../")+"/logs/keto_weightlog.txt"):
		self.weightlogmap={}
		self.path = file
		
		self.date = localtime()
		self.today = "%04d/%02d/%02d" % self.date[0:3]
		self.yesterday= "%04d/%02d/%02d" % localtime(time()-(24*60*60))[0:3]
		self.nighttime= (self.date[4] > 20)

		self.read()
		
	def logprompt(self):
		self.checkYesterNight()
		print >> sys.stderr, "\nToday's log:"
	
		self.log(self.today, self.nighttime)


	def log(self, date, nightime, lbls=-1):	
		d_str=""
		if date==self.today:
			d_str="this morning" if (not nightime) else "tonight"
		elif date==self.yesterday:
			d_str="yesterday morning" if (not nightime) else "last night"
		else:
			d_str=date

		if lbls==-1:
			lbls=float(raw_input('Please give input for %s : ' % d_str))
		
		if date in self.weightlogmap:
			self.weightlogmap[date].update(lbls,nightime)			
		else:
			w=Weight()
			w.update(lbls,nightime)
			self.weightlogmap[date]=w

		self.write()
		self.display(date)

	def read(self):
		try:
			f=open(self.path,'r')
		except IOError:
			f=open(self.path,'w')
			f.write("")
			f.close()
			return
		
		
		f.readline()	#Skip header
		for weight in f:
			if len(weight)< 5:
				continue
			date, morn, nigh = weight.split('\t')
			self.weightlogmap[date] = Weight(float(morn),float(nigh))
		f.close()


	def write(self):
		f=open(self.path,'w')
		print >> f, "Date     \tMorn\tNight\n"	#header

		for date in sorted(self.weightlogmap.keys()):
			w = self.weightlogmap[date]
			print >> f, "%s\t%s\t%s" % (date, w.morn, w.night)
		f.close()

	def display(self, date):
		# Dates in order
		availdates= sorted(self.weightlogmap.keys())
		
		#Start point
		index = availdates.index(date)
		print >> sys.stderr, Weight.printheader()	#print header

		# Print all dates from that day forward
		# For today it is a single date
		for dated in availdates[index:]:
			w = self.weightlogmap[dated]
			print >> sys.stderr, "%s\t%s %s" % (dated, w.printout(), ("   <--" if date==dated else " "))



	def nextDay(self, date):
		return ("%04d/%02d/%02d" % localtime(time()+(24*60*60))[0:3])


	def checkYesterNight(self):
		# only checking for INCOMPLETE yesterdays (i.e no yesterday, no problem)
		if self.yesterday in self.weightlogmap:
			w = self.weightlogmap[self.yesterday]
			if w.night==-1:
				print >> sys.stderr, "Nothing logged for last night,",
				if ynprompt(" log that instead? "):
					self.log(self.yesterday,True)
				else:
					print >> sys.stderr, "Ignoring"
					self.log(self.yesterday,True,0)
#					self.weightlogmap[self.yesterday].night=0

	def checkTodayGaps(self):
		if self.today in self.weightlogmap:
			w = self.weightlogmap[self.today]

			if w.morn!=-1 and w.night!=-1:
				print >> sys.stderr, "Date logged already:"
				self.display(self.today)
				if ynprompt("Delete? "):
					self.weightlogmap.pop(self.today)
					print >> sys.stderr, "\rDeleted record"
					return 0
				return -1


			if w.morn==-1 and self.nighttime:
				print >> sys.stderr, "Nothing logged for this morning.",
				if ynprompt("Prepend? "):
					self.log(self.today,morning=True)
					return 0





wl = WeightLog()
wl.logprompt()
