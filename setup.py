#!/usr/bin/env python

from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(name='polygon_utils',
      version='1.0',
      packages=['polygon_utils',
                'polygon_utils.utils',
                ],
      install_requires=required,
     )