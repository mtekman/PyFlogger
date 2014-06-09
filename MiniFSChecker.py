#!/usr/bin/env python

import sys, re, Common
from Yemek import Yemek, Carb
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
	base_url="http://www.fatsecret.co.uk"
	mobile_url="http://m.fatsecret.co.uk"
	query_url=base_url+"/calories-nutrition/search?q="
	

	def __init__(self, query):
		print >> sys.stderr, "\rChecking online...",
		self.query = HTMLMethods.toHTMLChars(query)

		try:
			self.pagedata = uopen(FHandler.query_url+self.query).read()
		except URLError:
			print " stopped, no connection?"
			exit(-1)

#		# offline saved
#		print self.pagedata
#		exit(0)
##		self.pagedata = open("test2.html").read()

		self.results = self.ParseResults()
#		print >> sys.stderr, "found results: %d" % len(self.results)

		self.found = self.resHandler()


	def resHandler(self, max_split=30):
		if len(self.results)==0:
			print "No matches"
			return -1
	
		maxlen_foodname=30

		print >> sys.stderr, '\n', 
		hhh = Yemek.printheader(buffer=maxlen_foodname+4)
		print >> sys.stderr, hhh
		hhh = hhh.replace('\t','    ')
		print >> sys.stderr, '-'*(len(hhh)-1)
			    
		choose=1
		for x in self.results:
			res_lines = x.printout(pre="").split('\n')
			choose_s = "%2d:" % choose
			print choose_s, res_lines[0]

			del res_lines[0]
			while len(res_lines)>0:
				print ' '*(len(choose_s)-2), res_lines[0]
				del res_lines[0]

			choose +=1
		ind = int(raw_input('Please pick a number (0 to cancel): '))-1
		if ind==-1:
			return -1
		return self.results[ind-1]



	@staticmethod
	def handleFoodInfo(food_data):
		#Cal
		b_1 = food_data.index("<b>")
		b_2 = food_data.index("calories</b>", b_1+1)
		
		calories = int(food_data[b_1+3:b_2])
#		print "cal:", calories
		
		#Per
		b_3 = food_data.index(".</div>", b_2+1)
		tokes = food_data[b_2+12:b_3].split()

		num_index = 0
		for t in xrange(len(tokes)):
			try:
				Common.amountsplit(tokes[t], floater=True)
				num_index = t
				break
			except ValueError:
				pass

		per = Common.amountsplit(tokes[num_index], floater=True)[0]
		unit = tokes[num_index+1].strip()
#		print "p/u:", per, unit
		
		#Fat
		b_2 = food_data.index("<b>Fat:</b>", b_3+1)
		b_3 = food_data.index("</div>",b_2+1)
		
		fat = Common.amountsplit(food_data[b_2+11:b_3].strip().split()[0], floater=True)[0]
#		print "fat:", fat
		
		#Carbs
		b_2 = food_data.index("<b>Carbs:</b>", b_3+1)
		b_3 = food_data.index("</div>",b_2+1)
		
		carb_data = food_data[b_2+13:b_3].strip().split()
		carbs = Common.amountsplit(carb_data[0], floater=True)[0]
		
		f_index = s_index = -1
		for c_d in xrange(len(carb_data)):
			if "Fibre:" in carb_data[c_d]:
				f_index = c_d+1
			elif "Sugar:" in carb_data[c_d]:
				s_index = c_d+1

		fibre = Common.amountsplit(carb_data[f_index], floater=True)[0]
		sugar = Common.amountsplit(carb_data[s_index], floater=True)[0]
		
		if f_index==-1:
			fibre = 0
		if s_index==-1:
			sugar = carbs

		
		#Protein
		b_2 = food_data.index("<b>Protein:</b>", b_3+1)
		b_3 = food_data.index("</div>",b_2+1)
		
		protein = Common.amountsplit(food_data[b_2+15:b_3].strip().split()[0],floater=True)[0]
#		print "protein", protein
		if unit=="grams":unit='g'
		
		car = Carb(carbs, fibre, sugar)

		return calories, car, fat, protein, per, unit



	@staticmethod
	def handlePortionData(portion_data):
		try:
			start_index = portion_data.index("<h2>Common serving sizes</h2>")
		except ValueError:
			return -1
		
		start_index = portion_data.index("<table ", start_index+1)
		end_index = portion_data.index("</table>", start_index + 5)
		
		portion_data = portion_data[start_index:end_index].split("<tr>")[1:]
		
		res = []
		
		for p_data in portion_data:
			start = p_data.index("<a href=\"")+9
			start = p_data.index(">", start)+1
			end = p_data.index("</a>", start)
			
			name = p_data[start:end].strip()
			
			#Extra name info
			try:
				ex_start = p_data.index("(",end+5)
				ex_end = p_data.index(")",ex_start+1)
				
				name += p_data[ex_start:ex_end+1].strip()
			except ValueError:
				pass
			
			# Calorie info
			start = p_data.index("a class=\"small-text\" href=", end)
			start = p_data.index(">", start+10)+1
			end = p_data.index("</a>", start)
			
			calorie = int(p_data[start:end].strip())
			
			res.append( [name, calorie] )
		return res





	@staticmethod
	def getFoodInfo(url):
		try:
			newurl = FHandler.mobile_url + url
			tempdata = uopen(newurl).read()
		except URLError:
			print " stopped, no connection?"
			exit(-1)

		n_index1 = tempdata.index("<h1>")
		n_index2 = tempdata.index("</h1>", n_index1+1)
		
		name = tempdata[n_index1+4:n_index2].strip().lower()

		index1 = tempdata.index("<div>There are")
		index2 = tempdata.index("</td></tr>", index1+1)

		food_data = tempdata[index1:index2]
		food_info = FHandler.handleFoodInfo(food_data)
		
		yem = Yemek(name, 
			food_info[0], food_info[1], food_info[2], 
			food_info[3], food_info[4], food_info[5])
		
		portion_data = tempdata[index2:]
		portion_info = FHandler.handlePortionData(portion_data)
		
		if portion_info!=-1:
			for key,val in portion_info:
				yem.portions.insert(key,val)
		
		return yem


	@staticmethod
	def tryFacts(meta):
		try:
			n,a = meta.split("per ")
		except ValueError:
			return -1



	def ParseResults(self):
		res = []
		tokes = self.pagedata.split("prominent")
		
		for meta in tokes:
			url = meta.split('href="')[1].split('">')[0]
			try:
				n,a = meta.split("per ")
			except ValueError:
				continue
				
			result = FHandler.getFoodInfo(url)
			print >> sys.stderr, "\r\t\t\t", len(res)+1,
			res.append(result)
		
		return res


#f = FHandler("milk")
#print f.found
