#!/usr/bin/env python
# import sys
# sys.path.insert(0, '../')

import pyarchey.pyarchey as py

# o = py.Output()
# print 'Distro Name    Pretty Name'
# print '---------------------------'
# print o.readDistro('./slack.test')
# print o.readDistro('./arch.test')
# print o.readDistro('./raspbian.test')

def test_slack():
	o = py.Output()
	assert o.readDistro('./test/slack.test') == ('Slackware', 'Slackware 14.1')
	
def test_arch():
	o = py.Output()
	assert o.readDistro('./test/arch.test') == ('Arch Linux', 'Arch Linux')

def test_raspbian():
	o = py.Output()
	assert o.readDistro('./test/raspbian.test') == ('Raspbian', 'Raspbian 7 (wheezy)')