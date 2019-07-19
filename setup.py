import os
from setuptools import setup

from pyarchey import __version__ as VERSION


def read(fname):
    with open(os.path.join(os.path.dirname(__file__), fname)) as f:
        return f.read()


with open('requirements.txt') as f:
    requirements = f.read().splitlines()


setup(
    name="pyarchey2",
    version=VERSION,
    author="Renyi Khor",
    keywords=['system info', 'ascii art', 'archey'],
    author_email="renyi.ace@gmail.com",
    description="PyArchey2 is a fork of PyArchey. It is an attempt to speed up PyArchey by introducing multithreading and dropping support for Python2.",
    license="GPL",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2.7',
        # 'Programming Language :: Python :: 2 :: Only',
        # 'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.2',
        # 'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',
        # 'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',

        # Operating systems this runs on
        'Operating System :: Unix',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX',

        # what does this do?
        'Topic :: Utilities',
        'Topic :: System :: Shells',
        'Environment :: Console'
    ],
    install_requires=requirements,
    url="https://github.com/renyi/pyarchey2",
    long_description=read("README.rst"),
    packages=["pyarchey"],
    entry_points={
        'console_scripts': [
            'pyarchey=pyarchey.pyarchey:main',
        ],
    },
)
