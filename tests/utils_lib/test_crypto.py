"""Tests for ``utils.crypto`` module."""

from requests import Response

import pytest

from mws.utils.crypto import response_md5_is_valid
from mws.utils.crypto import calc_md5


def test_calc_md5():
    content = b"abc\tdef"
    assert calc_md5(content) == b"Zj+Bh1BJ8HzBb9ToK28qFQ=="


def test_response_md5_is_valid():
    correct_hash = "Zj+Bh1BJ8HzBb9ToK28qFQ=="
    response = Response()
    response._content = b"abc\tdef"
    response.headers["content-md5"] = correct_hash
    assert response_md5_is_valid(response) is True

    response.headers["content-md5"] = "incorrect hash!"
    assert response_md5_is_valid(response) is False


def test_response_no_md5_is_valid():
    """A response with no 'content-md5' header should pass validation."""
    response = Response()
    response._content = b"abc\tdef"
    assert response_md5_is_valid(response) is True
