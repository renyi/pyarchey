#!/usr/bin/env python
#
#
# pyarchey is a simple system information tool written in Python.
#
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
# Changes:
# ---------------------
# 29 Mar 15 0.4.0 Forked
#  4 Apr 15 0.5.0 Added Apple logo, changed custom code to psutil
#


# For more info on psutil, see https://pythonhosted.org/psutil/
#

# Import libraries
import os, sys, subprocess              #
import re                               #
from subprocess import Popen, PIPE      # call commandline programs
from sys import platform as _platform   # distribution
import socket                           # ip address
import psutil as ps                     # system info
import datetime as dt                   # uptime

#---------------Output---------------#

output = [ 'User', 'Hostname', 'IP','OS', 'Kernel', 'Uptime', 'Shell', 'Processes', 'Packages', 'CPU', 'CPU Usage', 'RAM', 'Disk' ]

#---------------Dictionaries---------------#
#  https://wiki.archlinux.org/index.php/Color_Bash_Prompt
# escape[ x;y   x-{0 normal 1 bold} y-color
CLR="\033[0;0m"   # normal color scheme
BK ="\033[0;30m"   # black
BL ="\033[0;34m"   # blue
GR ="\033[0;32m"   # green
CY ="\033[0;36m"   # cyan
RD ='\033[0;31m'   # red
PL ="\033[0;35m"   # purple
BR ="\033[0;33m"   # brown
GY ="\033[0;30m"   # grey
LG ="\033[0;37m"   # light grey

# Bold colors (note be 'B' before the color name)
BBK ="\033[1;30m"   # black
BBL ="\033[1;34m"   # blue
BGR ="\033[1;32m"   # green
BCY ="\033[1;36m"   # cyan
BRD ='\033[1;31m'   # red
BPL ="\033[1;35m"   # purple
BBR ="\033[1;33m"   # brown
BGY ="\033[1;30m"   # grey
BLG ="\033[1;37m"   # light grey

colorDict = {
    'Arch Linux':       [BL, BBL],
    'Ubuntu':           [RD, BRD, BBR],
    'FreeBSD':          [RD, BRD, BR],
    'Mac OSX':          [CLR, CY],
    'Debian':           [RD, BRD],
    'Raspbian':         [RD, BRD],
    'LinuxMint':        [BLG, BGR],
    'CrunchBang':       [BLG,BLG],
    'Fedora':           [BLG, BBL, BL],
    'openSUSE project': [BLG, BGR],
    'Sensors':          [BRD, BGR, BBR],
    'Clear':            [CLR]
    }

logosDict = {'Arch Linux': '''{color[1]}
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
\x1b[0m'''
,'FreeBSD':'''{color[0]}
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
\x1b[0m'''
,'Debian':'''{color[0]}
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
\x1b[0m'''
,'Raspbian':'''{color[0]}
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
\x1b[0m'''
,'Ubuntu':'''{color[0]}
{color[0]}                          .oyhhs:   {results[0]}
{color[1]}                 ..--.., {color[0]}shhhhhh-   {results[1]}
{color[1]}               -+++++++++`:{color[0]}yyhhyo`  {results[2]}
{color[2]}          .--  {color[1]}-++++++++/-.-{color[0]}::-`    {results[3]}
{color[2]}        .::::-   {color[1]}:-----:/+++/++/.   {results[4]}
{color[2]}       -:::::-.          {color[1]}.:++++++:  {results[5]}
{color[1]}  ,,, {color[2]}.:::::-`             {color[1]}.++++++- {results[6]}
{color[1]}./+++/-{color[2]}`-::-                {color[1]}./////: {results[7]}
{color[1]}+++++++ {color[2]}.::-                        {results[8]}
{color[1]}./+++/-`{color[2]}-::-                {color[0]}:yyyyyo {results[9]}
{color[1]}  ``` `{color[2]}-::::-`             {color[0]}:yhhhhh: {results[10]}
{color[2]}       -:::::-.         {color[0]}`-ohhhhhh+  {results[11]}
{color[2]}        .::::-` {color[0]}-o+///+oyhhyyyhy:   {results[12]}
{color[2]}         `.--  {color[0]}/yhhhhhhhy+{color[2]},....
{color[0]}               /hhhhhhhhh{color[2]}-.-:::;
{color[0]}               `.:://::- {color[2]}-:::::;
{color[2]}                         `.-:-'
{color[2]}
\x1b[0m'''
,'LinuxMint':'''{color[0]}
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
\x1b[0m'''
,'Fedora':'''{color[0]}
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
\x1b[0m'''
,'openSUSE project':'''{color[0]}
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
\x1b[0m'''
, 'Mac OSX':'''
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
\x1b[0m'''
}







def fileCheck(f):
    """
    1. Checks if a file exists, if so, reads it
    2. looks for distribution name in file
    3. returns name and if it was successful or not
    """
    txt = ''

    if os.path.isfile(f):
        txt = open(f).readlines()

    else:
        return False,'linux'

    linux = ['Arch','Fedora','LinuxMint','Ubuntu','SUSE','Debian','Raspbian']
    dist = 'Linux'
    ans = False
    for line in txt:
        for i in linux:
            if line.find(i) >= 0:
                dist = i
                ans = True
                break

    return ans,dist

dist = _platform
if dist == 'darwin':
    dist = 'Mac OSX'
elif dist == 'freebsd':
    dist = 'FreeBSD'
else:
    try:
    	dist = Popen(['lsb_release', '-is'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
    except:
    	#print 'Error w/ lsb_release'
    	ans,dist = fileCheck('/etc/os-release')
        if not ans: dist = 'Debian'

def autoSize(used,total):
    mem = ['B','KB','MB','GB','TB','PB']
    for x in range(1,5):
        if (total / (1024 ** x)) < 1000:
            used = used / (1024 ** x)
            total = total / (1024 ** x)
            size = mem[x]
            break
    return used,total,size

#---------------Classes---------------#

class Output:
    results = []
    #results.extend(['']*(18-len(output)))

    def __init__(self):
        #self.distro = self.__detectDistro()
        self.distro = dist + ' Linux' if dist == 'Arch' else dist

#    def __detectDistro(self):
#        if dist == 'Arch':
#            return 'Arch Linux'
#        elif dist == 'FreeBSD':
#            return 'FreeBSD'
#        else:
#            sys.exit(1)

    def append(self, display):
        self.results.append('%s%s: %s%s' % (colorDict[self.distro][1], display.key, colorDict['Clear'][0], display.value))

    def output(self):
        print(logosDict[self.distro].format(color = colorDict[self.distro], results = self.results))

class User:
    def __init__(self):
        self.key = 'User'
        self.value = os.getenv('USER')

class Hostname:
    def __init__(self):
        hostname = Popen(['uname', '-n'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        self.key = 'Hostname'
        self.value = hostname

class OS:
    def __init__(self):
        if dist == 'Mac OSX':
            OS = dist
        elif dist == 'FreeBSD':
            OS = 'FreeBSD'
        elif dist == 'Arch':
            OS =  'Arch Linux'
        elif dist == 'openSUSE project':
            OS = 'openSUSE'
        else:
            OS = dist

        arch = Popen(['uname', '-m'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        OS = OS + ' ' + arch

        self.key = 'OS'
        self.value = OS


class Kernel:
    def __init__(self):
        kernel = Popen(['uname', '-r'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        self.key = 'Kernel'
        self.value = kernel

class Uptime:
    def __init__(self):
        # if dist == 'Mac OSX':
        #     fuptime = Popen(['uptime'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        #     fuptime = 10000 # FIXME
        # elif dist == 'FreeBSD':
        #     boottime = Popen(['sysctl', '-n',  'kern.boottime'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n').split()[3]
        #     currtime = Popen(['date', '+%s'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
        #     fuptime =int(currtime) - int(re.sub(',', '', boottime))
        # else:
        #     fuptime = int(open('/proc/uptime').read().split('.')[0])
        # day = int(fuptime / 86400)
        # fuptime = fuptime % 86400
        # hour = int(fuptime / 3600)
        # fuptime = fuptime % 3600
        # minute = int(fuptime / 60)
        # uptime = ''
        # if day == 1:
        #     uptime += '%d day, ' % day
        # if day > 1:
        #     uptime += '%d days, ' % day
        # uptime += '%d:%02d' % (hour, minute)

        up = ps.boot_time()
        up = dt.datetime.fromtimestamp(up)
        now = dt.datetime.now()
        diff = now - up
        uptime = '%d days %d hrs %d mins' %(diff.days,diff.seconds/3600,(diff.seconds%3600)/60)
        self.key = 'Uptime'
        self.value = uptime

class Shell:
    def __init__(self):
        self.key = 'Shell'
        self.value = os.getenv('SHELL')

class Processes:
    def __init__(self):
        self.key = 'Processes'
        # self.tmux = ' (tmux)' if os.getenv('TMUX') else ''
        # self.value = os.getenv('TERM') + self.tmux
        self.value =  str(len(ps.pids())) + ' running'

class Packages:
    def __init__(self):
        if dist == 'Mac OSX':
            p1 = Popen(['brew', 'list', '-1'], stdout=PIPE).communicate()[0].decode("Utf-8")
        elif dist == 'FreeBSD':
            p1 = Popen(['pkg', 'info'], stdout=PIPE).communicate()[0].decode("Utf-8")
        elif dist == 'Arch':
            p1 = Popen(['pacman', '-Q'], stdout=PIPE).communicate()[0].decode("Utf-8")
        elif dist == 'Fedora' or dist == 'openSUSE project':
            p1 = Popen(['rpm', '-qa'], stdout=PIPE).communicate()[0].decode("Utf-8")
        elif dist == 'Ubuntu' or dist == 'Debian' or dist == 'LinuxMint' or dist == 'Raspbian':
            p0 = Popen(['dpkg', '--get-selections'], stdout=PIPE)
            p1 = Popen(['grep', '-v', 'deinstall'], stdin=p0.stdout, stdout=PIPE).communicate()[0].decode("Utf-8")
        packages = len(p1.rstrip('\n').split('\n'))
        self.key = 'Packages'
        self.value = packages

class CPU:
    def __init__(self):
        #file = open('/proc/cpuinfo').readlines()
        if dist == 'Mac OSX':
            cpu = Popen(['sysctl', '-n','machdep.cpu.brand_string'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')[0]
            c = cpu.replace('(R)','').replace('(TM)','').replace('CPU','').split()
            cpuinfo = ' '.join(c)
        elif dist == 'FreeBSD':
            file = Popen(['sysctl', '-n','hw'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
            cpuinfo = re.sub('  +', ' ', file[1].replace('model name\t: ', '').rstrip('\n'))
        else:
            file = Popen(['grep', '-i', 'model name\t: ', '/proc/cpuinfo'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
            cpuinfo = re.sub('  +', ' ', file[0].replace('model name\t: ', ''))
        self.key = 'CPU'
        self.value = cpuinfo

class RAM:
    def __init__(self):
        # if dist == 'Mac OSX': # FIXME
        #     raminfo = Popen(['sysctl','-n','hw.memsize'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')[0]
        #     ram = int(raminfo)/(1024**3)
        #     used = ram
        #     total = ram
        # elif dist == 'FreeBSD':
        #     raminfo = Popen(['vmstat'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
        #     ram = raminfo[2].split()
        #     used = int(ram[3])//1000
        #     total = int(ram[4])//1000
        # else:
        #     raminfo = Popen(['free', '-m'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
        #     ram = ''.join(filter(re.compile('M').search, raminfo)).split()
        #     used = ram[2]
        #     total = ram[1]

        ram = ps.virtual_memory()
        used = ram.used
        total = ram.total

        used,total,size = autoSize(used,total)
        ramdisplay = '%s %s/ %s %s' % (used, size, total,size)
        #
        # usedpercent = ((float(used) / float(total)) * 100)
        # if usedpercent <= 33:
        #     ramdisplay = '%s%s MB %s/ %s %s' % (colorDict['Sensors'][1], used, colorDict['Clear'][0], total,size)
        # if usedpercent > 33 and usedpercent < 67:
        #     ramdisplay = '%s%s MB %s/ %s %s' % (colorDict['Sensors'][2], used, colorDict['Clear'][0], total,size)
        # if usedpercent >= 67:
        #     ramdisplay = '%s%s MB %s/ %s %s' % (colorDict['Sensors'][0], used, colorDict['Clear'][0], total,size)
        self.key = 'RAM'
        self.value = ramdisplay

class Disk:
    def __init__(self):
        # if dist == 'Mac OSX':
        #     p1 = Popen(['df', '-lhg'], stdout=PIPE).communicate()[0].decode("Utf-8")
        #     total = p1.splitlines()[-1]
        #     used = total.split()[2]
        #     size = total.split()[1]
        #     usedpercent = float(total.split()[4][:-1])
        # elif dist == 'FreeBSD':
        #     p1 = Popen(['df', '-Tlhc'], stdout=PIPE).communicate()[0].decode("Utf-8")
        #     total = p1.splitlines()[-1]
        #     used = total.split()[2]
        #     size = total.split()[1]
        #     usedpercent = float(total.split()[4][:-1])
        # else:
        #     p1 = Popen(['df', '-Tlh', '--total', '-t', 'ext4', '-t', 'ext3', '-t', 'ext2', '-t', 'reiserfs', '-t', 'jfs', '-t', 'ntfs', '-t', 'fat32', '-t', 'btrfs', '-t', 'fuseblk', '-t', 'xfs'], stdout=PIPE).communicate()[0].decode("Utf-8")
        #     total = p1.splitlines()[-1]
        #     used = total.split()[3]
        #     size = total.split()[2]
        #     usedpercent = float(total.split()[5][:-1])

        p = ps.disk_usage('/')
        total = p.total
        used = p.used

        used,total,size = autoSize(used,total)

        usedpercent = int(float(used)/float(total)*100.0)

        if usedpercent <= 33:
            disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][1], used, colorDict['Clear'][0], total, size)
        if usedpercent > 33 and usedpercent < 67:
            disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][2], used, colorDict['Clear'][0], total, size)
        if usedpercent >= 67:
            disk = '%s%s %s/ %s %s' % (colorDict['Sensors'][0], used, colorDict['Clear'][0], total, size)
        self.key = 'Disk'
        self.value = disk

class IP:
    def __init__(self):
        ip = socket.gethostbyname(socket.gethostname())

        # try a zeroconfig host name
        if ip.find('127.0') >=0:
            ip = socket.gethostbyname(socket.gethostname()+'.local')
        self.key = 'IP'
        self.value = ip

class CPU2:
    def __init__(self):
        cpu = ps.cpu_percent(interval=1, percpu=True)
        self.key = 'CPU Usage'
        self.value = str(cpu)

def main():

    classes = {
         'User': User,
         'OS': OS,
         'Hostname': Hostname,
         'IP': IP,
         'Kernel': Kernel,
         'Uptime': Uptime,
         'Shell': Shell,
         'Processes': Processes,
         'Packages': Packages,
         'CPU': CPU,
         'RAM': RAM,
         'CPU Usage': CPU2,
         'Disk': Disk
    }


    out = Output()
    for x in output:
        out.append(classes[x]())
    out.output()


if __name__ == '__main__':
    main()
