#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='drcutils',
      version='0.1.0',
      description='Utilities for research in the Design Research Collective',
      author='The Design Research Collective',
      author_email='ask-drc@andrew.cmu.edu',
      url='https://github.com/cmudrc/drcutils/',      
      install_requires=[ 
            "datasets", 
            "gradio", 
            "huggingface_hub", 
            "IPython", 
            "keras"
            "matplotlib",
            "netron",
            "numpy",
            "numpy-stl", 
            "Pillow", 
            "plotly", 
            "svgpathtools"
      ],
      packages=['drcutils'],
      package_dir={'drcutils': 'src/drcutils'},
      package_data={'drcutils': ['data/*']},
)
