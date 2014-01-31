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
      text += 1
      text= "%d"
    except ValueError:
    c=x
    for let in str(text):
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
    self.screen.printGrid()
    print >> sys.stderr, (self.min_x, self.max_x, self.min_y, self.max_y),\
    self.xspace_per_int, self.yspace_per_int
	
    

  def setAxes(self, xresol=5, yresol=2):
#    xresol=self.xspace_per_int

    for y in xrange(self.marg,self.rows-self.marg):
      for x in xrange(self.marg, self.cols-self.marg):
        if y==(self.rows-(self.marg)-1):
          self.screen.grid[y][x] = '_'
          if x%xresol==0:
             self.screen.writeText('/', y+1, x)
             self.screen.writeText( ((self.min_x + ((x-self.marg)/self.xspace_per_int))  ), y+2, x)
        if x==self.marg:
          self.screen.grid[y][x] = '|'
          if y%yresol==0:
             self.screen.writeText( ((self.max_y - ((y-self.marg)/self.yspace_per_int)) ), y, x-2)


  def determineRanges(self, tuples):
    tuples.sort(key=lambda x: x[0])
    self.min_x = tuples[0][0]
    self.max_x = tuples[-1][0]

    ysorted = sorted(tuples, key=lambda x: x[1])
    self.min_y = ysorted[0][1]
    self.max_y = ysorted[-1][1]

  def determineGrid(self):
     self.xspace_per_int = (float(self.cols-(2*self.marg))/(self.max_x - self.min_x))
     self.yspace_per_int = (float(self.rows-(2*self.marg))/(self.max_y - self.min_y))
     if self.yspace_per_int==0:
     	self.yspace_per_int = 1

                                                         
w = WeightPlot([[2,5],\
[3,9],\
[4,9],\
[8,1],\
[11,-3],\
[11,-9]])

