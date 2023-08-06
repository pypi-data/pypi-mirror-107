#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    reshapedata LLC
"""
import platform
from setuptools import setup
from setuptools import find_packages

setup(
    name = 'wfzdy_pyrdt',
    version = '1.0.1',
    install_requires=[
        'requests',
    ],
    packages=find_packages(),
    license = 'dingyan',
    author = 'Reshapedata',
    author_email = 'hulilei@takewiki.com.cn',
    url = 'http://www.reshapedata.com',
    description = 'reshape data type in py language ',
    keywords = ['reshapedata', 'rdt','wfzdy_pyrdt'],
    python_requires='>=3.6',
)
