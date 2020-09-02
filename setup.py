# -*- coding: utf-8 -*-
import sys

import setuptools

version = '1.0.4c'
homepage = 'https://github.com/python-amazon-mws/python-amazon-mws'
short_description = 'Python library for interacting with the Amazon MWS API'
with open('README.md') as readme:
    long_description = readme.read()

requires = [
    'requests',
]
extras_require = {
    ":python_version<'3.4'": ['enum34'],
}

# Fix for old setuptools versions.
# (Copied from source of the flake8 package)
if int(setuptools.__version__.split('.')[0]) < 18:
    extras_require = {}
    if sys.version_info < (3, 4):
        requires.append('enum34')

setuptools.setup(
    name='mws',
    version=version,
    maintainer='python-amazon-mws',
    download_url=homepage + '/archive/v{}.tar.gz'.format(version),
    maintainer_email='python-amazon-mws@googlegroups.com',
    url=homepage,
    description=short_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['mws', 'mws.apis'],
    install_requires=requires,
    extras_require=extras_require,
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
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    platforms=['OS Independent'],
    license='Unlicense',
    include_package_data=True,
    zip_safe=False,
)
