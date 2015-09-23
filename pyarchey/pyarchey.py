#!/usr/bin/env python
#
#
# pyarchey is a simple system information tool written in Python.
#
# Copyright 2015 Kevin Walchko <kevin.walchko@outlook.com>
# Copyright 2010 Melik Manukyan <melik@archlinux.us>
# Copyright 2010 David Vazgenovich Shakaryan <dvshakaryan@gmail.com>
#
# ASCII art by Brett Bohnenkamper <kittykatt@silverirc.com>
# Changes Jerome Launay <jerome@projet-libre.org>
# Fedora support by YeOK <yeok@henpen.org>
#
# Distributed under the terms of the GNU General Public License v3.
# See http://www.gnu.org/licenses/gpl.txt for the full license text.
##############################################################################
#
#


# For more info on psutil, see https://pythonhosted.org/psutil/
#
# Import libraries
import os                               # fileCheck, tries to determine distribution
import re                               # used by CPU
import uuid                             # mac address
from subprocess import Popen, PIPE      # call commandline programs
from sys import platform as _platform   # distribution
import socket                           # ip address
import psutil as ps                     # system info
import datetime as dt                   # uptime
import json                             # json
import argparse                         # handle command line args
#import unittest                         # unit test
import math								# handle memory sizes
import platform							# get system info - not used yet

#---------------Dictionaries---------------#
#  https://wiki.archlinux.org/index.php/Color_Bash_Prompt
# escape[ x;y   x-{0 normal 1 bold} y-color
CLR="\033[0;0m"   # normal color scheme
BK ="\033[0;30m"   # black
BL ="\033[0;34m"   # blue
GR ="\033[0;32m"   # green
CY ="\033[0;36m"   # cyan
RD ="\033[0;31m"   # red
PL ="\033[0;35m"   # purple
YW ="\033[0;33m"   # yellow
GY ="\033[0;30m"   # grey
LG ="\033[0;37m"   # light grey

# Bold colors (note be 'B' before the color name)
BBK ="\033[1;30m"   # black
BBL ="\033[1;34m"   # blue
BGR ="\033[1;32m"   # green
BCY ="\033[1;36m"   # cyan
BRD ="\033[1;31m"   # red
BPL ="\033[1;35m"   # purple
BYW ="\033[1;33m"   # yellow
BGY ="\033[1;30m"   # grey
BLG ="\033[1;37m"   # light grey

colorDict = {
	'Arch Linux':		[BL, BBL],
	'Ubuntu':			[RD, BRD, BYW],
	'FreeBSD':			[RD, BRD, YW],
	'Mac OSX':			[CLR, CY],
	'Debian':			[RD, BRD],
	'Raspbian':			[RD, BRD],
	'LinuxMint':		[BLG, BGR],
	'Gentoo':			[BPL, BLG],
	'OpenBSD':			[BYW, BYW, YW],
	'Fedora':			[BLG, BBL, BL],
	'openSUSE project': [BLG, BGR],
	'Slackware':		[BLG, BL, BBL],
	'Linux':			[CLR, BBL],
	'Sensors':			[BRD, BGR, BYW],
	'Clear':			[CLR]
	}

logosDict = {'Arch Linux': """{color[1]}
{color[1]}               +                {results[0]}
{color[1]}               #                {results[1]}
{color[1]}              ###               {results[2]}
{color[1]}             #####              {results[3]}
{color[1]}             ######             {results[4]}
{color[1]}            ; #####;            {results[5]}
{color[1]}           +##.#####            {results[6]}
{color[1]}          +##########           {results[7]}
{color[1]}         ######{color[0]}#####{color[1]}##;         {results[8]}
{color[1]}        ###{color[0]}############{color[1]}+        {results[9]}
{color[1]}       #{color[0]}######   #######        {results[10]}
{color[0]}     .######;     ;###;`\".      {results[11]}
{color[0]}    .#######;     ;#####.       {results[12]}
{color[0]}    #########.   .########`
{color[0]}   ######'           '######
{color[0]}  ;####                 ####;
{color[0]}  ##'                     '##
{color[0]} #'                         `#
\x1b[0m"""
,'FreeBSD':"""{color[0]}
{color[0]}  ```                        `    {results[0]}
{color[0]} s` `.....---.......--.```   -/   {results[1]}
{color[0]} +o   .--`         /y:`      +.   {results[2]}
{color[0]}  yo`:.            :o      `+-    {results[3]}
{color[0]}   y/               -/`   -o/     {results[4]}
{color[0]}  .-                  ::/sy+:.    {results[5]}
{color[0]}  /                     `--  /    {results[6]}
{color[0]} `:                          :`   {results[7]}
{color[0]} `:                          :`   {results[8]}
{color[0]}  /                          /    {results[9]}
{color[0]}  .-                        -.    {results[10]}
{color[0]}   --                      -.     {results[11]}
{color[0]}    `:`                  `:`      {results[12]}
{color[0]}      .--             `--.
{color[0]}         .---.....----.
{color[0]}
{color[0]}
{color[0]}
\x1b[0m"""
,'Debian':"""{color[0]}
{color[1]}           _sudZUZ#Z#XZo=_        {results[0]}
{color[1]}        _jmZZ2!!~---~!!X##wx      {results[1]}
{color[1]}     .<wdP~~            -!YZL,    {results[2]}
{color[1]}    .mX2'       _xaaa__     XZ[.  {results[3]}
{color[1]}    oZ[      _jdXY!~?S#wa   ]Xb;  {results[4]}
{color[1]}   _#e'     .]X2(     ~Xw|  )XXc  {results[5]}
{color[1]}  .2Z`      ]X[.       xY|  ]oZ(  {results[6]}
{color[1]}  .2#;      )3k;     _s!~   jXf`  {results[7]}
{color[0]}   1Z>      -]Xb/    ~    __#2(   {results[8]}
{color[0]}   -Zo;       +!4ZwerfgnZZXY'     {results[9]}
{color[0]}    *#[,        ~-?!!!!!!-~       {results[10]}
{color[0]}     XUb;.                        {results[11]}
{color[0]}      )YXL,,                      {results[12]}
{color[0]}        +3#bc,
{color[0]}          -)SSL,,
{color[0]}             ~~~~~
\x1b[0m"""
,'Raspbian':"""{color[0]}
{color[0]}        .~~.   .~~.      {results[0]}
{color[0]}       '. \ ' ' / .'     {results[1]}
{color[0]}        .~ .~~~..~.      {results[2]}
{color[0]}       : .~.'~'.~. :     {results[3]}
{color[0]}      ~ (   ) (   ) ~    {results[4]}
{color[0]}     ( : '~'.~.'~' : )   {results[5]}
{color[0]}      ~ .~ (   ) ~. ~    {results[6]}
{color[0]}       (  : '~' :  )     {results[7]}
{color[0]}        '~ .~~~. ~'      {results[8]}
{color[0]}            '~'          {results[9]}
{color[0]}                         {results[10]}
{color[0]}                         {results[11]}
{color[0]}                         {results[12]}
\x1b[0m"""
,'Ubuntu':"""{color[0]}
{color[0]}                          .oyhhs:   {results[0]}
{color[1]}                 ..--.., {color[0]}shhhhhh-   {results[1]}
{color[1]}               -+++++++++`:{color[0]}yyhhyo`  {results[2]}
{color[2]}          .--  {color[1]}-++++++++/-.-{color[0]}::-`    {results[3]}
{color[2]}        .::::-   {color[1]}:-----:/+++/++/.   {results[4]}
{color[2]}       -:::::-.          {color[1]}.:++++++:  {results[5]}
{color[1]}  ,,, {color[2]}.:::::-`             {color[1]}.++++++- {results[6]}
{color[1]}./+++/-{color[2]}`-::-                {color[1]}./////: {results[7]}
{color[1]}+++++++ {color[2]}.::-                        {color[1]}{results[8]}
{color[1]}./+++/-`{color[2]}-::-                {color[0]}:yyyyyo {results[9]}
{color[1]}  ``` `{color[2]}-::::-`             {color[0]}:yhhhhh: {results[10]}
{color[2]}       -:::::-.         {color[0]}`-ohhhhhh+  {results[11]}
{color[2]}        .::::-` {color[0]}-o+///+oyhhyyyhy:   {results[12]}
{color[2]}         `.--  {color[0]}/yhhhhhhhy+{color[2]},....
{color[0]}               /hhhhhhhhh{color[2]}-.-:::;
{color[0]}               `.:://::- {color[2]}-:::::;
{color[2]}                         `.-:-'
{color[2]}
\x1b[0m"""
,'LinuxMint':"""{color[0]}
{color[0]} MMMMMMMMMMMMMMMMMMMMMMMMMmds+.      {results[0]}
{color[0]} MMm----::-://////////////oymNMd+`   {results[1]}
{color[0]} MMd      {color[1]}/++                {color[0]}-sNMd:  {results[2]}
{color[0]} MMNso/`  {color[1]}dMM    `.::-. .-::.`{color[0]} .hMN: {results[3]}
{color[0]} ddddMMh  {color[1]}dMM   :hNMNMNhNMNMNh: `{color[0]}NMm {results[4]}
{color[0]}     NMm  {color[1]}dMM  .NMN/-+MMM+-/NMN` {color[0]}dMM {results[5]}
{color[0]}     NMm  {color[1]}dMM  -MMm  `MMM   dMM. {color[0]}dMM {results[6]}
{color[0]}     NMm  {color[1]}dMM  -MMm  `MMM   dMM. {color[0]}dMM {results[7]}
{color[0]}     NMm  {color[1]}dMM  .mmd  `mmm   yMM. {color[0]}dMM {results[8]}
{color[0]}     NMm  {color[1]}dMM`  ..`   ...   ydm. {color[0]}dMM {results[9]}
{color[0]}     hMM-  {color[1]}+MMd/-------...-:sdds {color[0]}MMM {results[10]}
{color[0]}     -NMm-  {color[1]}:hNMNNNmdddddddddy/` {color[0]}dMM {results[11]}
{color[0]}      -dMNs-``{color[1]}-::::-------.``    {color[0]}dMM {results[12]}
{color[0]}       `/dMNmy+/:-------------:/yMMM
{color[0]}          ./ydNMMMMMMMMMMMMMMMMMMMMM
{color[0]}
{color[0]}
{color[0]}
\x1b[0m"""
,'Fedora':"""{color[0]}
{color[2]}           :/------------://        {results[0]}
{color[2]}        :------------------://      {results[1]}
{color[2]}      :-----------{color[0]}/shhdhyo/{color[2]}-://     {results[2]}
{color[2]}    /-----------{color[0]}omMMMNNNMMMd/{color[2]}-:/    {results[3]}
{color[2]}   :-----------{color[0]}sMMMdo:/{color[2]}       -:/   {results[4]}
{color[2]}  :-----------{color[0]}:MMMd{color[2]}-------    --:/  {results[5]}
{color[2]}  /-----------{color[0]}:MMMy{color[2]}-------    ---/  {results[6]}
{color[2]} :------    --{color[0]}/+MMMh/{color[2]}--        ---: {results[7]}
{color[2]} :---     {color[0]}oNMMMMMMMMMNho{color[2]}     -----: {results[8]}
{color[2]} :--      {color[0]}+shhhMMMmhhy++{color[2]}   ------:  {results[9]}
{color[2]} :-      -----{color[0]}:MMMy{color[2]}--------------/  {results[10]}
{color[2]} :-     ------{color[0]}/MMMy{color[2]}-------------:   {results[11]}
{color[2]} :-      ----{color[0]}/hMMM+{color[2]}------------:    {results[12]}
{color[2]} :--{color[0]}:dMMNdhhdNMMNo{color[2]}-----------:
{color[2]} :---{color[0]}:sdNMMMMNds:{color[2]}----------:
{color[2]} :------{color[0]}:://:{color[2]}-----------://
{color[2]} :--------------------://
{color[2]}
\x1b[0m"""
,'openSUSE project':"""{color[0]}
{color[1]}        +########_ #=.    {results[0]}
{color[1]}      ################-#  {results[1]}
{color[1]}    =################ -:+ {results[2]}
{color[1]}   ################+# #~# {results[3]}
{color[1]}  ################## ==#= {results[4]}
{color[1]} :##+:################-_# {results[5]}
{color[1]} ## `_  ##########=###=`  {results[6]}
{color[1]} #._###- ##   .##.        {results[7]}
{color[1]} #`#~ `# ##    `#_^       {results[8]}
{color[1]} ## ## #  #     ^#        {results[9]}
{color[1]}  #=  ##                  {results[10]}
{color[1]}   ####                   {results[11]}
{color[1]}                          {results[12]}
{color[1]}
{color[1]}
{color[1]}
\x1b[0m"""
, 'Slackware':"""{color[0]}
{color[1]}                   :::::::                    {results[0]}
{color[1]}             :::::::::::::::::::              {results[1]}
{color[1]}          :::::::::::::::::::::::::           {results[2]}
{color[1]}        ::::::::{color[0]}cllcccccllllllll{color[1]}::::::        {results[3]}
{color[1]}     :::::::::{color[0]}lc               dc{color[1]}:::::::      {results[4]}
{color[1]}    ::::::::{color[0]}cl   clllccllll    oc{color[1]}:::::::::    {results[5]}
{color[1]}   :::::::::{color[0]}o   lc{color[1]}::::::::{color[0]}co   oc{color[1]}::::::::::   {results[6]}
{color[1]}  ::::::::::{color[0]}o    cccclc{color[1]}:::::{color[0]}clcc{color[1]}::::::::::::  {results[7]}
{color[1]}  :::::::::::{color[0]}lc        cclccclc{color[1]}:::::::::::::  {results[8]}
{color[1]} ::::::::::::::{color[0]}lcclcc          lc{color[1]}:::::::::::: {results[9]}
{color[1]} ::::::::::{color[0]}cclcc{color[1]}:::::{color[0]}lccclc     oc{color[1]}::::::::::: {results[10]}
{color[1]} ::::::::::{color[0]}o    l{color[1]}::::::::::{color[0]}l    lc{color[1]}::::::::::: {results[11]}
{color[1]}  :::::{color[0]}cll{color[1]}:{color[0]}o     clcllcccll     o{color[1]}:::::::::::  {results[12]}
{color[1]}  :::::{color[0]}occ{color[1]}:{color[0]}o                  clc{color[1]}:::::::::::
{color[1]}   ::::{color[0]}ocl{color[1]}:{color[0]}ccslclccclclccclclc{color[1]}:::::::::::::
{color[1]}    :::{color[0]}oclcccccccccccccllllllllllllll{color[1]}:::::
{color[1]}     ::{color[0]}lcc1lcccccccccccccccccccccccco{color[1]}::::
{color[1]}       ::::::::::::::::::::::::::::::::
{color[1]}         ::::::::::::::::::::::::::::
{color[1]}            ::::::::::::::::::::::
{color[1]}                 ::::::::::::
{color[1]}
\x1b[0m"""
, 'Mac OSX':"""{color[0]}
{color[0]}                  ##             {results[0]}
{color[0]}               ####              {results[1]}
{color[0]}               ##                {results[2]}
{color[0]}       #######    #######        {results[3]}
{color[0]}     ######################      {results[4]}
{color[0]}    #####################        {results[5]}
{color[0]}    ####################         {results[6]}
{color[0]}    ####################         {results[7]}
{color[0]}    #####################        {results[8]}
{color[0]}     ######################      {results[9]}
{color[0]}      ####################       {results[10]}
{color[0]}        ################         {results[11]}
{color[0]}          ###     ####           {results[12]}
\x1b[0m"""
,'Gentoo':"""{color[0]}
{color[0]}        __q@@@@m             {results[0]}
{color[0]}      _q@@@@@@@@@@_          {results[1]}
{color[0]}     _@@@@@@@@@@@@@@m        {results[2]}
{color[0]}    q@@@@@@@@@@@@@@@@@_      {results[3]}
{color[0]}   _@@@@@@@@@@##@@@@@@@h     {results[4]}
{color[0]}   @@@@@@@@@@@ ##@@@@@@@@_   {results[5]}
{color[0]}   7##@@@@@@@___@@@@@@@@@@,  {results[6]}
{color[0]}     ####@@@@@@@@@@@@@@@@@@  {results[7]}
{color[0]}       ####@@@@@@@@@@@@@@@@  {results[8]}
{color[0]}        q@@@@@@@@@@@@@@@@#W  {results[9]}
{color[0]}       q@@@@@@@@@@@@@@@@@@/  {results[10]}
{color[0]}     _@@@@@@@@@@@@@@@@#@@    {results[11]}
{color[0]}    q@@@@@@@@@@@@@@@#@##^    {results[12]}
{color[0]}   m#@@@@@@@@@@@@@@#@#W
{color[0]}  _q@@@@@@@@@@@@@#@#*>
{color[0]}   p@@@@@@@@@@@#@##%
{color[0]}    _##@@@@@##@#@#g
{color[0]}      _#@@@@@@#@@
{color[0]}        _p@@@@q
\x1b[0m"""
,'OpenBSD':"""{color[0]}
{color[0]}               |    .            {results[0]}
{color[0]}           .   |L  /|   .        {results[1]}
{color[0]}       _ . | _| --+._/| .        {results[2]}
{color[0]}      / ||| Y J  )   / |/| ./    {results[3]}
{color[0]}     J  |)'( |        ` F`.'/    {results[4]}
{color[0]}   -<|  F         __     .-<     {results[5]}
{color[0]}     | /       .-'. `.  /-. L___ {results[6]}
{color[0]}     J       <      | | |O.-|.-' {results[7]}
{color[0]}   _J   .-    / O | |   |. ./    {results[8]}
{color[0]}  '-F  -<_.        .-'  `-'-L__  {results[9]}
{color[0]} __J  _   _.     >-'  )._.   |'  {results[10]}
{color[0]} `-|.'   /_.           _|   F    {results[11]}
{color[0]}   /.-   .                _.<    {results[12]}
{color[0]}  /'    /.'             .'  `
{color[0]}   /L  /'   |/      _.-'-
{color[0]}  /'J       ___.---'|
{color[0]}    |  .--' V  | `. `
{color[0]}    |/`. `-.     `._)
{color[0]}       / .-.
{color[0]}        (  `
{color[0]}        `.
\x1b[0m"""
, 'Linux':"""{color[0]}
{color[0]}              a8888b.            {results[0]}
{color[0]}             d888888b.           {results[1]}
{color[0]}             8P"YP"Y88           {results[2]}
{color[0]}             8|o||o|88           {results[3]}
{color[0]}             8'    .88           {results[4]}
{color[0]}             8`._.' Y8.          {results[5]}
{color[0]}            d/      `8b.         {results[6]}
{color[0]}          .dP   .     Y8b.       {results[7]}
{color[0]}         d8:'   "   `::88b.      {results[8]}
{color[0]}        d8"           `Y88b      {results[9]}
{color[0]}       :8P     '       :888      {results[10]}
{color[0]}        8a.    :      _a88P      {results[11]}
{color[0]}      ._/"Yaa_ :    .| 88P|      {results[12]}
{color[0]}      \    YP"      `| 8P  `.
{color[0]}      /     \._____.d|    .'
{color[0]}      `--..__)888888P`._.'
\x1b[0m"""

}



def autoSize(used,total):
	mem = ['B','KB','MB','GB','TB','PB']
	for x in range(1,6):
		if total > 1000:
			used = math.ceil(used/1024)
			total = math.ceil(total/1024)
			size = mem[x]
	return used,total,size

#---------------Classes---------------#

class Output(object):
	results = []

	def __init__(self):
		self.distro,self.pname = self.detectDistro()
		self.json = {}

# 	def fileCheck(self,f):
# 		"""
# 		1. Checks if a file exists, if so, reads it
# 		2. looks for distribution name in file
# 		3. returns name and if it was successful or not
# 		"""
# 		txt = ''
# 
# 		if os.path.isfile(f):
# 			txt = open(f).readlines()
# 
# 		else:
# 			return False,'Linux'
# 
# 		linux = ['Arch Linux','Fedora','LinuxMint','Ubuntu','SUSE','Debian','Raspbian','Slackware']
# 		dist = 'Linux'
# 		ans = False
# 		for line in txt:
# 			for i in linux:
# 				if line.find(i) >= 0:
# 					dist = i
# 					ans = True
# 					break
# 
# 		return ans,dist

	def detectDistro(self):
		"""
		Attempts to determine the distribution and draw the logo. However, if it can't, 
		then it defaults to 'Linux' and draws a simple linux penguin. 
		"""
		dist = _platform
		pname = ''
		
		if dist == 'darwin':
			dist = 'Mac OSX'
		elif dist == 'freebsd':
			dist = 'FreeBSD'
		else:
			dist,pname = self.readDistro()
			
# 			try:
# 				dist = Popen(['lsb_release', '-is'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
# 			except:
# 				#print 'Error w/ lsb_release'
# 				ans,dist = self.fileCheck('/etc/os-release')

		# Correct some distribution names
		if dist == 'Arch':
			dist =	'Arch Linux'
		elif dist == 'openSUSE project':
			dist = 'openSUSE'


		return dist, pname

	def readDistro(self,f='/etc/os-release'):
		"""
		1. Checks if a file exists, if so, reads it
		2. looks for distribution name in file
		3. returns name and if not successful, just says 'Linux' which is the default
		
		pi@calculon ~ $ more /etc/os-release
		PRETTY_NAME="Raspbian GNU/Linux 7 (wheezy)"
		NAME="Raspbian GNU/Linux"
		VERSION_ID="7"
		VERSION="7 (wheezy)"
		ID=raspbian
		ID_LIKE=debian
		ANSI_COLOR="1;31"
		HOME_URL="http://www.raspbian.org/"
		SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
		BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
		
		$ cat /etc/os-release 
		NAME="Arch Linux"
		ID=arch
		PRETTY_NAME="Arch Linux"
		ANSI_COLOR="0;36"
		HOME_URL="https://www.archlinux.org/"
		SUPPORT_URL="https://bbs.archlinux.org/"
		BUG_REPORT_URL="https://bugs.archlinux.org/"
		"""
		try:
			txt = open(f).readlines()
			pretty_name = ''
			name = ''

			for line in txt:
				if line.find('PRETTY_NAME') >=0: pretty_name = line.split('=')[1].replace('"','').replace('\n','').replace('GNU/Linux ','')
				if line.find('NAME') >= 0: name = line.split('=')[1].replace('"','').replace('\n','')
			
			if not name: name = 'Linux'
			
			return name,pretty_name
		
		except:
			name = Popen(['lsb_release', '-is'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
			if not name: name = 'Linux'
			return name,''	

	def getDistro(self):
		if self.pname: return self.pname
		else: return self.distro
		
	def append(self, display):
		self.results.append('%s%s: %s%s' % (colorDict[self.distro][1], display.key, colorDict['Clear'][0], display.value))
		self.json[display.key] = display.value

	def output(self, json=False):
		if json:
			return self.json
		else:
			print(logosDict[self.distro].format(color = colorDict[self.distro], results = self.results))


class User(object):
	def __init__(self):
		self.key = 'User'
		self.value = os.getenv('USER')

class Hostname(object):
	def __init__(self):
		#hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
		self.key = 'Hostname'
		self.value = platform.node()


class OS(object):
	def __init__(self,dist):
		OS = dist
		
		if dist == 'Mac OSX':
			v = platform.mac_ver() 
			OS = OS + ' ' + v[0] + ' ' + v[2]
		else: 
			OS = OS + ' ' + platform.machine()

		self.key = 'OS'
		self.value = OS
		
# 	def getDistro(self,f='/etc/os-release'):
# 		"""
# 		1. Checks if a file exists, if so, reads it
# 		2. looks for distribution name in file
# 		3. returns name and if it was successful or not
# 		
# 		pi@calculon ~ $ more /etc/os-release
# 		PRETTY_NAME="Raspbian GNU/Linux 7 (wheezy)"
# 		NAME="Raspbian GNU/Linux"
# 		VERSION_ID="7"
# 		VERSION="7 (wheezy)"
# 		ID=raspbian
# 		ID_LIKE=debian
# 		ANSI_COLOR="1;31"
# 		HOME_URL="http://www.raspbian.org/"
# 		SUPPORT_URL="http://www.raspbian.org/RaspbianForums"
# 		BUG_REPORT_URL="http://www.raspbian.org/RaspbianBugs"
# 		
# 		$ cat /etc/os-release 
# 		NAME="Arch Linux"
# 		ID=arch
# 		PRETTY_NAME="Arch Linux"
# 		ANSI_COLOR="0;36"
# 		HOME_URL="https://www.archlinux.org/"
# 		SUPPORT_URL="https://bbs.archlinux.org/"
# 		BUG_REPORT_URL="https://bugs.archlinux.org/"
# 		"""
# 		try:
# 			txt = open(f).readlines()
# 
# 			for line in txt:
# 				if line.find('PRETTY_NAME') >=0: return line.split('=')[1].replace('"','').replace('\n','').replace('GNU/Linux ','')
# 			return ''
# 		
# 		except:
# 			return ''	


class Kernel(object):
	def __init__(self):
		#kernel = Popen(['uname', '-r'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
		self.key = 'Kernel'
		#self.value = kernel
		self.value = platform.release()

class Uptime(object):
	def __init__(self):
		up = ps.boot_time()
		up = dt.datetime.fromtimestamp(up)
		now = dt.datetime.now()
		diff = now - up
		uptime = '%d days %d hrs %d mins' %(diff.days,diff.seconds/3600,(diff.seconds%3600)/60)
		self.key = 'Uptime'
		self.value = uptime

class Shell(object):
	def __init__(self):
		self.key = 'Shell'
		self.value = os.getenv('SHELL')

class Processes(object):
	def __init__(self):
		self.key = 'Processes'
		self.value =  str(len(ps.pids())) + ' running'

class Packages(object):
	def __init__(self,dist):
		try:
			if dist == 'Mac OSX':
				p1 = Popen(['brew', 'list', '-1'], stdout=PIPE).communicate()[0].decode("Utf-8")
			elif dist == 'FreeBSD':
				p1 = Popen(['pkg', 'info'], stdout=PIPE).communicate()[0].decode("Utf-8")
			elif dist == 'Arch Linux':
				p1 = Popen(['pacman', '-Q'], stdout=PIPE).communicate()[0].decode("Utf-8")
			elif dist == 'Fedora' or dist == 'openSUSE project':
				p1 = Popen(['rpm', '-qa'], stdout=PIPE).communicate()[0].decode("Utf-8")
			elif dist == 'Ubuntu' or dist == 'Debian' or dist == 'LinuxMint' or dist == 'Raspbian':
				p0 = Popen(['dpkg', '--get-selections'], stdout=PIPE)
				p1 = Popen(['grep', '-v', 'deinstall'], stdin=p0.stdout, stdout=PIPE).communicate()[0].decode("Utf-8")
			elif dist == 'Slackware':
				 p1 = Popen(['ls', '/var/log/packages/'], stdout=PIPE).communicate()[0].decode("Utf-8")
			packages = len(p1.rstrip('\n').split('\n'))
		except:
			packages = 0
		self.key = 'Packages'
		self.value = packages

class CPU(object):
	def __init__(self,dist):
		#file = open('/proc/cpuinfo').readlines()
		try:
			if dist == 'Mac OSX':
				cpu = Popen(['sysctl', '-n','machdep.cpu.brand_string'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')[0]
				c = cpu.replace('(R)','').replace('(TM)','').replace('CPU','').split()
				cpuinfo = ' '.join(c)
			elif dist == 'FreeBSD':
				cpu = Popen(['sysctl', '-n','hw'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
				cpuinfo = re.sub('	+', ' ', cpu[1].replace('model name\t: ', '').rstrip('\n'))
			else:
				cpu = Popen(['grep', '-i', 'model name\t: ', '/proc/cpuinfo'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
				cpuinfo = re.sub('	+', ' ', cpu[0].replace('model name\t: ', ''))
		except:
			cpuinfo = 'unknown'
		self.key = 'CPU'
		self.value = cpuinfo

class RAM(object):
	def __init__(self):
		ram = ps.virtual_memory()
		used = ram.used
		total = ram.total

		used,total,size = autoSize(used,total)
		ramdisplay = '%s %s/ %s %s' % (used, size, total,size)

		self.key = 'RAM'
		self.value = ramdisplay

class Disk(object):
	def __init__(self,json=False):
		p = ps.disk_usage('/')
		total = p.total
		used = p.used

		used,total,size = autoSize(used,total)

		usedpercent = int(float(used)/float(total)*100.0)

		if json:
			disk = '%s / %s %s' % (used, total, size)
		else:
			if usedpercent <= 33:
				disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][1], used, colorDict['Clear'][0], total, size)
			if usedpercent > 33 and usedpercent < 67:
				disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][2], used, colorDict['Clear'][0], total, size)
			if usedpercent >= 67:
				disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][0], used, colorDict['Clear'][0], total, size)
		self.key = 'Disk'
		self.value = disk

class IP(object):
	def __init__(self, zeroconfig=False):
		"""
		This tries to get the host name and deterine the IP address from it.
		It also tries to handle zeroconfig well. Also, there is an issue with getting
		the MAC address, so this uses uuid to get that too. However, using the UUID is 
		not reliable, because it can return any MAC address (bluetooth, wired, wireless,
		etc) or even make a random one.
		"""
		ip = '127.0.0.1'
		mac = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
		try:
			host = socket.gethostname()
			if zeroconfig:
				if host.find('.local') < 0:
					host=host + '.local'

			ip = socket.gethostbyname(host)
		except:
			print('Error in IP()')
		
		self.key = 'IP'
		self.value = ip + ' / ' + mac.upper()

class CPU2(object):
	def __init__(self):
		cpu = ps.cpu_percent(interval=1, percpu=True)
		self.key = 'CPU Usage'
		self.value = str(cpu)

def handleArgs():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
	description="""
Displays system info and a logo for OS

Currently, it displays:
	Username
	Hostname
	IP Address / MAC address
	OS Name
	Kernel Version
	Uptime: days hrs mins
	Shell
	Processess Running
	Packages Installed
	CPU
	CPU Usage
	RAM
	Disk Usage""", epilog="""Package info at: https://pypi.python.org/pypi/pyarchey
Submit issues to: https://github.com/walchko/pyarchey""")

	#parser.add_argument('-a', '--art', help='not implemented yet')
	parser.add_argument('-d', '--display', help='displays all ascii logos and exits', action='store_true')
	parser.add_argument('-j', '--json', help='instead of printing to screen, returns system as json', action='store_true')
# 	parser.add_argument('-v', '--version', help='prints version number', action='store_true')
	parser.add_argument('-z', '--zeroconfig', help='assume a zeroconfig network and adds .local to the hostname', action='store_true')

	args = vars(parser.parse_args())

	return args

def main():
	args = handleArgs()

	if args['display']:
		for i in logosDict:
			print(i)
			print(logosDict[i].format(color = colorDict[i],results=list(xrange(0,13))) )
		return 0

    # Need a good way to display version number, there seems to be no standard
# 	if args['version']:
# 		print('pyarchey 0.6.3')
# 		return 0

	out = Output()
	out.append( User() )
	out.append( Hostname() )
	out.append( IP(args['zeroconfig']) )
	out.append( OS( out.getDistro() ) )
	out.append( Kernel() )
	out.append( Uptime() )
	out.append( Shell() )
	out.append( Processes() )
	out.append( Packages(out.distro) )
	out.append( CPU(out.distro) )
	out.append( CPU2() )
	out.append( RAM() )
	out.append( Disk(args['json']) )

	jsn = out.output(args['json'])


	if args['json']:
		return json.dumps(jsn)



if __name__ == '__main__':
	main()
