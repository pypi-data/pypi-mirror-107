#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata FJH
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name='wfz_fjh',
    version='1.0.3',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    license='Apache License',
    author='fjh',
    author_email='1160230887@qq.com',
    url='http://www.reshapedata.com',
    description='reshape data type in py language ',
    keywords=['reshapedata', 'rdt', 'wfz_fjh'],
    python_requires='>=3.6',
)
