#!/usr/bin/env python

from setuptools import setup
from sys import path

setup(name= 'scipaas',
    version= '0.1.0',
    author= 'Wesley Brewer',
    author_email= 'wes@fluidphysics.com',
    py_modules= ['scipaas'],
    url= 'http://fluidphysics.com',
    license= 'MIT',
    description= 'A middleware execution platform for running scientific applications in the cloud.',
    long_description= open(path[0]+'/README.md', 'r').read(),
    install_requires= [
        'web2py >= 2.1.1',
        'boto >= 2.3.6',
        ],
)
