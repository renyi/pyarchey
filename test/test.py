#!/usr/bin/env python
import sys
sys.path.insert(0, '../')

import pyarchey.pyarchey as py

o = py.Output()
print 'Distro Name    Pretty Name'
print '---------------------------'
print o.readDistro('./slack.test')
print o.readDistro('./arch.test')
print o.readDistro('./raspbian.test')