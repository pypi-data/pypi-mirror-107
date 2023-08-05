#!/usr/bin/env python3

from setuptools import setup

setup(
   name='piemmer',
   version='1.0.1-dev',
   description='A algorithm to simplify the input for principal component analysis',
   author='Hao-Wei chang',
   author_email='emmer.man42@gmail.com',
   packages=['piemmer'],
   install_requires=['numpy', 'pandas', 'matplotlib', 'skbio', 'scipy'],
)
