# PyArchey

[![Build Status](https://travis-ci.org/walchko/archey.svg?branch=master)](https://travis-ci.org/walchko/archey)

    [kevin@Tardis ~]$ pyarchey

                    ##             User: kevin
                 ####              Hostname: Tardis.local
                 ##                IP: 192.168.1.4
         #######    #######        OS: Mac OSX x86_64
       ######################      Kernel: 14.1.0
      #####################        Uptime: 0 days 9:28
      ####################         Shell: /bin/bash
      ####################         Terminal: Processes running: 219
      #####################        Packages: 112
       ######################      CPU: Intel Core2 Duo P8600 @ 2.40GHz
        ####################       Misc: CPU usage: [46.0, 34.0]
          ################         RAM: 7 MB / 8 GB
            ###     ####           Disk: 93 / 232 GB

## Requirements

Some of the custom code was removed and `psutil` was used to provide a cross-platform solution.

## Install

The preferred way is to use pypi.org

    pip install pyarchey

You can also do

    git clone https://github.com/walchko/pyarchey.git
    cd pyarchey
    python setup.py install

If you plan on doing some development, instead of `install` you can do 'develop'.


## History

As far as I am aware, this was started by @djmelik which was then forked by @mikeantonacci where I forked it form him.
