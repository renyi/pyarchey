=========
PyArchey
=========

.. image:: https://travis-ci.org/walchko/pyarchey.svg?branch=0.5
    :target: https://travis-ci.org/walchko/pyarchey
.. image:: https://pypip.in/version/pyarchey/badge.svg
    :target: https://pypi.python.org/pypi/pyarchey/
    :alt: Latest Version
.. image:: https://pypip.in/download/pyarchey/badge.svg
    :target: https://pypi.python.org/pypi//pyarchey/
    :alt: Downloads
.. image:: https://pypip.in/license/pyarchey/badge.svg
    :target: https://pypi.python.org/pypi/pyarchey/
    :alt: License

This is based off the ``archey`` command (which is also python) distributed by various linux, unix, and osx package managers. In order to avoid a naming conflict between them, I called this ``pyarchey``.

Currently, ``pyarchey`` supports Arch, Fedora, LinuxMint, Ubuntu, SUSE, Debian, Raspbian, generic Linux, and Slackware.

::

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

-------------
Requirements
-------------

Some of the custom code was removed and ``psutil`` was used to provide a cross-platform solution.

--------
Install
--------

The preferred way is to use `pypi.org <https://pypi.python.org/pypi>`_ ::

    pip install pyarchey

You can also do::

    git clone https://github.com/walchko/pyarchey.git
    cd pyarchey
    python setup.py install

If you plan on doing some development, instead of `install` you can do `develop`.

------
Usage
------

To run::

	pyarchey

args:

--display     display ascii logos for all distributions
--help        help
--json        output json of system info, nothing is printed to the screen
--zeroconfig  add ``.local`` to a hostname for zeroconfig to find IP address easier

------
To Do
------

Some things I would like to do:

- Display user defined ascii art from command line
- Get a better Raspbian image
- Turn colors on/off
- Allow different colors to be defined from command line

--------
History
--------

As far as I am aware, this was started by @djmelik which was then forked by @mikeantonacci where I forked it form him.

--------------
Contributions
--------------

- Dimitris Zlatanidis (dslackw) - Slackware support
- mikeantonacci - fixed tab errors

--------
Changes
--------

=========  ========  ======
Date       Version   Notes
=========  ========  ======
29 Mar 15  0.4.0     Forked
 4 Apr 15  0.5.0     Added Apple logo, changed custom code to psutil
11 Apr 15  0.6.0     Added commandline args for: displaying ascii logos, json output, zeroconfig
=========  ========  ==================
