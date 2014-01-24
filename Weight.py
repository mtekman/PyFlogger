#!/usr/bin/env python

import sys
from time import localtime, time
from os.path import abspath

class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night

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
			self.weightlogmap[date] = Weight(int(morn),int(nigh))
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

		print >> sys.stderr, '\n'
		print >> sys.stderr, '='*39
		print >> sys.stderr, "Date     \tMorn\tNight"	#print header

		# Print all dates from that day forward
		# For today it is a single date
		for dated in availdates[index:]:
			w = self.weightlogmap[dated]
			print >> sys.stderr, "%s\t%d\t%d%s" % (dated, w.morn, w.night,\
				"   <--" if date==dated else "")



	def nextDay(self, date):
		return ("%04d/%02d/%02d" % localtime(time()+(24*60*60))[0:3])


	def checkYesterNight(self):
		# only checking for INCOMPLETE yesterdays (i.e no yesterday, no problem)
		if self.yesterday in self.weightlogmap:
			if self.weightlogmap[self.yesterday].night==-1:
				print >> sys.stderr, "Nothing logged for last night,",
				ans = raw_input(" log that? ")
				if ans[0].lower()=='y':
					self.log(self.yesterday,night=True)
				else:
					print >> sys.stderr, "Ignoring"
					self.weightlogmap[self.yesterday]=0

	def checkTodayGaps(self):
		if self.today in self.weightlogmap:
			w = self.weightlogmap[self.today]

			if w.morn!=-1 and w.night!=-1:
				print >> sys.stderr, "Date logged already:"
				self.display(self.today)
				if raw_input("Delete? ")[0].lower() == 'y':
					self.weightlogmap.pop(self.today)
					print >> sys.stderr, "\rDeleted record"
					return 0
				return -1


			if w.morn==-1 and w.nighttime:
				print >> sys.stderr, "Nothing logged for this morning.",
				if raw_input("Prepend? ")[0].lower() == 'y':
					self.log(self.today,morning=True)
					return 0


	def logprompt(self):
		self.checkYesterNight()
		print >> sys.stderr, "\nToday's log:"
	
		res = self.checkTodayGaps()
		if res!=-1:
			self.log(self.today, not(self.nighttime))


				
	def log(self, date, morning):	
		d_str=""
		if date==self.today:
			d_str="this morning" if morning else "tonight"
		elif date==self.yesterday:
			d_str="yesterday morning" if morning else "last night"
		else:
			d_str=date
	
		lbls=int(raw_input('Please give input for %s : ' % d_str))

		#Weight exists for that date
		if date in self.weightlogmap:
			w = self.weightlogmap[date]

			if self.nighttime==False:
				if w.morn==-1:
					self.weightlogmap[date].morn = lbls
					print >> sys.stderr, "[Logged Morning lb]"
					return 0
				print >> sys.stderr, "Wait. Already logged for morning:"
				self.display(date)
				if raw_input(" Update with new? ")[0].lower() == 'y':
					self.weightlog
				
				

			if w.night==-1 and self.nighttime:
				self.weightlogmap[date].night = lbls
				print >> sys.stderr, "[Logged Night lb]"
				return 0
				
			if w.morn!=-1 and w.night!=-1:
				print >> sys.stderr, "Already logged weight for %s!" % date ,
				ans = raw_input(" Remove? ")
				if ans[0].lower() == 'y':
					self.weightlogmap.pop(date)
					print >> sys.stderr, "\rDeleted record"
					self.log(date,lbls, morning=True)
					return

				print >> sys.stderr, "\rUnchanged"
				return
				
		#Weight does not exist for that date
		self.weightlogmap[date] = Weight(lbls)
		print >> sys.stderr, "[Logged Morning lb]"

		self.write()
		self.display(date)

wl = WeightLog()
wl.logprompt()
