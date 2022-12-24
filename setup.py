#!/usr/bin/env python

from setuptools import setup, find_packages
import mock
import sys

MOCK_MODULES = ['numpy', 'scipy', 'matplotlib', 'matplotlib.pyplot', 'scipy.interpolate', "numpy-stl"]
for mod_name in MOCK_MODULES:
      sys.modules[mod_name] = mock.Mock()

setup(
      name='drcutils',
      version='0.1.0',
      description='Utilities for research in the Design Research Collective',
      author='The Design Research Collective',
      author_email='ask-drc@andrew.cmu.edu',
      url='https://github.com/cmudrc/drcutils/',      
      install_requires=[ 
            "IPython",
            "matplotlib",
            "netron",
            "numpy",
            "numpy-stl", 
            "Pillow", 
            "plotly", 
            "svgpathtools",
      ],
      packages=find_packages(),
      package_data={'drcutils': ['data/*']},
)
