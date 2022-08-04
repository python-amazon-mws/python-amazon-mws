# -*- coding: utf-8 -*-
from pathlib import Path

import setuptools

BASE_DIR = Path(__file__).resolve().parent

version = "1.0dev19"
homepage = "https://github.com/python-amazon-mws/python-amazon-mws"
short_description = "Python library for interacting with the Amazon MWS API"

readme = BASE_DIR / "README.md"
long_description = readme.read_text(encoding="utf-8")

# Base requirements
install_requires = [
    "requests",
    "defusedxml>=0.7.1",
    "xmltodict>=0.12.0",
]

## Extras ##
# Development tools
extras_require_dev = [
    # pre-commit hooks to ensure code quality before committing.
    #   Run `pre-commit install` to add the git pre-commit hook,
    #   then `pre-commit run --all-files` for initial checks.
    #   More info: https://pre-commit.com
    "pre-commit~=2.19.0",
    # linting
    "flake8~=4.0.1",
    "flake8-bandit~=3.0.0",
    "flake8-isort~=4.1.1",
    # security scanning
    "bandit~=1.7.4",
    # formatting
    "black~=22.3.0",
    # testing
    "pytest~=7.1.2",
    "pytest-cov~=3.0.0",
]

# Documentation
# See `docs/requirements.txt` for list of requirements.
# We maintain the requirements.txt there so ReadTheDocs can access it directly.
docs_requirements = BASE_DIR / "docs" / "requirements.txt"
extras_require_docs = docs_requirements.read_text().strip().split("\n")

extras_require = {
    "develop": extras_require_dev,
    "docs": extras_require_docs,
    # Combine all extras into a shorthand 'all' for convenience
    "all": extras_require_dev + extras_require_docs,
}

setuptools.setup(
    name="mws",
    version=version,
    maintainer="python-amazon-mws",
    download_url=f"{homepage}/archive/v{version}.tar.gz",
    maintainer_email="griceturrble@protonmail.com",
    url=homepage,
    description=short_description,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(
        exclude=[
            "tests",
            "tests.*",
        ]
    ),
    install_requires=install_requires,
    extras_require=extras_require,
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    platforms=["OS Independent"],
    license="Unlicense",
    include_package_data=True,
    zip_safe=False,
)
