# -*- coding: utf-8 -*-
"""
Created on Sat Oct 13 16:30:30 2018

@author: shane
"""

import glob
import os
import shutil
import sys

from setuptools import find_packages, setup

from ntclient import __title__, __version__, PY_MIN_VER, PY_SYS_VER

# Old pip doesn't respect `python_requires'
if PY_SYS_VER < PY_MIN_VER:
    PY_MIN_STR = ".".join(str(x) for x in PY_MIN_VER)
    PY_SYS_STR = ".".join(str(x) for x in PY_SYS_VER)
    print("ERROR: nutra requires Python %s or later to install" % PY_MIN_STR)
    print("HINT:  You're running Python " + PY_SYS_STR)
    sys.exit(1)

# cd to parent dir of setup.py
os.chdir(os.path.dirname(os.path.abspath(__file__)))
shutil.rmtree("dist", True)

CLASSIFIERS = [
    "Environment :: Console",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "Intended Audience :: Healthcare Industry",
    "Intended Audience :: Education",
    "Development Status :: 3 - Alpha",
    "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

# TODO:resolve Levenshtein build error on Windows
REQUIREMENTS = [
    "argcomplete",
    "colorama",
    "fuzzywuzzy",
    # "python-Levenshtein",
    "requests",
    "tabulate",
]

README = open("README.rst").read()

setup(
    name=__title__,
    author="gamesguru",
    author_email="mathmuncher11@gmail.com",
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    python_requires=">=3.4.3",
    packages=find_packages(exclude=["test"]),
    include_package_data=True,
    scripts=glob.glob("scripts/*"),
    # entry_points={"console_scripts": ["nutra=ntclient.__main__:main"]},
    description="Home and office nutrient tracking software",
    long_description=README,
    long_description_content_type="text/x-rst",
    url="https://github.com/nutratech/cli",
    license="GPL v3",
    version=__version__,
)

# Clean up
shutil.rmtree(__title__ + ".egg-info", True)
shutil.rmtree("__pycache__", True)
shutil.rmtree(".pytest_cache", True)
