# -*- coding: utf-8 -*-
# @Time : 2021/5/25 15:27 
# @Author : liyf--95/02/02
# @File : setup.py 
# @Software: PyCharm

from __future__ import print_function
from setuptools import setup, find_packages
import sys

import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="ramdom_ua",
    version="1.0",
    author="liyf",
    author_email="liyufeng_0202@163.com",
    description="get ua",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitee.com/liyufeng0202/random_ua",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)