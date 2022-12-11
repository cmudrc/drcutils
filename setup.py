#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='drcutils',
      version='0.1.0',
      description='DRC Utilities',
      author='Chris McComb',
      author_email='ccmcc2012@gmail.com',
      url='https://github.com/cmudrc/drcutils/',
      packages=find_packages("src/*"),
      )
