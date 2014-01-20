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
    c=x
    for let in text:
      self.grid[y][c] = let
      c += 1

    
class WeightPlot:
  
  def __init__(self, array_of_tuples):
    self.rows, self.cols = map(lambda x: int(x), popen('stty size').read().split())
    self.screen = Grid(self.rows, self.cols)

    self.marg=3

    self.determineRanges(array_of_tuples)
    self.determineGrid()
    print >> sys.stderr, (self.min_x, self.max_x, self.min_y, self.max_y),\
    self.xspace_per_int, self.yspace_per_int
    
    self.setAxes()
    self.screen.printGrid()
    

  def setAxes(self):
    for y in xrange(self.marg,self.rows-self.marg):
      for x in xrange(self.marg, self.cols-self.marg):
        if y==(self.rows-(self.marg+1)):
          self.screen.grid[y][x] = '_'
        if x==self.marg:
          self.screen.grid[y][x] = '|'
          if y%3==0:
             self.screen.writeText(str(self.max_y - ((y+1)*self.yspace_per_int)), y, x-2)


  def determineRanges(self, tuples):
    tuples.sort(key=lambda x: x[0])
    self.min_x = tuples[0][0]
    self.max_x = tuples[-1][0]

    ysorted = sorted(tuples, key=lambda x: x[1])
    self.min_y = ysorted[0][1]
    self.max_y = ysorted[-1][1]

  def determineGrid(self):
     self.xspace_per_int = (self.cols-(2*self.marg))/(self.max_x - self.min_x)
     self.yspace_per_int = (self.rows-(2*self.marg))/(self.max_y - self.min_y)

                                                         
w = WeightPlot([[2,5],\
[3,9],\
[4,9],\
[8,1],\
[11,-3]])

