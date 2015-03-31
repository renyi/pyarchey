import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="pyarchey",
    version="0.4",
    author="Kevin Walchko",
    keywords='system info',
    author_email="kevin.walchko@outlook.com",
    description="A simple python scrip to display an OS logo in ASCII art along with basic system information.",
    license="GPL",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        #'Intended Audience :: Developers',
        #'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GPL License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        # 'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: 3.4',
    ],
    install_requires=['psutil'],
    url="",
    long_description=read("README.md"),
    packages=["pyarchey"],
    entry_points={
        'console_scripts': [
            'pyarchey=pyarchey.pyarchey:main',
        ],
    },
)
