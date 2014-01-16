#!/usr/bin/env python

class Weight:
	def __init__(self,morning=-1,night=-1):
		self.morn = morning
		self.night = night

class WeightLog:

	def __init__(self,path="~/.config/keto/weightlog.txt"):
		self.weightlogmap={}
		self.path = path
		read()
		
	def read(self):
		f=open(self.path,'r')

		f.readline()	#Skip header
		for weight in f:
			date, morn, nigh = weight.split()
			self.weightlogmap[date] = Weight(morn,nigh)
		f.close()

	def write(self):
		f=open(self.path,'w')
		print >> f, "Date\tMorn\tNight"	#print header

		for date in sorted(self.weightlogmap.keys()):
			w = self.weightlogmap[date]
			print >> f, "%s\t%s\t%s" % (date, w.morn, w.night)
		f.close()


	def log(self,lbls):
		currdate=date()

		#Weight exists for that date
		if currdate in weightlogmap:
			w = weightlogmap[currdate]

			if w.morn==-1 and w.night==-1:
				weightlogmap[currdate].morn = lbls
				print >> sys.stderr, "Morning lb:", lbls

			if w.morn!=-1 and w.night==-1:
				weightlogmap[currdate].night = lbls
				print >> sys.stderr, "Night lb:", lbls

			else:
				print >> sys.stderr, "\
Already logged weight!:",\
 weightlogmap[currdate].morn,\
 weightlogmap[currdate].night
				ans = input("Remove?\n")
				if ans[0].lower() == 'Y':
					weightlogmap.remove(currdate)

		#Weight does not exist for that date
		else:
			weightlogmap[currdate] = Weight(lbls)
