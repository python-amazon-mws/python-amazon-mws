# mws [![PyPI version](https://badge.fury.io/py/mws.svg)](https://badge.fury.io/py/mws)

master: 
[![Requirements Status](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements.svg?branch=master)](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements/) [![Build Status](https://travis-ci.org/python-amazon-mws/python-amazon-mws.svg?branch=master)](https://travis-ci.org/python-amazon-mws/python-amazon-mws?branch=master) [![codecov](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/master/graph/badge.svg)](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/master)

develop: 
[![Requirements Status](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements.svg?branch=develop)](https://requires.io/github/python-amazon-mws/python-amazon-mws/requirements/) [![Build Status](https://travis-ci.org/python-amazon-mws/python-amazon-mws.svg?branch=develop)](https://travis-ci.org/python-amazon-mws/python-amazon-mws?branch=develop) [![codecov](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/develop/graph/badge.svg)](https://codecov.io/gh/python-amazon-mws/python-amazon-mws/branch/develop)

This is a fork and continuation of https://github.com/czpython/python-amazon-mws with preliminary Python 2/3 support.

The main aim is to provide a *backwards-compatible* drop in replacement for the original package (i.e. same method signatures, class names, etc) with some extra features and anything that was obviously broken fixed.

# Installation
Install from PyPI with `pip install mws`.

# Quickstart

Put your API credentials in your environment.

```bash
$ export MWS_ACCOUNT_ID=...
$ export MWS_ACCESS_KEY=...
$ export MWS_SECRET_KEY=...
```

Now you can experiment with the API from a shell.

```python
>>> import mws, os
>>> orders_api = mws.Orders(
...     access_key=os.environ['MWS_ACCESS_KEY'],
...     secret_key=os.environ['MWS_SECRET_KEY'],
...     account_id=os.environ['MWS_ACCOUNT_ID'],
...     region='UK',  # if necessary
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
