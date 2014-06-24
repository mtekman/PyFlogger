#!/usr/bin/env python
from math import*
import sys

from Yemek import Yemek, Carb
from copy import copy

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
			if line.startswith('kc_total'):self.macro_kc = parseText(line)
			elif line.startswith('carb_total'):
				bad = parseText(line)
				self.macro_carb = Carb(bad,0,bad)
			elif line.startswith('protein_total'):self.macro_prot = parseText(line)
			elif line.startswith('fat_total'):self.macro_fat = parseText(line)
		f.close()
		


	def make(self,k,v,offs=0):
		r = self.rad
		d=range(-r,r)
		for y in d:
			t=""
			for x in d:
				if x*x+y*y<(r+offs)**2:
					a=(atan2(y,x))/pi/2+.5
					t=t+PieChart.s(k,v,a)
				else:t=t+" "

			pre_exist = self.circle[y]
			builder = ""
			if pre_exist!=[]:
				for c in xrange(len(t)):
					if t[c]!=' ':
						builder += t[c]
					else:
						builder += pre_exist[c]
			else:
				builder = t
			self.circle[y] = builder


	def printout(self, lmargin):
		l_count=0
		print ""
		r = len(self.circle)/2
		d=range(-r,r)
		for l in d:
			if l%2==0:continue
			
			line = self.circle[l]
			l_count += 1
			print "%s%s" % ("  ", line),
			
			if   l_count == 2:
				print self.totals_line,
			elif l_count == 3: 
				print self.cpf_line,
			elif l_count == 7:
				print self.allows_line,
			
			print ""
		print "\n\n"

		


	def __init__(self, c,p,f,kc, macrofile, lmargin = 6, radius=16, printme=True):

		if printme:
			self.circle = [[] for x in xrange(2*radius)]
			self.rad = radius
			lmarginal = lmargin - 20


		self.kc_current = kc
		self.carb_current = c # carb obj
		self.protein_current = p
		self.fat_current = f
		

		if printme:
			self.totals_line = ' ' * lmarginal
			
			outnow = "Totals :   %s" % Yemek.outformat
			outnow = '%'.join(outnow.split('%')[:-2])
			
			self.totals_line += outnow % (
				int(self.kc_current),
				self.carb_current.total, self.carb_current.fibre, self.carb_current.sugar, self.carb_current.bad,
				self.protein_current,
				self.fat_current,)


		self.setMacros(macrofile)

		#Allowed
		self.allow_kc = self.macro_kc - self.kc_current
		
		self.allow_carb = copy(self.macro_carb)
		self.allow_carb.sub(self.carb_current)
 		
 		self.allow_prot = self.macro_prot - self.protein_current
		self.allow_fat = self.macro_fat - self.fat_current

		if printme:
			self.allows_line = ' ' * lmarginal
			self.allows_line += " Allow :   %5d  %5.1f [%5.1f,%5.1f] = %4.1f  %4.1f  %4.1f" % (
				int(self.allow_kc), 
				self.allow_carb.total, self.allow_carb.fibre, self.allow_carb.sugar, self.allow_carb.bad,
				self.allow_prot,
				self.allow_fat)    
#
# Bit of a mess  - I was trying to overlay macro and current pie charts and though it works it looks ugly.
#			macro_total_fract = self.macro_carb.bad + self.macro_prot + self.macro_fat
#
#			c_rem = (self.macro_carb.bad - self.carb_current.bad)/macro_total_fract
#			c_cur = self.carb_current.bad/macro_total_fract
#
#			p_rem = (self.macro_prot - self.protein_current)/macro_total_fract
#			p_cur = self.protein_current/macro_total_fract
#
#			f_rem = (self.macro_fat - self.fat_current)/macro_total_fract
#			f_cur = self.fat_current/macro_total_fract
#
#			colors_outer="##%%$$"
#			colors_inner="-='\".:"
#
#			self.make(colors_outer,[c_rem,c_cur,p_rem,p_cur,f_rem,f_cur],offs=-1)
#			self.make(colors_inner,[c_rem,c_cur,p_rem,p_cur,f_rem,f_cur],offs=-1)

			current_total_fract = self.carb_current.bad + self.protein_current + self.fat_current

			c  = self.carb_current.bad/current_total_fract
			p = self.protein_current/current_total_fract
			f = self.fat_current/current_total_fract

#			colors=".%^"
			colors=".%+"
			self.make(colors,[c,p,f])

			mid_x, mid_y = (len(self.circle[0])/2)+1, self.rad/2
			mid_y = (mid_y - 5) if mid_y % 2 == 0 else mid_y
			kc_text = '[' + str(kc) + ']'

			offset_x = len(kc_text)
			mid_x -= offset_x		

			self.cpf_line = ' ' * lmarginal
			self.cpf_line += "  CPF  :                                %3.1f%%  %3.1f%% %3.1f%%" % (
				100*c, 100*p, 100*f)

			self.circle[mid_y] = self.circle[mid_y][:mid_x+2] + kc_text + self.circle[mid_y][mid_x+offset_x+2:]
			self.printout(lmargin+20)



#pc = PieChart(10,60,70,190, 8,8,True)
#print pc.kc_total, pc.carb_total, pc.protein_total, pc.fat_total
