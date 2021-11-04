#!/usr/bin/env python

from distutils.core import setup

setup(name='Tilibot',
      version='1.0', # Fix
      description='Tiliqua Biomechanics Emulation', 
      author='Dan Gibbons',
      author_email='danegibbons@gmail.com',
      url='', # Fix
      packages=['distutils', 'distutils.command'], # Fix
      python_requires='>=3.8'
     )
