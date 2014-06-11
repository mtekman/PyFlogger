#!/usr/bin/env python

import sys
from Yemek import Yemek, Carb, Portion, Tags
from os.path import abspath
import Common
import MiniFSChecker

class FoodList:
	def __init__(self,file=abspath("../")+"/logs/keto_foodlist.txt"):
		self.foodmap={}
		self.path= file
		self.read()

	def read(self):
		try:
			f=open(self.path,'r')
		except IOError:
			f=open(self.path,'w')
			f.write(" ")
			f.close()
			return

		# Strip Headers
		f.readline(); f.readline()
		
		for foodentry in f:
			if len(foodentry)< 5:
				continue

			dd = foodentry.split('|')
			name = dd[0]
			data = dd[1]
			portions = ""
			tags=""
			if len(dd)==3:portions = dd[2]
			if len(dd)==4:
				portions = dd[2]
				tags = dd[3].strip()
			
			name = name.strip().lower()
			
			tokes = data.split()
			#629      11.6   [     7.4,   4.2]   =                4.2  21.1  55.8 100.0 g
			kC, carb_total, junk, fibre, sugar, junk, carb_bad_unused, prot, fat, per = tokes[0:10]
			unit = ' '.join(tokes[10:])

			carbs = Carb(carb_total, fibre[:-1], sugar[:-1])
			food = Yemek(name, kC, carbs, prot, fat, per, unit)
			
			# Handle avail portions
			if portions!="":
				p_data = portions.split(Portion.start_delim)[1:]
				for pv in p_data:
					p,v = pv.split(Portion.end_delim)
					food.portions.insert(p.strip(), int(v))

			# Handle Tags
			if tags!="":
				t_data = tags.split(Tags.delim)
				for tv in t_data:
					food.tags.insert(tv.strip())
			
			self.foodmap[food.name] = food
		f.close()


	def write(self):
		
		Common.backup(self.path)
		f=open(self.path,'w')
		
		maxlen_name = reduce(lambda x,y: x if len(x) > len(y) else y, self.foodmap.keys())
		maxlen_name = len(maxlen_name)+5
		
		maxport_name = reduce(lambda x,y: x if len(self.foodmap[x].unit) > len(self.foodmap[y].unit) else y, self.foodmap.keys())
		maxport_name = len(self.foodmap[maxport_name].unit)+5
		
		
		print >> f, Yemek.printheader(buffer=maxlen_name, 
			portions_buff=(maxport_name-len('unit')),
			tags=True)
		print >> f, ""
		
		for food in sorted(self.foodmap.keys()):
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(buffer=maxlen_name, pre="", 
				portions_buff=(maxport_name-len(fooditem.unit)),
				tags=True)
		f.close()


	def printlist(self):
		keys = sorted(self.foodmap.keys())
		print >> sys.stderr, Yemek.printheader()
		for food in keys:
			fooditem = self.foodmap[food]
			print >> sys.stderr, fooditem.printout() #.strip()



	def insertAll(self, yem, input_search=[]):
		#Tag prompt
		user_input_tags = Tags.tagprompt()
		if user_input_tags!=-1:
			yem.tags.insertList(user_input_tags)
		
		if input_search!=[]:yem.tags.insertList(input_search)

		name = yem.name.strip().lower()
		self.foodmap[name] = yem
		print >> sys.stderr, "Inserted", name
		self.write()


	def insert(self,name, input_search=[]):
		print "Inserting new food:", name
		per,unit = Common.amountsplit(raw_input("Per Unit (e.g. '100g'): ").strip())
		kc, carb_total, carb_sugar, carb_fibre , prot, fat = raw_input("kCal Carb Sug Fibr Prot Fat: ").split()
			
		carbs = Carb(carb_total, carb_fibre, carb_sugar)
		y = Yemek(name, kc, carbs, prot, fat, per, unit)

		self.insertAll(y, input_search)


	def removeprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			del self.foodmap[name]
			print >> sys.stderr, "[Removed]"
		else:
			print >> sys.stderr, "[Does not exist!]"
		self.write()


	def insertprompt(self):
		name = raw_input('Food Name: ').strip()

		if name in self.foodmap:
			print >> sys.stderr, "[Food already exists!]"
			print >> sys.stderr,  self.foodmap[name].printout(header=True)
			exit(-1)
		self.insert(name)


	#This is the main insertion method
	def updateprompt(self):
	
	   # Print details if exists, else insert, else return close match
		name = self.info(raw_input('Food: ').strip())
		
		# Name exists by now, or prog exited
      
		if name in self.foodmap:
			edit = raw_input('\nEdit? ')
			if edit[0].lower() != 'y':
				exit(-1)
		else:
			print >> sys.stderr, "\n[New Food: \"%s\"]" % name
		self.insert(name)
	
	def search(self,name):
		searchname = name.split()  #d[0].strip()
		#print searchfoods, searchname
			
		found=[];
		for avail_food, obj in self.foodmap.iteritems():
			#words
			for ss in searchname:
				for s in avail_food.split():
					if ss.strip() in s.strip():
						if obj not in found: found.append(obj)
						break
		
		if len(found)==0:
			print "Searching tags..."
			for avail_food, obj in self.foodmap.iteritems():
				for ss in searchname:
					for tag in obj.tags.tags:
						if ss.strip() in tag:
							if obj not in found: found.append(obj)
							break
			
			
		return found


	def updateListInfo(self):
		for name in self.foodmap.keys():
			food = self.foodmap[name]
			
			if not((food.carb.sugar ==0 and food.carb.fibre==0) and (food.carb.total == food.carb.bad)):
				continue
			
			if "FS_online" not in food.tags.tags:continue
			
#			if name != 'chicken drumstick (skin eaten)':continue
			
			print "Check:"
			print food.printout(pre="---")
			f = MiniFSChecker.FHandler(food.name, food).found
			if f!=-1:
				del self.foodmap[name]
				self.foodmap[f.name.lower()] = f
				self.write()
		
		self.write()


	
	def info(self,name):
		if name in self.foodmap:
			print >> sys.stderr,  self.foodmap[name].printout(header=True)
			return name

		#Search objects for closest match
		arg_name = name	#store
		
		found = self.search(name)
		res = len(found)

		if res == 0:
			print >> sys.stderr, "\nCannot find:", "\"%s\"" % name,
			if Common.ynprompt(", manually insert?"):
				self.insert(name, [arg_name])
				return name.lower()
			if Common.ynprompt('Search online? '):
				f = MiniFSChecker.FHandler(name).found
				if f==-1:exit(0)
				self.insertAll(f, [arg_name,"FS_online"])
				return f.name
			exit(0)
			
		# Found something, print
		print >> sys.stderr, "\nMatched:",		
		res = Common.choice(found)

		if res==-1:
			print >> sys.stderr, "None"
			if Common.ynprompt('Search online? '):
				f = MiniFSChecker.FHandler(name).found
				if f==-1:exit(0)
				self.insertAll(f, [arg_name, "FS_online"]) # Nothing found, include input name as a tag
				name = f.name
			else:
				#Manual insert
				self.insert(name, [arg_name])		# Nothing ...
		else:
			name = res.name
		return name
				

#w = FoodList()
#w.updateListInfo()
