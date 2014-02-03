#!/usr/bin/env python

import sys
from os import popen
from time import sleep

class Grid:
	def __init__(self, rows, cols):
		self.grid = []
		self.rows = rows
		self.cols = cols
		self.marg = 3
    
		for y in xrange(rows):
			row = []
			for x in xrange(cols):
				row.append(' ')
			self.grid.append(row)


	def printGrid(self):
		for y in xrange(len(self.grid)):
			print reduce(lambda x,y: x+y, self.grid[y])
			
	def writeText(self, text, y, x):
		try:
			text += 0			
			if text<0:
				x -= 1
			
			text= "%0.1f" % text
		except TypeError:
			pass

		
		c = x
		for let in text:
			self.grid[y][c] = let
			c += 1

    
class WeightPlot:
  
  def __init__(self, array_of_tuples):
    self.rows, self.cols = map(lambda x: int(x), popen('stty size').read().split())
    self.screen = Grid(self.rows, self.cols)

    self.marg=4

    self.determineRanges(array_of_tuples)
    self.determineGrid()
    
    self.setAxes()
    self.plotPoints(array_of_tuples)
    self.screen.printGrid()
  
    print array_of_tuples
      
#    print >> sys.stderr, (self.min_x, self.max_x, self.min_y, self.max_y),\
#    self.xspace_per_int, self.yspace_per_int
	
    
  def plotPoints(self, array):

		for arr in array:
			y,x = arr
			
			grid_y = self.translateVal2Coord(y,False)
			grid_x = self.translateVal2Coord(x,True)
			
			print "yy=",grid_y, " xx=", grid_x
			
			self.screen.writeText('x [%.1f,%.1f]' %(x,y), grid_y, grid_x)


  def setAxes(self, xresol=5, yresol=2):

    for y in xrange(self.marg+1,self.rows-self.marg):
      for x in xrange(self.marg+1, self.cols-self.marg):
        if y==(self.rows-(self.marg)-1):
          self.screen.grid[y][x] = '_'
          if x%xresol==0:
             self.screen.writeText('/', y+1, x)
             self.screen.writeText( ((self.min_x + ((x-self.marg)/self.xspace_per_int))  ), y+2, x)
        if x==self.marg+1:
          self.screen.grid[y][x] = '|'
          if y%yresol==0:
             self.screen.writeText('/', y, x-1)
             self.screen.writeText( ((self.max_y - ((y-self.marg)/self.yspace_per_int)) ), y, x-4)


  def determineRanges(self, tuples):
    tuples.sort(key=lambda x: x[0])
    self.min_x = tuples[0][0] - 1
    self.max_x = tuples[-1][0] + 1

    ysorted = sorted(tuples, key=lambda x: x[1])
    self.min_y = ysorted[0][1] - 1
    self.max_y = ysorted[-1][1] + 1

  def determineGrid(self):
     self.xspace_per_int = (float(self.cols-(2*self.marg))/(self.max_x - self.min_x))
     self.yspace_per_int = (float(self.rows-(2*self.marg))/(self.max_y - self.min_y))
     if self.yspace_per_int==0:
     	self.yspace_per_int = 1

  def translateVal2Coord(self, val, isX):
		if isX:
			return int( (val - (self.min_x + 1))*self.xspace_per_int)+self.marg)
#			return  self.min_x + ((val-self.marg)/self.xspace_per_int)
		else:
			return int((-(val - (self.max_y-1))*self.yspace_per_int)+self.marg)
#			return self.max_y - ((y-self.marg)/self.yspace_per_int)


                                                         
w = WeightPlot([[2,5],\
[3,9],\
[4,9],\
[8,1],\
[11,-3],\
[11,-9]])

