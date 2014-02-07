#!/usr/bin/env python

import sys
from os import popen

'''Translates XYGraph into terminal window space'''
class Printer:
	
	def __init__(self, graphObj):	
		self.margX = 10
		self.margY = 6
		self.rows, self.columns= map(lambda x: int(x), popen('stty size').read().split());

		self.rows -= self.margY
		self.columns -= self.margX
						
		graphObj.scaleGrid(self.rows, self.columns)
		self.exgrid = graphObj.grid

		# scale
		ylen= len(self.exgrid)
		xlen= len(self.exgrid[0])
		
		print '#'* len(self.exgrid[0])
		for row in reversed(self.exgrid):
			print "".join(row)
		print '#'* len(self.exgrid[0])

		
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
		
		scaleX = (float(cols-1)/xlen)  #(float(xlen)/cols)
		scaleY = (float(rows-1)/ylen)  #(float(ylen)/rows)+1

		for p in self.points:
			coordX = int(float(p.x - self.minX) * scaleX )
			coordY = int(float(p.y - self.minY) * scaleY )
			
			print '(',p.x,',',p.y,')--D', coordX, coordY, p.val
			
			if coordX > cols-4:
				plotval="[%s]__." % p.val
				self.grid[coordY][coordX-len(plotval)] = plotval
			else:
				self.grid[coordY][coordX] = ".__[%s]" % p.val
		
		
				

		


xy = XYGraph()
xy.addPoint(10,10,"a")
xy.addPoint(20,20,"b")
xy.addPoint(30,30,"c")
xy.addPoint(40,40,"d")

p = Printer(xy)
