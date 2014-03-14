#!/usr/bin/env python

import FoodList

class Suggest:
	def __init__(self, foodlist_obj, kc, carb, prot, fat):
		self.foodlist = foodlist_obj.foodmap
		self.allowed_kc = kc
		self.allowed_carb = carb
		self.allowed_prot = prot
		self.allowed_fat = fat

		
		self.suggestSomething()

	def suggestSomething(self):
		res=[]
		decr=100

		while ((decr > 0) and (len(res)==0)):
			res = self.checkAvail(decr)
			decr -= 20

		self.res = res
		self.printout(res)


	def checkAvail(self, perc):
		found=[]

		for food in self.foodlist:
			scaled = food.scaled( float(perc) / 100 )

			if 
