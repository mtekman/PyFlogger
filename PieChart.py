#!/usr/bin/env python
from math import*
import sys

class PieChart:

	@staticmethod
	def s(k,v,a):
		if not v:return ' '
		if a<=v[0]:return k[0]
		return PieChart.s(k[1:],v[1:],a-v[0])

	def make(self,k,v,r):
		d=range(-r,r)
		for y in d:
			if y%2==0:continue

			t=""
			for x in d:
				if x*x+y*y<r*r:
					a=atan2(y,x)/pi/2+.5
					t=t+PieChart.s(k,v,a)
				else:t=t+" "
			self.circle.append(t)

	def printout(self, lmargin):
		l_count=0
		print ""
		for line in self.circle:
			l_count += 1
			print "%s%s" % ("  ", line),
			
			if   l_count == 2:
				print self.totals_line,
			elif l_count == 3: 
				print self.cpf_line,
			elif l_count == 7:
				print self.allows_line,
			
			print ""
		print ""


	def __init__(self, c,p,f,kc, lmargin = 6, radius=6):

		colors="/-|"

		self.total = c + p + f
		self.circle = []
		self.rad = radius/2

		self.kc_total = kc
		self.carb_total = c
		self.protein_total = p
		self.fat_total = f
		
		lmarginal = lmargin - 20

		self.totals_line = ' ' * lmarginal
		self.totals_line += "Totals :\t%d\t%s\t%s\t%s" % (
			int(self.kc_total),
			self.carb_total,
			self.protein_total,
			self.fat_total)

                #Allowed
                #1350   18      76      75
                self.kc_total -= 1350
                self.carb_total -= 18
                self.protein_total -= 76
                self.fat_total -= 75

		self.allows_line = ' ' * lmarginal
		self.allows_line += " Allow :\t%d\t%s\t%s\t%s" % (
			int(-self.kc_total), 
			-self.carb_total,
			-self.protein_total,
			-self.fat_total)    
		
		self.c = float(c)/self.total
		self.p = float(p)/self.total
		self.f = float(f)/self.total

		self.make(colors,[self.c,self.p,self.f],radius)

		mid_x, mid_y = (len(self.circle[0])/2)+1, len(self.circle)/2
		mid_y = (mid_y - 1) if mid_y % 2 == 0 else mid_y
		kc_text = '[' + str(kc) + ']'

		offset_x = len(kc_text)
		mid_x -= offset_x		

		self.cpf_line = ' ' * lmarginal
		self.cpf_line += "  CPF  :\t      \t%.1f%%\t%.1f%%\t%.1f%%" % (
			100*self.c, 100*self.p, 100*self.f)

		self.circle[mid_y] = self.circle[mid_y][:mid_x+2] + kc_text + self.circle[mid_y][mid_x+offset_x+2:]
		self.printout(lmargin+20)



#pc = PieChart(10,60,70,190)
