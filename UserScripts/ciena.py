#!/usr/bin/python

from Switch import *

try:
	sw = Switch("10.0.0.140", "ciena")
	sw.Prompt()
except KeyboardInterrupt:
	print
	print
	exit(0)
