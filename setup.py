# -*- coding: utf-8 -*-
import setuptools
import sys

short_description = 'Python library for interacting with the Amazon MWS API'

try:
    from pypandoc import convert_file
    long_description = convert_file('README.md', 'rst')
except (ImportError, OSError):  # either pypandoc or pandoc isn't installed
    long_description = "See README.md"

requires = [
    'requests',
    'xmltodict'
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
    version='1.0.0dev12',
    maintainer="James Hiew",
    maintainer_email="james@hiew.net",
    url="http://github.com/jameshiew/mws",
    description=short_description,
    long_description=long_description,
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
    ],
    platforms=['OS Independent'],
    license='Unlicense',
    include_package_data=True,
    zip_safe=False,
)
