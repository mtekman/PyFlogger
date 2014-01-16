#!/usr/bin/env python

class FoodList:
	def __init__(self,file="~/.config/keto/foodlist.txt"):
		self.foodmap={}
		self.path= file

	def read(self):
		f=open(self.path,'r')
		
		# Strip Header
		f.readline()
		for foodentry in f:
			food = Yemek(foodentry)
			self.foodmap[food.name]= food
		f.close()

	def write(self):
		f=open(self.path,'w')

		for food in sorted(self.foodmap.keys()):
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(header=false)
		f.close()


	def printlist(self):
		keys = sorted(self.foodmap.keys())
		print >> sys.stderr, self.foodmap[keys][0].printout(headeronly=True)
		
		for food in keys:
			fooditem = self.foodmap[food]
			print >> f, fooditem.printout(header=False)


	def insert(self,name):
		per,unit = input("Per,Unit (e.g. '100 g'):").split(' ')
		kc, carb, prot, fat = input("kCal, Carb, Protein, Fat").split(',')
			
		self.foodmap[name] = Yemek(name,kc,carb,prot,fat,per,unit)
		print >> sys.stderr, "Inserted", name
		write()


	def removeprompt(self):
		name = input('Food Name:').strip()

		if name in self.foodmap:
			self.foodmap.remove(name)
			print >> sys.stderr, "Removed"
		else:
			print >> sys.stderr, "does not exist"
		write()

	def insertprompt(self):
		name = input('Food Name:').strip()

		if name in self.foodmap:
			print >> sys.stderr, "Food already exists!\n"
			print >> sys.stderr,  self.foodmap[name].printout()
			exit(-1)
		insert(name)


	def updateprompt(self):
		name = input('Food Name:').strip()

		if name in self.foodmap:
			print >> sys.stderr, "Currently:"
			print >> sys.stderr,  self.foodmap[name].printout()
		else:
			print >> sys.stderr, "New Food:"
		insert(name)
	
	def info(self,name):
		if name in self.foodmap:
			print >> sys.stderr,  self.foodmap[name].printout()
		else:
			print >> sys.stderr, "Cannot find:", name
			ans = input('insert?').strip()
			if ans[0].lower() == 'y':
				insert(name)


