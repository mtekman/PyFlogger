#!/usr/bin/env python

import sys, re
from Yemek import Yemek
from urllib2 import urlopen as uopen

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
		self.pagedata = uopen(FHandler.static_url+query).read()
		# offline saved
#		self.pagedata = open("/home/user/MyDocs/.documents/mcds.html").read()
		print >> sys.stderr, "found results:",
		self.results = self.ParseResults()
		print >> sys.stderr, len(self.results)
		res = self.resHandler()
		print "chose:",res.printout()

	def resHandler(self):
		if len(self.results)==0:
			print "No matches"
			return
	
		maxlen_foodname=len(reduce(lambda x,y: ( x if (len(x.name) > len(y.name)) else y ), self.results).name)

		hhh = "%s\t%s" % (' '*maxlen_foodname, Yemek.printheader().strip())
		print >> sys.stderr, hhh
		hhh = hhh.replace('\t','    ')
		print >> sys.stderr, '-'*(len(hhh)-1)
			    
		choose=1
		for x in self.results:
			print choose,':', x.printout(buffer=maxlen_foodname)
			choose +=1
		ind = int(raw_input('Please pick a number:'))
		return self.results[ind-1]
	
	@staticmethod
	def stripAll(list):
		return map(lambda x: x.strip(), list)
	
	@staticmethod
	def getFacts(meta):
		n,a = meta.split('per')
		
		#name
		n = n.split('>')[1].split('<')[0].strip().replace('\n',"")
		
		#amounts
		a = a.split('<')[0]
		a_tokes = FHandler.stripAll(a.split('|'))
		if len(a_tokes)!=4:
			return -1
		
		per, cal= FHandler.stripAll(a_tokes[0].split('-'))
		cal, farc, ca, prot = map(lambda x: x.split(':')[-1], [cal] + a_tokes[1:])
		
		cal = int(cal.split('kc')[0])
		farc, ca, prot = (float(x.split('g')[0]) for x in (farc,ca,prot))
		
		per = per.split()[0].strip()
		unit = " ".join(per.split()[1:]).strip()
		
		return Yemek(n, cal, farc, ca, prot, per, unit)
	
	
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


f = FHandler("macaroni")
