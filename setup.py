#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='drcutils',
      version='0.1.0',
      description='DRC Utilities',
      author='Chris McComb',
      author_email='ccmcc2012@gmail.com',
      url='https://github.com/cmudrc/drcutils/',      
      install_requires=["numpy", "matplotlib", "huggingface_hub", "datasets", "gradio", "numpy-stl", "Pillow", "svgpathtools", "plotly"],
      packages=['drcutils'],
      package_dir={'drcutils': 'src/drcutils'},
      package_data={'drcutils': ['data/*']},
      )
