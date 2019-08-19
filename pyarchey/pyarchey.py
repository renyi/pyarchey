#!/usr/bin/env python
#
#
# pyarchey is a simple system information tool written in Python.
#
# Copyright 2019 Renyi Khor <renyi.ace@gmail.com>
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
from __future__ import print_function   # make things nicer for python 3
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
import platform                         # get system info - not used yet
import typing

import threading
import logging

from queue import Queue

logger = logging.getLogger('pyarchey2')


# ---------------Dictionaries---------------#
#  https://wiki.archlinux.org/index.php/Color_Bash_Prompt
# escape[ x;y   x-{0 normal 1 bold} y-color
CLR = "\033[0;0m"   # normal color scheme
BK = "\033[0;30m"   # black
BL = "\033[0;34m"   # blue
GR = "\033[0;32m"   # green
CY = "\033[0;36m"   # cyan
RD = "\033[0;31m"   # red
PL = "\033[0;35m"   # purple
YW = "\033[0;33m"   # yellow
GY = "\033[0;30m"   # grey
LG = "\033[0;37m"   # light grey

# Bold colors (note be 'B' before the color name)
BBK = "\033[1;30m"   # black
BBL = "\033[1;34m"   # blue
BGR = "\033[1;32m"   # green
BCY = "\033[1;36m"   # cyan
BRD = "\033[1;31m"   # red
BPL = "\033[1;35m"   # purple
BYW = "\033[1;33m"   # yellow
BGY = "\033[1;30m"   # grey
BLG = "\033[1;37m"   # light grey

colorDict = {
    'Arch Linux':       [BL, BBL],       # noqa
    'Ubuntu':           [RD, BRD, BYW],  # noqa
    'FreeBSD':          [RD, BRD, YW],   # noqa
    'Mac OSX':          [CLR, CY],       # noqa
    'Debian':           [RD, BRD],       # noqa
    'Raspbian':         [RD, BRD, GR],   # noqa
    'LinuxMint':        [BLG, BGR],      # noqa 
    'Gentoo':           [BPL, BLG],      # noqa
    'OpenBSD':          [BYW, BYW, YW],  # noqa
    'Fedora':           [BLG, BBL, BL],  # noqa
    'openSUSE project': [BLG, BGR],      # noqa
    'Slackware':        [BLG, BL, BBL],  # noqa
    'Linux':            [CLR, BBL],      # noqa
    'Sensors':          [BRD, BGR, BYW], # noqa
    'Clear':            [CLR]            # noqa
}

logosDict = {
    'Arch Linux': """{color[1]}
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
    \x1b[0m""",

    'FreeBSD': """{color[0]}
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
    \x1b[0m""",

    'Debian': """{color[0]}
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
    \x1b[0m""",

    'Raspbian': """{color[0]}
    {color[2]}        .~~.   .~~.      {results[0]}
    {color[2]}       '. \ ' ' / .'     {results[1]}
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
    \x1b[0m""",

    'Ubuntu': """{color[0]}
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
    \x1b[0m""",

    'LinuxMint': """{color[0]}
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
    \x1b[0m""",

    'Fedora':"""{color[0]}
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
    \x1b[0m""",

    'openSUSE project':"""{color[0]}
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
    \x1b[0m""",

    'Slackware': """{color[0]}
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
    \x1b[0m""",

    'Mac OSX': """{color[0]}
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
    \x1b[0m""",

    'Gentoo': """{color[0]}
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
    \x1b[0m""",

    'OpenBSD': """{color[0]}
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
    \x1b[0m""",

    'Linux': """{color[0]}
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


def format_bytes(size: float) -> str:
    power = 2**10  # 2**10 = 1024
    n = 0
    power_labels = {0: '', 1: 'K', 2: 'M', 3: 'G', 4: 'T', 5: 'P', 6: 'E', 7: 'Z', 8: 'Y'}
    while size > power:
        size /= power
        n += 1
    return f'{size:.2f} {power_labels[n]}B'


def autoSize(used: float, total: float) -> list:
    return format_bytes(used), format_bytes(total)


# ---------------Classes---------------#


class Output():
    results: typing.List[typing.List] = []
    json: dict = {}
    distro: str = None
    pname: str = None

    args: dict = None
    queue: Queue = None
    threads: typing.List[threading.Thread] = []

    def __init__(self, args, **kwargs):
        self.args = args

        self.getDistro()

    # def __getattr__(self, name):
    #     for f in self.features:
    #         if f'get_{f}' == name:
    #             c = getattr(self, f)
    #             print(c)
    #             t = threading.Thread(target=c)
    #             self.threads.append(t)
    #             return t

    def detectDistro(self) -> str:
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
            dist, pname = self.readDistro()

        # Correct some distribution names
        if dist == 'Arch':
            dist = 'Arch Linux'
        elif dist == 'openSUSE project':
            dist = 'openSUSE'
        return dist, pname

    def readDistro(self, f: str = '/etc/os-release') -> list:
        """
        See: http://www.dsm.fordham.edu/cgi-bin/man-cgi.pl?topic=os-release&ampsect=5

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
            with open(f, 'r') as f:
                txt = f.readlines()

            pretty_name = ''
            name = ''

            for line in txt:
                if line.startswith('PRETTY_NAME'):
                    pretty_name = line.split('=')[1].replace('"', '').replace('\n', '').replace('GNU/Linux ', '')

                if line.startswith('NAME'):
                    name = line.split('=')[1].replace('"', '').replace('\n', '').replace(' GNU/Linux', '')

            if not name:
                name = 'Linux'

            return name, pretty_name

        except Exception as e:
            logger.error(e)
            name = Popen(['lsb_release', '-is'], stdout=PIPE).communicate()[0].decode('Utf-8').rstrip('\n')
            if not name:
                name = 'Linux'
            return name, ''

    def getDistro(self) -> str:
        """
        Ideally returns the pretty distro name instead of the short distro name. If we
        weren't able to figure out the distro, it defaults to Linux.
        """
        if not self.pname and not self.distro:
            self.distro, self.pname = self.detectDistro()
        return self.pname if self.pname else self.distro

    def append(self, display: str):
        """
        Sets up the printing
        """
        self.results.append(f'{colorDict[self.distro][1]}{display[0]}: {colorDict["Clear"][0]}{display[1]}')

    def getall(self):
        if not self.queue:
            self.queue = Queue()

        self.threads.append(threading.Thread(target=self.user))
        self.threads.append(threading.Thread(target=self.hostname))
        self.threads.append(threading.Thread(target=self.ip, args=[self.args.get('zeroconfig', False)]))
        self.threads.append(threading.Thread(target=self.os, args=[self.distro]))
        self.threads.append(threading.Thread(target=self.kernel))
        self.threads.append(threading.Thread(target=self.uptime))
        self.threads.append(threading.Thread(target=self.shell))
        self.threads.append(threading.Thread(target=self.processes))
        self.threads.append(threading.Thread(target=self.packages, args=[self.distro]))
        self.threads.append(threading.Thread(target=self.cpu, args=[self.distro]))
        self.threads.append(threading.Thread(target=self.cpu2))
        self.threads.append(threading.Thread(target=self.ram))
        self.threads.append(threading.Thread(target=self.disk, args=[self.args.get('json', False)]))

        logger.debug('Starting threads ...')
        for t in self.threads:
            t.start()

        logger.debug('Joining threads ...')
        for t in self.threads:
            t.join()

        logger.debug('Getting results from queue...')
        for t in self.threads:
            res = self.queue.get(False)
            logger.debug(res)

            # Append list
            self.append(res)

            # Append json
            self.json[res[0]] = res[1]

            # Finish q
            self.queue.task_done()

        logger.debug('Joining queue ...')
        self.queue.join()

    def output(self, js: bool = False, dumps: typing.Callable = None, raw: bool = False) -> typing.Union[dict, str]:
        """
        Does the printing. Either picture and info to screen or dumps json.
        """
        if not self.results or not self.json:
            self.getall()

        if self.json:
            if raw is True:
                return self.json  # json dict

            if js is True or self.args.get('json', False) is True:
                if dumps is None:
                    dumps = json.dumps
                return json.dumps(self.json)  # json string

        # Full UI
        return logosDict[self.distro].format(color=colorDict[self.distro], results=self.results)  # graphics dict

    def user(self) -> str:
        logger.debug('Getting user ..')
        try:
            user = os.getenv('USER')
            msg = 'User', f'{user}'
        except Exception as e:
            logger.error(f'user: {e}')
            msg = 'User', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done user.')
        return msg

    def hostname(self) -> str:
        logger.debug('Getting hostname ..')
        try:
            msg = 'Hostname', f'{platform.node()}'
        except Exception as e:
            logger.error(f'hostname: {e}')
            msg = 'Hostname', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done hostname.')
        return msg

    def os(self, dist: str) -> str:
        logger.debug('Getting os ..')
        try:
            OS = dist

            if dist == 'Mac OSX':
                v = platform.mac_ver()
                OS = f'{OS} {v[0]} {v[2]}'

            else:
                OS = f'{OS} {platform.machine()}'

            msg = 'OS', f'{OS}'
        except Exception as e:
            logger.error(f'os: {e}')
            msg = 'OS', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done os.')
        return msg

    def kernel(self) -> str:
        logger.debug('Getting kernel ..')
        try:
            msg = 'Kernel', f'{platform.release()}'
        except Exception as e:
            logger.error(f'kernel: {e}')
            msg = 'Kernel', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done kernel.')
        return msg

    def uptime(self) -> str:
        logger.debug('Getting uptime ..')
        try:
            up = ps.boot_time()
            up = dt.datetime.fromtimestamp(up)
            now = dt.datetime.now()
            diff = now - up

            uptime = f'{diff.days:.0f} days {diff.seconds / 3600:.0f} hrs {(diff.seconds % 3600) / 60:.0f} mins'
            msg = 'Uptime', f'{uptime}'
        except Exception as e:
            logger.error(f'uptime: {e}')
            msg = 'Uptime', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done uptime.')
        return msg

    def shell(self) -> str:
        logger.debug('Getting shell ..')
        try:
            shell = os.getenv('SHELL')
            msg = 'Shell', f'{shell}'
        except Exception as e:
            logger.error(f'shell: {e}')
            msg = 'Shell', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done shell.')
        return msg

    def processes(self) -> str:
        logger.debug('Getting processes ..')
        try:
            msg = 'Processes', f'{str(len(ps.pids()))} running'
        except Exception as e:
            logger.error(f'processes: {e}')
            msg = 'Processes', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done processes.')
        return msg

    def packages(self, dist: str) -> str:
        logger.debug('Getting packages ..')
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

            msg = 'Packages', f'{packages}'
        except Exception as e:
            logger.error(f'packages: {e}')
            msg = 'Packages', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done packages.')
        return msg

    def cpu(self, dist: str) -> str:
        logger.debug('Getting cpu ..')
        cpuinfo = 'unknown'
        try:
            if dist == 'Mac OSX':
                cpu = Popen(['sysctl', '-n', 'machdep.cpu.brand_string'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')[0]
                c = cpu.replace('(R)', '').replace('(TM)', '').replace('CPU', '').split()
                cpuinfo = ' '.join(c)
            elif dist == 'FreeBSD':
                cpu = Popen(['sysctl', '-n', 'hw'], stdout=PIPE).communicate()[0].decode('Utf-8').split('\n')
                cpuinfo = re.sub('  +', ' ', cpu[1].replace('model name\t: ', '').rstrip('\n'))
            else:
                with open('/proc/cpuinfo', 'r') as f:
                    txt = f.readlines()

                for line in txt:
                    if line.find('model name') >= 0:
                        cpuinfo = line.split(': ')[1].strip('\n')

            msg = 'CPU', f'{cpuinfo}'
        except Exception as e:
            logger.error(f'cpu: {e}')
            msg = 'CPU', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done cpu.')
        return msg

    def ram(self) -> str:
        logger.debug('Getting ram ..')
        try:
            ram = ps.virtual_memory()
            used = ram.used
            total = ram.total

            used, total = autoSize(used, total)

            msg = 'RAM', f'{used} / {total}'
        except Exception as e:
            logger.error(f'ram: {e}')
            msg = 'RAM', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done ram.')
        return msg

    def disk(self, json: bool = False) -> str:
        logger.debug('Getting disk ..')
        try:
            p = ps.disk_usage('/')
            total = p.total
            used = p.used

            used, total = autoSize(used, total)

            usedpercent = int(float(p.used) / float(p.total) * 100.0)

            if json is True:
                disk = f'{used} / {total}'

            else:
                if usedpercent <= 33:
                    label1 = colorDict.get('Sensors')[1]
                    label2 = colorDict.get('Clear')[0]
                    disk = f'{label1}{used} {label2}/ {total}'
                elif usedpercent > 33 and usedpercent < 67:
                    label1 = colorDict.get('Sensors')[2]
                    label2 = colorDict.get('Clear')[0]
                    disk = f'{label1}{used} {label2}/ {total}'
                elif usedpercent >= 67:
                    label1 = colorDict.get('Sensors')[0]
                    label2 = colorDict.get('Clear')[0]
                    disk = f'{label1}{used} {label2}/ {total}'

            msg = 'Disk', f'{disk}'
        except Exception as e:
            logger.error(f'disk: {e}')
            msg = 'Disk', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done disk.')
        return msg

    def ip(self, zeroconfig: bool = False) -> str:
        """
        This tries to get the host name and deterine the IP address from it.
        It also tries to handle zeroconfig well. Also, there is an issue with getting
        the MAC address, so this uses uuid to get that too. However, using the UUID is
        not reliable, because it can return any MAC address (bluetooth, wired, wireless,
        etc) or even make a random one.
        """
        logger.debug('Getting ip ..')
        ip = '127.0.0.1'
        mac = ':'.join(re.findall('..', '%012x' % uuid.getnode())).upper()
        try:
            if not self.distro == 'Mac OSX':  # Temp fix for [Errno 8] nodename nor servname provided, or not known
                host = socket.gethostname()
                # host = socket.getfqdn()
                # ni_list = psutil.net_if_addrs()
                if zeroconfig is True:
                    if host.find('.local') < 0:
                        host = host + '.local'

                ip = socket.gethostbyname(host)
        except Exception as e:
            logger.error(f'ip: {e}')

        msg = 'IP', f'{ip} / {mac}'

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done ip.')
        return msg

    def cpu2(self) -> str:
        logger.debug('Getting cpu2 ..')
        try:
            cpu = ps.cpu_percent(interval=1, percpu=True)
            msg = 'CPU Usage', f'{cpu}'
        except Exception as e:
            logger.error(f'cpu2: {e}')
            msg = 'CPU Usage', ''

        if self.queue is not None:
            self.queue.put(msg, False)

        logger.debug('Done cpu2.')
        return msg


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
                                            Disk Usage""",
                                     epilog="Package info at: https://pypi.python.org/pypi/pyarchey2. Submit issues to: https://github.com/renyi/pyarchey2")

    # parser.add_argument('-a', '--art', help='not implemented yet')
    parser.add_argument('-d', '--display', help='displays all ascii logos and exits', action='store_true')
    parser.add_argument('-j', '--json', help='instead of printing to screen, returns system as json', action='store_true')
    # parser.add_argument('-v', '--version', help='prints version number', action='store_true')
    parser.add_argument('-z', '--zeroconfig', help='assume a zeroconfig network and adds .local to the hostname', action='store_true')
    parser.add_argument('--verbose', help='enables more verbose messages', action='store_true')
    parser.add_argument('--debug', help='print debug messages', action='store_true')
    # parser.add_argument('--version', action='version', version='%(prog)s 1.0')

    args = vars(parser.parse_args())

    return args


def main():
    args = handleArgs()

    if args['display'] is True:
        for i in logosDict:
            print(i)
            print(logosDict[i].format(color=colorDict[i], results=list(range(0, 13))))
        return 0

    if args['debug'] is True:
        logging.basicConfig(level=logging.DEBUG)

    elif args['verbose'] is True:
        logging.basicConfig(level=logging.INFO)

    out = Output(args=args)
    return out.output()


if __name__ == '__main__':
    print(main())
