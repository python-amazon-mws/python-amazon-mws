# -*- coding: utf-8 -*-
import setuptools

version = "1.0dev16"
homepage = "https://github.com/python-amazon-mws/python-amazon-mws"
short_description = "Python library for interacting with the Amazon MWS API"
with open("README.md", encoding="utf-8") as readme:
    long_description = readme.read()

requires = [
    "requests",
    "xmltodict>=0.12.0,<0.13",
]

setuptools.setup(
    name="mws",
    version=version,
    maintainer="python-amazon-mws",
    download_url=homepage + "/archive/v{}.tar.gz".format(version),
    maintainer_email="python-amazon-mws@googlegroups.com",
    url=homepage,
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    install_requires=requires,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    platforms=["OS Independent"],
    license="Unlicense",
    include_package_data=True,
    zip_safe=False,
)
