# mws [![PyPI version](https://badge.fury.io/py/mws.svg)](https://badge.fury.io/py/mws) [![Gitter chat](https://badges.gitter.im/python-amazon-mws/python-amazon-mws.png)](https://gitter.im/python-amazon-mws/community)

master: 
[![Requirements Status](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements.svg?branch=master)](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements/) [![Build Status](https://travis-ci.org/python-amazon-mws/python-amazon-mws.svg?branch=master)](https://travis-ci.org/python-amazon-mws/python-amazon-mws?branch=master) [![codecov](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/master/graph/badge.svg)](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/master)

develop: 
[![Requirements Status](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements.svg?branch=develop)](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements/) [![Build Status](https://travis-ci.org/python-amazon-mws/python-amazon-mws.svg?branch=develop)](https://travis-ci.org/python-amazon-mws/python-amazon-mws?branch=develop) [![codecov](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/develop/graph/badge.svg)](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/develop)

Python package for interacting the [Amazon Marketplace Web Services](http://docs.developer.amazonservices.com/en_UK/dev_guide/index.html) API.

This project is a fork and continuation of [czpython/python-amazon-mws](https://github.com/czpython/python-amazon-mws) with added Python 3 support.

# Installation

Install the latest version from PyPI.

```
pip install mws
```

Currently the `mws` package on PyPI points to the 0.x branch, but at some later point may point to 1.x. 

| Versions | Description                                                                                                                                                                                | Branch  |
|----------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------|
| 0.x      | A backwards-compatible drop in replacement for the original package (i.e. same method signatures, class names, etc) with some extra features and anything that was obviously broken fixed. | master  |
| 1.x      | New features along with backwards-incompatible API changes.                                                                                                                                | develop |

If you want to continue using the 0.x versions, please pin your package to major version 0. i.e use something like `mws~=0.8.6` in your project's `requirements.txt`. 

If you want to use 1.x functionality right now, you can install directly from the Git repo. 

```
pip install git+https://github.com/python-amazon-mws/python-amazon-mws.git@develop#egg=mws
```

# Quickstart

Export your API credentials as environment variables in your shell.

```
export MWS_ACCOUNT_ID=...
export MWS_ACCESS_KEY=...
export MWS_SECRET_KEY=...
```

Now you can experiment with the API from within an interactive Python shell e.g.

```
>>> import mws, os
>>> orders_api = mws.Orders(
...     access_key=os.environ['MWS_ACCESS_KEY'],
...     secret_key=os.environ['MWS_SECRET_KEY'],
...     account_id=os.environ['MWS_ACCOUNT_ID'],
...     region='UK',   # defaults to 'US'
... )
>>> service_status = orders_api.get_service_status()
>>> service_status
<mws.mws.DictWrapper object at 0x1063a2160>
>>> service_status.original
'<?xml version="1.0"?>\n<GetServiceStatusResponse xmlns="https://mws.amazonservices.com/Orders/2013-09-01">\n  <GetServiceStatusResult>\n    <Status>GREEN</Status>\n    <Timestamp>2017-06-14T16:39:12.765Z</Timestamp>\n  </GetServiceStatusResult>\n  <ResponseMetadata>\n    <RequestId>affdec68-05d2-4bc5-a8a4-bb40f307dd6b</RequestId>\n  </ResponseMetadata>\n</
GetServiceStatusResponse>\n'
>>> service_status.parsed
{'value': '\n    ', 'Status': {'value': 'GREEN'}, 'Timestamp': {'value': '2017-06-14T16:39:12.765Z'}}
>>> service_status.response
<Response [200]>
```

# Development
All dependencies for working on `mws` are in `requirements.txt` and `docs/requirements.txt`.

## Tests
Tests are run with pytest. We test against Python 2.7 and supported Python 3.x versions with Travis.

## Documentation
Docs are built using Sphinx. Change into the `docs/` directory and install any dependencies from the `requirements.txt` there.

To build HTML documentation, run:

```
make html
```
The output HTML documentation will be in `docs/build/`.

To run a live reloading server serving the HTML documentation (on port 8000 by default):

```
make livehtml
```

## Contributing
Please make pull requests to `develop`. Code coverage isn't necessary but encouraged where possible (especially for anything which might behave differently between Python 2/3).
