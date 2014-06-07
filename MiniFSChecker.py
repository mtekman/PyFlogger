#!/usr/bin/env python

import sys, re, Common
from Yemek import Yemek
from urllib2 import urlopen as uopen, URLError, build_opener as bo, Request as req, HTTPRedirectHandler as hredh


class SmartRedirectHandler(hredh):
    def http_error_301(self, req, fp, code, msg, headers):  
        result = hredh.http_error_301(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):  
        result = hredh.http_error_302(
            self, req, fp, code, msg, headers)              
        result.status = code                                
        return result



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
	mobile_url="http://m.fatsecret.com"

	def __init__(self, query):
		print >> sys.stderr, "Checking online...",
		self.query = HTMLMethods.toHTMLChars(query)

		try:
			self.pagedata = uopen(FHandler.static_url+self.query).read()
		except URLError:
			print " stopped, no connection?"
			exit(-1)

#		# offline saved
#		print self.pagedata
#		exit(0)
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
			res_lines = x.printout().split('\n')
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
	def getFoodInfo(url):
		try:
			newurl = FHandler.mobile_url + url
			print newurl
			re = req(newurl)
			pp = bo(SmartRedirectHandler())
			f = pp.open(re)
			print f.headers
			print f.url
			exit(0)
#			tempdata = uopen(newurl).read()
		except URLError:
			print " stopped, no connection?"
			exit(-1)

		print tempdata
		exit(0)

	
	@staticmethod
	def getFacts(meta):
		try:
			n,a = meta.split("per ")
		except ValueError:
			return -1
		
		#name
		n = n.split('>')[1].split('<')[0].strip().replace('\n',"").lower()

#		FHandler.getFoodInfo(url)
		
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
			print meta,"\n"
			res.append(y)
		
		return res

f = FHandler("chicken")
print f.found
