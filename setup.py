#!/usr/bin/env python

from distutils.core import setup

setup(name='Tilibot',
      version='1.0', # Fix
      description='Tiliqua Biomechanics Emulation', 
      author='Dan Gibbons',
      author_email='danegibbons@gmail.com',
      packages=['distutils', 'distutils.command'], # Fix
     )