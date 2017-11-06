#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'commitizen-py2.7'
WORKDIR = 'commitizen'
DESCRIPTION = 'Python commitizen client tool.'
URL = 'https://github.com/ranshamay89/commitizen'
EMAIL = 'ran.shamay89@gmail.com'
AUTHOR = 'Ran Shamay'
REQUIRED = [
    'delegator.py', 'whaaaaat', 'configparser'
]

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

about = {}
with open(os.path.join(here, WORKDIR, '__version__.py')) as f:
    exec (f.read(), about)

setup(

    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    packages=find_packages(exclude=('tests',)),
    url='',
    author=AUTHOR,
    author_email=EMAIL,
    entry_points={
        'console_scripts': ['cz=commitizen.cli:main'],
    },
    install_requires=REQUIRED,
    zip_safe=True,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
