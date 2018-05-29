import pytest
import requests

from mws.mws import validate_hash, MWSError


class Fake_Response(object):
    def __init__(self, content, hash):
        self.status_code = 200
        self.headers = {'content-md5': hash}
        self.content = content


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
