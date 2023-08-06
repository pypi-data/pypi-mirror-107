#!/usr/bin/env python3

from setuptools import setup, find_packages

setup(
   name='piemmer',
   version='1.0.4-dev',
   description='A algorithm to simplify the input for principal component analysis',
   author='Hao-Wei chang',
   author_email='emmer.man42@gmail.com',
   packages=find_packages(),
   package_data={'piemmer': ['data/*.csv', 'data/*/*.csv', 'data/*/*/*.csv']},
   install_requires=['numpy', 'pandas', 'matplotlib', 'scikit-bio', 'scipy', 'tqdm', 'statsmodels'],
)
