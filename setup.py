# -*- coding: utf-8 -*-
from setuptools import setup

short_description = 'Python library for interacting with the Amazon MWS API'

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'rst')
except (ImportError, OSError):  # either pypandoc or pandoc isn't installed
    long_description = "See README.md"

setup(
    name='mws',
    version='0.8.6',
    maintainer="James Hiew",
    download_url='https://github.com/python-amazon-mws/python-amazon-mws/archive/v0.8.6.tar.gz',
    maintainer_email="james@hiew.net",
    url="http://github.com/jameshiew/mws",
    description=short_description,
    long_description=long_description,
    packages=['mws'],
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    platforms=['OS Independent'],
    license='Unlicense',
    include_package_data=True,
    zip_safe=False,
)
