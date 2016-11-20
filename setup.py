# -*- coding: utf-8 -*-
from pypandoc import convert
from setuptools import setup

setup(
    name='mws',
    version='0.7-dev',
    maintainer="James Hiew",
    maintainer_email="james@hiew.net",
    url="http://github.com/jameshiew/mws",
    description='Python library for interacting with the Amazon MWS API',
    long_description=convert("README.md", 'rst'),
    packages=['mws'],
    install_requires=[
        'requests'
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
    ],
    platforms=['OS Independent'],
    license='Unlicense',
    include_package_data=True,
    zip_safe=False
)
