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
		for line in self.circle:
			print "%s%s" % ( (' '*lmargin), line)
		print ""


	def __init__(self, c,p,f,kc, lmargin = 6, radius=6):

		total = c + p + f
		
		self.c = float(c)/total
		self.p = float(p)/total
		self.f = float(f)/total

		self.circle = []
		self.make("#.+",[self.c,self.p,self.f],radius)

		mid_x, mid_y = len(self.circle[0])/2, len(self.circle)/2
		kc_text = str(kc)

		offset_x = len(kc_text)
		mid_x -= offset_x
		
		print >> sys.stderr,'\n',' '*(lmargin),
		print >> sys.stderr, " CPF  :\t      \t%.1f%%\t%.1f%%\t%.1f%%\n" % (100*self.c, 100*self.p, 100*self.f)
		self.circle[mid_y] = self.circle[mid_y][:mid_x+2] + kc_text + self.circle[mid_y][mid_x+offset_x+2:]

		self.printout(lmargin+20)



#pc = PieChart(10,60,70,190)
