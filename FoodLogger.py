#!/usr/bin/env python

class FoodLogger:
	def __init__(self, FoodL,  file="~/.config/keto/foodlog.txt"):
		self.foodlog=[]
		self.path= file
		self.foodlist = FoodL # i.e. ref FoodList cobj
		self.date = "%04d/%02d/%02d--%02d:%02d" % time()[0:5]
		read(self.date)

	# any date
	def read(self,date):
		f=open(self.path,'r')
		
		# Strip Header
		f.readline()

		for line in f:
			ddate, amount, yemek = line.split('|')

			if date == ddate:
				food = Yemek(yemek,amount)
				self.foodlog.append(food)
		f.close()


	def showTotals(self,date):
		self.read(date)
		
		kC_total=0
		carb_total=0
		protein_total=0
		fat_total=0

		if len(self.foodlog)==0:
			print >> sys.stderr, "nothing logged for that day!"
			exit(-1)

		print >> sys.stderr, self.foodlog[0].printout(headeronly=True)

		for y in self.foodlog:
			scale = y.amount 

			kC_total += y.kC
			carb_total += y.carb
			protein_total += y.prot
			fat_total += y.fat

			print >> sys.stderr, y.printout(False)
		print >> sys.stderr, "Totals:\t%s\t%s\t%s\t%s\t%s" % (kC_total, carb_total, protein_total, fat_total)


	def log(self):
		name = input("Food:").strip()
		self.foodlist.info(name)
		
		am = int(input("amount consumed?").strip())
		yemk = Yemek(self.foodmap[name],am)
		
		dater = "%04d/%02d/%02d--%02d:%02d" % time()[0:5]

		f=open(self.path,'a')
		print >> f, "%s|%d|%s" % (dater,am,newy.printout(False))
		f.close()
