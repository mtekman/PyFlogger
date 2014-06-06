#!/usr/bin/env python
from math import*
import sys

class PieChart:

	@staticmethod
	def s(k,v,a):
		if not v:return ' '
		if a<=v[0]:return k[0]
		return PieChart.s(k[1:],v[1:],a-v[0])


	def setMacros(self, macrofile):
		periodmap = {'day':1, 'week':5}

		def parseText(line):
			junk, eqs = line.split('=')
			value, period = eqs.split('/')
			return float(value)/periodmap[period.strip()]
			

		f = open( macrofile ,'r')


		for line in f:
			if line.startswith('kc_total'):
				self.macro_kc = parseText(line)
			elif line.startswith('carb_total'):
				self.macro_carb = parseText(line)
			elif line.startswith('protein_total'):
				self.macro_prot = parseText(line)
			elif line.startswith('fat_total'):
				self.macro_fat = parseText(line)
			
		f.close()
		





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

		


	def __init__(self, c,p,f,kc, macrofile, lmargin = 6, radius=8, printme=True):

		if printme:
			colors="/-|"

			self.circle = []
			self.rad = radius/2
			lmarginal = lmargin - 20


		self.kc_current = kc
		self.carb_current = c
		self.protein_current = p
		self.fat_current = f
		

		if printme:
			self.totals_line = ' ' * lmarginal
			self.totals_line += "Totals :\t%d\t%s\t%s\t%s" % (
				int(self.kc_current),
				self.carb_current,
				self.protein_current,
				self.fat_current)


		self.setMacros(macrofile)

#		print "kc,carb,prot,fat", self.macro_kc, self.macro_carb, self.macro_prot, self.macro_fat

		#Allowed
		self.macro_kc -= self.kc_current
		self.macro_carb -= self.carb_current
 		self.macro_prot -= self.protein_current
		self.macro_fat -= self.fat_current


#		print "kc,carb,prot,fat", self.macro_kc, self.macro_carb, self.macro_prot, self.macro_fat
		total_fract = self.macro_carb + self.macro_prot + self.macro_fat

		if printme:
			self.allows_line = ' ' * lmarginal
			self.allows_line += " Allow :\t%d\t%s\t%s\t%s" % (
				int(self.macro_kc), 
				self.macro_carb,
				self.macro_prot,
				self.macro_fat)    
		
		c = self.macro_carb/total_fract
		p = self.macro_prot/total_fract
		f = self.macro_fat/total_fract


		if printme:
			self.make(colors,[c,p,f],radius)

			mid_x, mid_y = (len(self.circle[0])/2)+1, len(self.circle)/2
			mid_y = (mid_y - 1) if mid_y % 2 == 0 else mid_y
			kc_text = '[' + str(kc) + ']'

			offset_x = len(kc_text)
			mid_x -= offset_x		

			self.cpf_line = ' ' * lmarginal
			self.cpf_line += "  CPF  :\t      \t%.1f%%\t%.1f%%\t%.1f%%" % (
				100*c, 100*p, 100*f)

			self.circle[mid_y] = self.circle[mid_y][:mid_x+2] + kc_text + self.circle[mid_y][mid_x+offset_x+2:]
			self.printout(lmargin+20)



#pc = PieChart(10,60,70,190, 8,8,True)
#print pc.kc_total, pc.carb_total, pc.protein_total, pc.fat_total
