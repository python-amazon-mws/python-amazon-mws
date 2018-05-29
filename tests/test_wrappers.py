# -*- coding: utf-8 -*-

import pytest
import requests

from mws.mws import validate_hash, DataWrapper, MWSError


class Fake_Response(object):
    def __init__(self, content, hash=None, apparent_encoding=None):
        self.status_code = 200
        self.encoding = 'Cp1252'  # we overwrite this flag
        self.apparent_encoding = apparent_encoding
        self.headers = {'content-md5': hash}
        self.content = content  # is a byte string

    @property
    def text(self):
        return self.content.decode(self.encoding)


def test_content_md5_comparison(monkeypatch):
    def fake_get(url):
        return Fake_Response(content, hash)
    content = b'abc\tdef'
    hash = 'Zj+Bh1BJ8HzBb9ToK28qFQ=='
    monkeypatch.setattr(requests, 'get', fake_get)
    fake_event = {"channel": "nowhere"}

    response = requests.get(fake_event)
    validate_hash(response)


def test_content_md5_check_raises_exception_if_fails(monkeypatch):
    def fake_get(url):
        return Fake_Response(content, hash)
    content = b'abc\tdef'
    hash = 'notthehash'
    monkeypatch.setattr(requests, 'get', fake_get)
    fake_event = {"channel": "nowhere"}
    response = requests.get(fake_event)
    with pytest.raises(MWSError):
        validate_hash(response)


def test_DataWrapper_for_text(monkeypatch):
    def fake_get(url):
        return Fake_Response(content, apparent_encoding=apparent_encoding)
    content = b'Without an \xf6, you would miss something'
    apparent_encoding = 'ISO-8859-1'
    monkeypatch.setattr(requests, 'get', fake_get)
    fake_event = {"channel": "nowhere"}
    response = requests.get(fake_event)

    y = DataWrapper(response)
    # here we test the encoding from the request.text function
    assert y.parsed == content.decode(apparent_encoding)
    # parsed should return the textdata
    assert y.parsed == y.textdata
    # those attributes should be None, since we create dicts only for xml
    assert y._response_dict is None
    assert y.pydict is None


def test_DataWrapper_for_xml(monkeypatch):
    def fake_get(url):
        return Fake_Response(content, apparent_encoding=apparent_encoding)
    content = b'<ListInventorySupplyResponse \
        xmlns="http://mws.amazonaws.com/FulfillmentInventory/2010-10-01/">\n \
        <ListInventorySupplyResult>\n    \
        <MarketplaceId>A1PA6795UKMFR9</MarketplaceId>\n    \
        <InventorySupplyList/>\n  </ListInventorySupplyResult>\n  \
        <ResponseMetadata>\n    \
        <RequestId>12bdfc18-8ccd-410d-ad33-31d5345d7b17</RequestId>\n  \
        </ResponseMetadata>\n</ListInventorySupplyResponse>\n'
    apparent_encoding = 'ISO-8859-1'
    monkeypatch.setattr(requests, 'get', fake_get)
    fake_event = {"channel": "nowhere"}
    response = requests.get(fake_event)

    y = DataWrapper(response, rootkey='ListInventorySupplyResult')
    # pydict is not using the rootkey at the very moment
    assert y.pydict == {'ListInventorySupplyResult': {'InventorySupplyList': None,
                                                      'MarketplaceId': 'A1PA6795UKMFR9'},
                        'ResponseMetadata': {'RequestId': '12bdfc18-8ccd-410d-ad33-31d5345d7b17'}}
    # pytest can compare the dict representation
    assert vars(y.parsed) == {'_DotDict__data': {'InventorySupplyList': None,
                                                 'MarketplaceId': 'A1PA6795UKMFR9'}}
