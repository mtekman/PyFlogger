#!/usr/bin/env python

import sys, re, Common
from Yemek import Yemek
from urllib2 import urlopen as uopen, URLError

class HTMLMethods:
	@staticmethod
	def toHTMLChars(query):
		replacemap = {}
		replacemap[" "]="+"
		replacemap["'"]="%27"
		for key in replacemap:
			query = query.replace(key, replacemap[key])
		return query


class FHandler:
	static_url="http://www.fatsecret.co.uk/calories-nutrition/search?q="

	def __init__(self, query):
		print >> sys.stderr, "Checking online...",
		self.query = HTMLMethods.toHTMLChars(query)

		try:
			self.pagedata = uopen(FHandler.static_url+self.query).read()
		except URLError:
			print " stopped, no connection?"
			exit(-1)

#		# offline saved
#		self.pagedata = open("test2.html").read()

		self.results = self.ParseResults()
		print >> sys.stderr, "found results: %d" % len(self.results)

		self.found = self.resHandler()


	def resHandler(self, max_split=30):
		if len(self.results)==0:
			print "No matches"
			return -1
	
		maxlen_foodname=30

		hhh = "%s   \t%s" % (' '*maxlen_foodname, Yemek.printheader().strip())
		print >> sys.stderr, hhh
		hhh = hhh.replace('\t','    ')
		print >> sys.stderr, '-'*(len(hhh)-1)
			    
		choose=1
		for x in self.results:
			res_lines = x.printout(buffer=maxlen_foodname, maxsplit=max_split).split('\n')
			choose_s = "%d :" % choose
			print choose_s, res_lines[0]

			del res_lines[0]
			while len(res_lines)>0:
				print ' '*(len(choose_s)), res_lines[0]
				del res_lines[0]

			choose +=1
		ind = int(raw_input('Please pick a number: '))
		return self.results[ind-1]
	
	
	@staticmethod
	def getFacts(meta):
		try:
			n,a = meta.split("per ")
		except ValueError:
			return -1
		
		#name
		n = n.split('>')[1].split('<')[0].strip().replace('\n',"").lower()
		
		#amounts
		a = a.split('<')[0]
		a_tokes = Common.stripAll(a.split('|'))
		if len(a_tokes)!=4:
			return -1
		
		per, cal= Common.stripAll(a_tokes[0].split('-'))
		cal, farc, ca, prot = map(lambda x: x.split(':')[-1], [cal] + a_tokes[1:])
		
		cal = int(cal.split('kc')[0])
		farc, ca, prot = (float(x.split('g')[0]) for x in (farc,ca,prot))
		
		per,unit = Common.amountsplit(per)

		return Yemek(n, cal, ca, prot, farc, per, unit)
	
	
	def ParseResults(self):
		res = []
		tokes = self.pagedata.split("prominent")
		
		for meta in tokes:
			url = meta.split('href="')[1].split('">')[0]
			y = FHandler.getFacts(meta)
			if y==-1:
				continue
			
			y.url = url
			res.append(y)
		
		return res
