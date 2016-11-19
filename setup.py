# -*- coding: utf-8 -*-
from setuptools import setup

setup(
    name='mws',
    version='0.6',
    maintainer="James Hiew",
    maintainer_email="james@hiew.net",
    url="http://github.com/jameshiew/mws",
    description='A python interface for Amazon MWS',
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
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    platforms=['OS Independent'],
    license='LICENSE.txt',
    include_package_data=True,
    zip_safe=False
)
