# mws
[![Requirements Status](https://requires.io/github/jameshiew/mws/requirements.svg)](https://requires.io/github/jameshiew/mws/requirements/) [![PyPI version](https://badge.fury.io/py/mws.svg)](https://badge.fury.io/py/mws) [![Build Status](https://travis-ci.org/jameshiew/mws.svg)](https://travis-ci.org/jameshiew/mws)

This is a fork and continuation of https://github.com/czpython/python-amazon-mws with preliminary Python 2/3 support.

Install from PyPI with `pip install mws`.

Pull requests welcome.

## Quickstart

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
>>> orders_api.get_service_status()
<mws.mws.DictWrapper object at 0x1053c4630>
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
