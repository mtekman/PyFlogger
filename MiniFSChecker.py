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
		headers = [tr.td.b for tr in food_data.table.find_all('tr')]
		fact_map = {}

		for t in range(len(headers)):
			tag = headers[t]
			if tag == None:
				continue

			#import pdb; pdb.set_trace()

			value = tag.parent.findNext('td')
			try:
				value = value.b.text
			except AttributeError:
				value = value.text

			fact_map[tag.text.lower()] = value

		# Serving size
		fact_map['serving'] = food_data.table.find('td',attrs={'class':'title'}).findNext('tr').td.text.split('Size:')[-1]

		#Cal
		import pdb; pdb.set_trace()
		b_1 = food_data.index("<b>")
		try:
			b_2 = food_data.index("calories</b>", b_1+1)
		except ValueError:
			b_2 = food_data.index("calorie</b>", b_1+1)

		calories = int(food_data[b_1+3:b_2])
#		print "cal:", calories

		#Per
		b_3 = food_data.index(".</div>", b_2+1)
		tokes = food_data[b_2+12:b_3].split()
#		print tokes


		# Store per,unit combos as tuples
		per_unit = []

		last_index = -1

		# Single pass, find all units
		for t in range(len(tokes)):
			try:
				per, unit = Common.amountsplit(tokes[t], floater=True)
				try:
					unit += ' '+tokes[t+1]
				except IndexError:
					pass
				per_unit.append( [per,unit] )
			except ValueError:
				pass


		per = per_unit[0][0]
		unit = per_unit[0][1]+' '+','.join(set(['('+str(x[0]).strip()+' '+x[1].strip()+')' for x in per_unit[1:]]))


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
		for c_d in range(len(carb_data)):
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

		return calories, car, protein, fat, per, unit



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
			tempdata = open('test_foodinfo','r').read()

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
