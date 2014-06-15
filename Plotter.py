#!/usr/bin/env python

import sys
from os import popen

'''Translates XYGraph into terminal window space'''
class Printer:
	
	def __init__(self, graphObj):	
		self.margX = 10
		self.margY = 6
		self.rows, self.columns= map(lambda x: int(x), popen('stty size').read().split());

		self.rows -= self.margY+1
		self.columns -= self.margX
						
		graphObj.scaleGrid(self.rows, self.columns)
		self.exgrid = graphObj.grid

		# scale
		ylen= len(self.exgrid)
		xlen= len(self.exgrid[0])
		
		
		#title
		print ' '*((self.columns/2)-5),"W/T chart",' '*((self.columns/2)-9)
		print "    ", '='*(self.columns), ' '*4

		for row in reversed(self.exgrid):
			print "".join(row)
		print ' '*((self.columns/2)-5),"Days Elapsed",' '*((self.columns/2)-9)

		
class Point:

	def __init__(self, x,y, text):
		self.x = x
		self.y = y
		self.val = text


'''Holds Points'''
class XYGraph:

	def __init__(self):
		self.points=[]
		self.minX = self.minY = sys.maxint
		self.maxX = self.maxY = 0
	
	
	def updateRange(self, v, axes):
		if axes=='x':
			if v < self.minX:
				self.minX=v
			if v > self.maxX:
				self.maxX=v
		if axes=='y':
			if v < self.minY:
				self.minY=v
			if v > self.maxY:
				self.maxY=v
	
	
	def addPoint(self, x,y,val):
		#Ranges
		self.updateRange(x,'x')
		self.updateRange(y,'y')
		
		# Insert into gridmap, yx
		p = Point(x,y,val)
		if p not in self.points:
			self.points.append(p)
		else:
			print "Dupe point", x,y


	def text2Array(self, text, array, start=0):
		if len(array) < len(text):
			array += [' ']* (len(text)-len(array))
	
		for x in xrange(len(text)):
			try:
				array[start+x] = text[x]
			except IndexError:
				pass


	
	def setAxes(self):

		#Y-axis
		for r in xrange(len(self.grid)):
			self.grid[r] = [' ',' ',' ',' ','|'] + self.grid[r]
			
			if r%3==1:
				coordY = "%.1f" % (self.minY + (float(r) / self.scaleY)) 
				self.text2Array(' '+str(coordY)+'_', self.grid[r] )


		#X-axis
		grid_row	= ['-'] * (len(self.grid[0])-3)
		hyphen_row = [' '] * (len(self.grid[0]))
		number_row = [' '] * (len(self.grid[0]))

		for r in xrange(len(self.grid[0])):
		
			coordX = int(self.minX + (float(r) / self.scaleX)) 
			
			if r%(len(str(coordX))+2)==0:
				hyphen_row[r] = '\\'
				self.text2Array( str(coordX), number_row, r )
		
		# Add margins
		grid_row	= ([' ']*5) + grid_row
		hyphen_row	= ([' ']*5) + hyphen_row
		number_row	= ([' ']*5) + number_row
		
		self.grid = [grid_row] + self.grid
		self.grid = [hyphen_row] + self.grid
		self.grid = [number_row] + self.grid
				

	def scaleGrid(self, rows,cols):

		self.grid=[]
		for r in xrange(rows):
			row = []
			for c in xrange(cols):
				row.append(' ')
			self.grid.append(row)
		
		#Rescale points
		xlen= self.maxX-self.minX
		ylen= self.maxY-self.minY
		
		self.scaleX = (float(cols-1)/xlen)  #(float(xlen)/cols)
		self.scaleY = (float(rows-1)/ylen)  #(float(ylen)/rows)+1

		for p in self.points:
			coordX = int(float(p.x - self.minX) * self.scaleX )
			coordY = int(float(p.y - self.minY) * self.scaleY )
			
			row_i = self.grid[coordY]
#			plotval = "[%s=%.1f,%.1f]" % (p.val, p.x, p.y)
			plotval = "%s" % p.val

#			if coordX > cols-10:
#				plotval += "__."
#				self.text2Array( plotval, row_i, coordX-len(plotval) )
#			else:
#				plotval = ".__" + plotval
#				self.text2Array( plotval, row_i, coordX )
			self.text2Array( plotval, row_i, coordX )
		
		self.setAxes()
				



#xy = XYGraph()
#xy.addPoint(10.9,10,"a")
#xy.addPoint(20,20.2,"b")
#xy.addPoint(30.3,30,"c")
#xy.addPoint(40,40.4,"d")
#p = Printer(xy)
