import pytest

from mws.mws import DataWrapper, MWSError


def test_content_md5_comparison():
    data = b"abc\tdef"
    hash = "Zj+Bh1BJ8HzBb9ToK28qFQ=="
    DataWrapper(data, {"content-md5": hash})


def test_content_md5_check_raises_exception_if_fails():
    data = b"abc\tdef"
    hash = "notthehash"
    with pytest.raises(MWSError):
        DataWrapper(data, {"content-md5": hash})
