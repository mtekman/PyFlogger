#!/usr/bin/env python

from Common import *
from Config import user_weightlog
from Convert import WeightCon
from Messages import RESULT, INFO


class Weight:

	@staticmethod
	def lbs2stone(lbs):
		if lbs<=0:return ""

		stone = lbs/14
		major = int(stone)
		minor = int((stone-major)*14)
		return str(major)+"'"+str(minor)


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

		p2s=("%s %s" % (Weight.lbs2stone(self.morn), Weight.lbs2stone(self.night))).strip()
		return resil+("%.1f\t%.1f\t[ %s\t]" % (self.morn, self.night, p2s))


	def set(self, lbls, setmorn, finalprint=False):
		if setmorn:
			if self.morn!=-1:
				INFO("Morning already set:")
				print(self.printout(header=True, filler=True))
				if (ynprompt('Overwrite? ')):
					self.morn = lbls
			else:
				self.morn = lbls
		else:
			if self.night!=-1:
				INFO("Night already set:")
				print(self.printout())
				if (ynprompt('Overwrite? ')):
					self.night = lbls
			else:
				self.night = lbls

		if finalprint:
			print(self.printout(True))



class WeightLog:
	def __init__(self):
		self.weightlogmap={}
		self.path = user_weightlog

		self.convert = WeightCon().convert  # method

		self.date  = localtime()
		self.today = "%04d/%02d/%02d" % self.date[0:3]
		self.yesterday = "%04d/%02d/%02d" % localtime(time()-(24*60*60))[0:3]
		self.yesterday = yesterday()[0:3]
		self.nighttime = (self.date[3] >= 19)
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
		print("Date     \tMorn\tNight\n", file=f)	#header

		for date in sorted(self.weightlogmap.keys()):
			w = self.weightlogmap[date]
			print("%s\t%s\t%s" % (date, w.morn, w.night), file=f)
		f.close()


	def display(self, date=None, lastSeven=False):
		# Dates in order
		availdates= sorted(self.weightlogmap.keys())

		if len(availdates) == 0:
			RESULT("Nothing logged.")
			return

		if date == None:
			date = availdates[0]

		#Start point
		index = availdates.index(date)

		#Last7
		if lastSeven:
			index -= 7
			if index < 0:
				index = 0

		print(Weight.printheader(), file=sys.stderr)	#print header

		# Print all dates from that day forward
		# For today it is a single date
		for dated in availdates[index:]:
			w = self.weightlogmap[dated]
			print("%s\t%s %s" % (dated, w.printout(), ("   <--" if date==dated else " ")), file=sys.stderr)


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

		tod = "morning" if isDay else "night"

		#Input
		inp = input('Please enter input for %s%s: ' % (day,tod))
		lbls = self.__parseUnits2Lbls(inp)
		self.log(date, lbls, isDay)
		self.display(date, lastSeven=True)


	def __parseUnits2Lbls(self,inp):
		amount, unit = amountsplit(inp)
		return amount * self.convert(unit,'lb')


	def checkGaps(self):
		if self.checkLastNight():
			return

#		if not(self.nighttime):
		if self.checkThisMorning():
			return

		self.checkToday()


	def checkThisMorning(self):
		if self.today in self.weightlogmap:
			w = self.weightlogmap[self.today]
			if self.nighttime and w.morn==-1:
				INFO("Night now, morning not set. ")
				if (ynprompt('Set morning? ')):
					self.logprompt(self.today, isDay=True)
					return True

			if not(self.nighttime) and w.morn!=-1:
				self.logprompt(self.today, isDay=True)
				return True

			return False #nothing changed

		#Else log a new morning at night
		if self.nighttime:
				INFO("Night now, morning not set. ")
				if (ynprompt('Set morning? ')):
					self.logprompt(self.today, isDay=True)
					return True
		return False #nothing changed

	def checkLastNight(self):
		if self.yesterday in self.weightlogmap:
			w = self.weightlogmap[self.yesterday]
			if w.night==-1:
				INFO("Last night not set")
				if (ynprompt('Set last night? ')):
					self.logprompt(self.yesterday, isDay=False)
					return True

				RESULT("[Ignoring last night]")
				if ynprompt('Ignore permanently? '):
					self.log(self.yesterday, 0, False)
					RESULT("[Ignoring last night permanently]")
					return True

				RESULT("[Temporarily ignored last night, moving on..]\n")

		return False #nothing changed

	def checkToday(self):
		self.logprompt(self.today, isDay=not(self.nighttime))





#wl = WeightLog()
#wl.checkGaps()

#exit(0)
#xy = XYGraph()

#startdate=""
#for date in sorted(wl.weightlogmap.keys()):
#
#	if startdate=="":
#		startdate=date
#		continue
#
#	days_since = wl.daysSince(startdate,date)
#	total = days_since

#	print date,total

#	w = wl.weightlogmap[date]
#	if w.morn>0:
#		xy.addPoint(total,w.morn,"x")
#	if w.night>0:
#		xy.addPoint(total+.5,w.night,"x")

#p = Printer(xy)
