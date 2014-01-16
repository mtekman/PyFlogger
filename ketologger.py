#!/usr/bin/env python

import sys
from time import localtime as time


class Args:

	def __init__(self,argv):
		self.argv = argv
		self.insert = False
		self.update = False
		self.remove = False


	def parse(self):
		for arg in self.argv:
			if arg=="insert":
				doNothing()
