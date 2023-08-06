#!/usr/bin/python
# -*- coding: UTF-8 -*-
import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='traffic_control',
    version='0.0.1',
    packages=setuptools.find_packages(),
    url=None,
    license='MIT',
    author='Martin',
    author_email='majianli@corp.netease.com',
    description='A small example package',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['paramiko'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
