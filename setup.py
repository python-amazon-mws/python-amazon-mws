#!/usr/bin/env python

from setuptools import setup

setup(
    name="python-amazon-mws",
    version="0.2",
    description="A python interface for Amazon MWS",
    author="Paulo Alvarado",
    author_email="commonzenpython@gmail.com",
    url="http://github.com/czpython/python-amazon-mws",
    packages=['mws'],
    install_requires=[
        'requests',
    ],
)