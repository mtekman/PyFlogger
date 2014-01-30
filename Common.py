#!/usr/bin/env python

import sys
from os.path import abspath, expanduser
from time import localtime, time




#Global method
def ynprompt(message):
	ans = raw_input(message)
	return (ans[0].lower()=='y')
