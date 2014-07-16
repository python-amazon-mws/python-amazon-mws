#!/usr/bin/env python
from setuptools import setup

version = '0.5'

setup(
    name="python-amazon-mws",
    version=version,
    description="A python interface for Amazon MWS",
    author="Paulo Alvarado",
    author_email="commonzenpython@gmail.com",
    url="http://github.com/czpython/python-amazon-mws",
    packages=['mws'],
    download_url = 'https://github.com/czpython/python-amazon-mws/tarball/0.3',
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Internet",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"],
    install_requires=[
        'requests',
    ],
)
