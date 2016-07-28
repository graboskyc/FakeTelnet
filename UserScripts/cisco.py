#!/usr/bin/python

from Switch import *

try:
        sw = Switch("10.0.0.141", "ios")
        sw.Prompt()
except KeyboardInterrupt:
        print
        print
        exit(0)
