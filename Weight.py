#!/usr/bin/env python

from time import localtime, time
from Common import *


class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night
		

	@staticmethod
	def printheader():
		return '\n'+('='*39)+\
			"\nDate     \tMorn\tNight"	#print header


	def printout(self, header=False, filler=False):
		resil=""
		if header:
			resil=Weight.printheader()+'\n'
			
		if filler:
			resil += "             \t"
		return resil+("%d\t%d" % (self.morn, self.night))
	
				
	def set(self, lbls, setmorn, finalprint=False):
		if setmorn:
			if self.morn!=-1:
				print "Morning already set:"
				print self.printout(header=True, filler=True)
				if (ynprompt('Overwrite? ')):
					self.morn = lbls
			else:
				self.morn = lbls
		else:
			if self.night!=-1:
				print "Night already set:"
				print self.printout()
				if (ynprompt('Overwrite? ')):
					self.night = lbls
			else:
				self.night = lbls

		if finalprint:
			print self.printout(True)
	
	
class WeightLog:
	def __init__(self,file=abspath("../")+"/logs/keto_weightlog.txt"):
		self.weightlogmap={}
		self.path = file
		
		self.date = localtime()
		self.today = "%04d/%02d/%02d" % self.date[0:3]
		self.yesterday= "%04d/%02d/%02d" % localtime(time()-(24*60*60))[0:3]
		self.nighttime= (self.date[3] >= 19)
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
	

	def logprompt(self ,date, isDay):
		#Get day string
		day=date
		if date==self.today:
			day="this " if isDay else "to"
		elif date==self.yesterday:
			day="yesterday " if isDay else "last "

		tod= "morning" if isDay else "night"

		#Input
		lbls= float(raw_input('Please enter input for %s%s: ' % (day,tod)).strip())		
		self.log(date, lbls, isDay)
		self.display(date)


	def checkGaps(self):
		if self.checkLastNight():
			return
		
		if not(self.nighttime):
			if self.checkThisMorning():
				return
			
		self.checkToday()

	
	def checkThisMorning(self):
		if self.today in self.weightlogmap:
			w = self.weightlogmap[self.today]
			if self.nighttime and w.morn==-1:
				print "Night now, morning not set"
				if (ynprompt('Set morning? ')):
					self.logprompt(self.today, isDay=True)
					return True
			
			if not(self.nighttime) and w.morn!=-1:
				self.logprompt(self.today, isDay=True)
				return True
		return False #nothing changed

	def checkLastNight(self):
		if self.yesterday in self.weightlogmap:
			w = self.weightlogmap[self.yesterday]
			if w.night==-1:
				print "Last night not set"
				if (ynprompt('Set last night? ')):
					self.logprompt(self.yesterday, isDay=False)
					return True
					
				print "[Ignoring last night]"
				if ynprompt('Ignore permanently? '):
					self.log(self.yesterday, 0, False)
					print "[Ignoring last night permanently]"
					return True

				print "[Temporarily ignored last night, moving on..]\n"
				
		return False #nothing changed

	def checkToday(self):
		wl.logprompt(self.today, isDay=not(self.nighttime))

wl = WeightLog()
wl.checkGaps()
