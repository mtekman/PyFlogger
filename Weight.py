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
		

	@staticmethod
	def printheader():
		return '\n'+('='*39)+\
			"\nDate     \tMorn\tNight"	#print header


	def printout(self, header=False):
		resil=""
		if header:
			resil=Weight.printheader()+'\n'
		return resil+("%d\t%d" % (self.morn, self.night))
				
				
	def set(lbls, setmorn):
		if setmorn:
			if self.morn!=-1:
				print "Morning already set:"
				print printout
				if (ynmprompt('Overwrite? '):
					self.morn = lbls
			else:
				self.morn = lbls
		else:
			if self.night!=-1:
				print "Night already set:"
				print printout
				if (ynmprompt('Overwrite? '):
					self.night = lbls
			else:
				self.night = lbls
		self.printout(True)
	
	
		
class WeightLog:
	def __init__(self,file=abspath("../")+"/logs/keto_weightlog.txt"):
		self.weightlogmap={}
		self.path = file
		
		self.date = localtime()
		self.today = "%04d/%02d/%02d" % self.date[0:3]
		self.yesterday= "%04d/%02d/%02d" % localtime(time()-(24*60*60))[0:3]
		self.nighttime= (self.date[4] > 20)

		self.read()

		
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


	def log(self, date, lbls, ismorning):
		w=""

		if date in self.weightlogmap:
			w = self.weightlogmap[date]
		else:
			w = Weight()
	
		w.set(lbls, ismorning )
		self.weightlogmap[date] = w
		self.write()
	

	def logprompt(date=self.date, isDay=not(self.nighttime) ):
		#Get day string
		day=date
		if date==self.date:
			day="today"
		elif date==self.yesterday
			day="yesterday"
		
		#Get time of day string
		tod= "night" if not(isDay) else "morning"
		
		#Input
		lbls= float(raw_input('Please enter weight for %s %s: ' % (day,tod)).strip())
		
		self.log(date, lbls, isDay)


###to implement##
	def checkGaps(self):
		self.checkLastNight()
		
		if not(self.nighttime):
			self.checkThisMorning()
		else:
			self.checkToday()
	


wl = WeightLog()
wl.logprompt()

