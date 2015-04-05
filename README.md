# PyArchey

[![Build Status](https://travis-ci.org/walchko/pyarchey.svg)](https://travis-ci.org/walchko/pyarchey)
[![Latest Version](https://pypip.in/version/pyarchey/badge.svg)](https://pypi.python.org/pypi/pyarchey/)
[![Downloads](https://pypip.in/download/pyarchey/badge.svg)](https://pypi.python.org/pypi/pyarchey/)
[![License](https://pypip.in/license/pyarchey/badge.svg)](https://pypi.python.org/pypi/pyarchey/)

This is based off the `archey` command (which is also python) distributed by various linux, unix, and osx package managers. In order to avoid a naming conflict between them, I called this `pyarchey`.


    [kevin@Tardis ~]$ pyarchey

                    ##             User: kevin
                 ####              Hostname: Dalek.local
                 ##                IP: 192.168.1.13
         #######    #######        OS: Mac OSX x86_64
       ######################      Kernel: 14.1.0
      #####################        Uptime: 6 days 5 hrs 32 mins
      ####################         Shell: /bin/bash
      ####################         Processes: 367 running
      #####################        Packages: 74
       ######################      CPU: Intel Core i5-2400S @ 2.50GHz
        ####################       CPU Usage: [5.9, 3.0, 4.0, 2.0]
          ################         RAM: 11 GB/ 12 GB
            ###     ####           Disk: 441 / 464 GB



    pi@calculon ~ $ pyarchey

            .~~.   .~~.      User: pi
           '. \ ' ' / .'     Hostname: calculon
            .~ .~~~..~.      IP: 192.168.1.17
           : .~.'~'.~. :     OS: Raspbian armv6l
          ~ (   ) (   ) ~    Kernel: 3.18.8+
         ( : '~'.~.'~' : )   Uptime: 34 days 4 hrs 38 mins
          ~ .~ (   ) ~. ~    Shell: /bin/bash
           (  : '~' :  )     Processes: 77 running
            '~ .~~~. ~'      Packages: 1061
                '~'          CPU: ARMv6-compatible processor rev 7 (v6l)
                             CPU Usage: [2.0]
                             RAM: 213 MB/ 229 MB
                             Disk: 4 / 14 GB


## Requirements

Some of the custom code was removed and `psutil` was used to provide a cross-platform solution.

## Install

The preferred way is to use [pypi.org](https://pypi.python.org/pypi)

    pip install pyarchey

You can also do

    git clone https://github.com/walchko/pyarchey.git
    cd pyarchey
    python setup.py install

If you plan on doing some development, instead of `install` you can do `develop`.

## Usage

To run:

	pyarchey

## To Do

Some things I would like to do:

- [ ] Display user defined ascii art from command line
- [ ] Display all ascii art
- [ ] Get a better Raspbian image
- [ ] Get a generic linux penguin image if distribution cannot be determined
- [ ] Return info in json format
- [ ] Turn colors on/off
- [ ] Allow different colors to be defined from command line

## History

As far as I am aware, this was started by @djmelik which was then forked by @mikeantonacci where I forked it form him.
