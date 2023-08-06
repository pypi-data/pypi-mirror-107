#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 25 15:35:12 2021

@author: newmac
"""

from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    url='https://github.com/tspeer/helloworld',
    author='Thomas Speer',
    author_email='tspeer@utexas.edu',
    name='helloworld_tspeer',
    version='0.0.1',
    description='Say hello!',
    py_modules=['helloworld'],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires = [],
    extras_require = {
        "dev": [
            "pytest>=3.7",
            ],
        },
)
