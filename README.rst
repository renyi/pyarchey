=========
PyArchey
=========

.. image:: https://imgs.xkcd.com/comics/automation.png
	:align: center


.. image:: https://travis-ci.org/walchko/pyarchey.svg?branch=master
    :target: https://travis-ci.org/walchko/pyarchey
.. image:: https://img.shields.io/pypi/v/pyarchey.svg
    :target: https://pypi.python.org/pypi/pyarchey/
    :alt: Latest Version
.. image:: https://img.shields.io/pypi/dm/pyarchey.svg
    :target: https://pypi.python.org/pypi/pyarchey/
    :alt: Downloads
.. image:: https://img.shields.io/pypi/l/pyarchey.svg
    :target: https://pypi.python.org/pypi/pyarchey/
    :alt: License

This is based off the ``archey`` command (which is also python) distributed by various 
linux, unix, and osx package managers. In order to avoid a naming conflict between them, 
I called this ``pyarchey``.

Currently, ``pyarchey`` supports logos for Arch, Fedora, LinuxMint, Ubuntu, SUSE, Debian, 
Raspbian, Gentoo, OpenBSD, generic Linux, and Slackware.

::

    [kevin@Tardis soccer2]$ pyarchey -z
    
                      ##             User: kevin
                   ####              Hostname: Tardis.local
                   ##                IP: 192.168.1.4 / 58:B0:35:F2:25:D8
           #######    #######        OS: Mac OSX 10.10.5 x86_64
         ######################      Kernel: 14.5.0
        #####################        Uptime: 13 days 14 hrs 45 mins
        ####################         Shell: /bin/bash
        ####################         Processes: 214 running
        #####################        Packages: 113
         ######################      CPU: Intel Core2 Duo P8600 @ 2.40GHz
          ####################       CPU Usage: [17.8, 13.9]
            ################         RAM: 7.0 GB/ 8.0 GB
              ###     ####           Disk: 219.0 / 233.0 GB



    pi@calculon ~/github/pyarchey $ pyarchey -z

            .~~.   .~~.      User: pi
           '. \ ' ' / .'     Hostname: calculon
            .~ .~~~..~.      IP: 192.168.1.17 / B8:27:EB:0A:5A:17
           : .~.'~'.~. :     OS: Raspbian 7 (wheezy) armv6l
          ~ (   ) (   ) ~    Kernel: 4.1.6+
         ( : '~'.~.'~' : )   Uptime: 15 days 21 hrs 23 mins
          ~ .~ (   ) ~. ~    Shell: /bin/bash
           (  : '~' :  )     Processes: 73 running
            '~ .~~~. ~'      Packages: 960
                '~'          CPU: ARMv6-compatible processor rev 7 (v6l)
                             CPU Usage: [1.0]
                             RAM: 216.0 MB/ 229.0 MB
                             Disk: 4.0 / 15.0 GB


    pi@calculon ~/github/pyarchey $ pyarchey -zj
    {"Kernel": "4.1.6+", "Uptime": "15 days 21 hrs 39 mins", "Shell": "/bin/bash", 
    "Disk": "4.0 / 15.0 GB", "IP": "192.168.1.17 / B8:27:EB:0A:5A:17", "Hostname": 
    "calculon", "Processes": "73 running", "RAM": "215.0 MB/ 229.0 MB", "User": "pi", 
    "CPU Usage": "[3.9]", "Packages": 960, "OS": "Raspbian 7 (wheezy) armv6l", "CPU": 
    "ARMv6-compatible processor rev 7 (v6l)"}


-------------
Requirements
-------------

Some of the custom code was removed and ``psutil`` was used to provide a cross-platform 
solution.

--------
Install
--------

The preferred way is to use `pypi.org <https://pypi.python.org/pypi>`_ ::

    pip install pyarchey

You can also do::

    git clone https://github.com/walchko/pyarchey.git
    cd pyarchey
    python setup.py install

If you plan on doing some development, instead of ``install`` you can do ``develop``.

------
Usage
------

To run::

	pyarchey

args:

-d, --display     display ascii logos for all distributions
-h, --help        help
-j, --json        output json of system info, nothing is printed to the screen
-z, --zeroconfig  add ``.local`` to a hostname for zeroconfig to find IP address easier


--------
History
--------

As far as I am aware, this was started by @djmelik which was then forked by 
@mikeantonacci where I forked it form him.

--------------
Contributions
--------------

- Dimitris Zlatanidis (dslackw) - Slackware support
- mikeantonacci - fixed tab errors
- Alessandro-Barbieri - Gentoo support

--------
Changes
--------
=============  ========  ======
Date           Version   Notes
=============  ========  ======
29 Mar 15      0.4.0     Forked
 4 Apr 15      0.5.0     Added Apple logo, changed custom code to ``psutil``
11 Apr 15      0.6.0     Added commandline args for: displaying ascii logos, json output, zeroconfig
26 Aug 15      0.6.2     Minor fixes
21 Sep 15      0.6.3     OSX now reports OSX version and minor other fixes
=============  ========  ======
