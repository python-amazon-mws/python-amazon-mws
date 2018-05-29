import pytest

from mws.mws import validate_hash, MWSError


def test_content_md5_comparison():
    content = b'abc\tdef'
    hash = 'Zj+Bh1BJ8HzBb9ToK28qFQ=='
    response = {'content': content, 'headers': {'content-md5': hash}}
    validate_hash(response)


def test_content_md5_check_raises_exception_if_fails():
    content = b'abc\tdef'
    hash = 'notthehash'
    response = {'content': content, 'headers': {'content-md5': hash}}
    with pytest.raises(MWSError):
        validate_hash(response)
