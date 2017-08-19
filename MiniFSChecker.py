#!/usr/bin/env python

import sys, re, Common
from Yemek import Yemek, Carb
from urllib.request import urlopen as uopen
from urllib.error import URLError
from bs4 import BeautifulSoup as bs


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


	def __init__(self, query, foodobj=0):
		print("\rChecking online...", end=' ', file=sys.stderr)
		self.query = HTMLMethods.toHTMLChars(query)

#		try:
#			self.pagedata = uopen(FHandler.query_url+self.query).read()
#		except URLError:
#			print(" stopped, no connection?")
#			exit(-1)

#		# offline saved
#		print(self.pagedata)
#		exit(0)
		self.pagedata = open("test_sub.html").read()

		self.results = self.ParseResults()
		if foodobj==0:
			self.found = self.resHandler()
		else:
			#Check current food obj against results list
			self.found = self.checkFoodHomology(foodobj)


	def checkFoodHomology(self,fobj):
		if len(self.results)==0:
			print("No matches")
			return -1

		good_results = []

		for fo in self.results:
			#ignore meaningless foods
			if fo.kC==0:
				continue

			diff = fobj.kC - fo.kC
			scale = float(fobj.kC)/float(fo.kC)
			if diff < 0:diff *=-1

			if diff < 10:
				good_results.append((fo,scale))
				continue


			th_prot = fobj.prot
			th_fat = fobj.fat
			if th_prot==0:th_prot=0.00001
			if th_fat==0:th_fat=0.00001

			my_prot = fo.prot
			my_fat = fo.fat
			if my_prot==0:my_prot=0.00001
			if my_fat==0:my_fat=0.00001

			my_rat = my_prot/my_fat
			th_rat = th_prot/th_fat

			diff = th_rat - my_rat
			if diff<0:diff*=-1

			if diff < 0.1:
				good_results.append((fo,scale))

		return Common.choice(good_results, fobj)



	def resHandler(self, max_split=30):
		if len(self.results)==0:
			print("No matches")
			return -1

		return Common.choice(self.results)



	@staticmethod
	def handleFoodInfo(food_data):
		#Header indexes and make a column map
		headers = [tr.find('td', {'class':'label borderTop'}) for tr in food_data.table.find_all('tr')]
		fact_map = {}

		for t in range(len(headers)):
			tag = headers[t]
			if tag == None:
				continue

			value = tag.findNext('td')
			try:
				value = value.b.text.strip()
			except AttributeError:
				value = value.text.strip()

			fact_map[tag.text.lower().strip()] = value

		# Serving size
		fact_map['serving'] = food_data.table.find('td',attrs={'class':'title'}).findNext('tr').td.text.split('Size:')[-1]

		car = Carb(
			fact_map['carbohydrate'][0],
			fact_map['fibre'][0],
			fact_map['sugar'][0]
		)

		return fact_map['calories'], car, fact_map['protein'], fact_map['fat'], fact_map['serving']



	@staticmethod
	def handlePortionData(portion_data):
		try:
			start_index = portion_data.index("<h2>Common serving sizes</h2>")
		except ValueError:
			return -1

		start_index = portion_data.index("<table ", start_index+1)
		end_index = portion_data.index("</table>", start_index + 5)

		portion_data = portion_data[start_index:end_index].split("<tr")[1:]

		res = []

		for p_data in portion_data:
			try:
				start = p_data.index("<a href=\"")+9
			except ValueError:
				continue

			start = p_data.index(">", start)+1
			end = p_data.index("</a>", start)

			name = p_data[start:end].strip()

			#Try for extra name info, skip otherwise
			try:
				ex_start = p_data.index("<span class=\"small-text grey-text\">(",end+5)+35
				ex_end = p_data.index(")",ex_start)

				name += " "+p_data[ex_start:ex_end+1].strip()
			except ValueError:
				pass


			# Calorie info
			start = p_data.index("a class=\"small-text\" href=", end)
			start = p_data.index(">", start+10)+1
			end = p_data.index("</a>", start)

			try:
				calorie = int(p_data[start:end].strip())
			except ValueError:
				# Couldn't convert, or kCal non-existent, skip
				continue

			res.append( [name, calorie] )
		return res





	@staticmethod
	def getFoodInfo(url):
		try:
			newurl = FHandler.mobile_url + url
			#tempdata = uopen(newurl).read()
			##with open('test_foodinfo','w') as file:file.write(str(tempdata));file.close();exit(0);
			tempdata = open('test_foodinfo.html','r').read()

		except URLError:
			print(" stopped, no connection?")
			exit(-1)


		bsobj = bs(tempdata,'html.parser')
		name = bsobj.body.find('div', attrs={'class':'page-title'}).text.strip(' \\r\\t\\n').lower()

		food_tagline = bsobj.find('div', attrs={'class':'page-info-text'}).text.strip(' \\r\\t\\n').lower()
		food_table = bsobj.find('div', attrs={'class':'nutpanel'})

		food_info = FHandler.handleFoodInfo(food_table)

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



	def ParseResults(self, num=30):

		bsobj = bs(self.pagedata, "html.parser")
		bsurls = bsobj.body.find_all('a', attrs={'class':'prominent'});

		for meta in bsurls:
			url = meta.attrs['href']
			text = meta.findNext('div', attrs={'class':'greyLink'}).text

			try:
				n,a, = text.split('per ')
			except IndexError:
				# Don't parse urls without proper parts
				continue

			result = FHandler.getFoodInfo(url)
			print("\r\t\t\t", len(res)+1, end=' ', file=sys.stderr)
			res.append(result)

			# count
			num -= 1
			if num==0: break


		return res


f = FHandler("milk")
