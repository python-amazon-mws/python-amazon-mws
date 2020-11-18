"""Utilities for hashing and cryptography."""

import base64
import hashlib


def calc_md5(string):
    """Generates base64-encoded MD5 hash of `string`."""
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b"\n")


def response_md5_is_valid(response):
    """Checks the MD5 hash of ``response.content`` against that response's
    "content-md5" header. Returns ``True`` if they match, else ``False``.
    If the response does not include a ``content-md5`` header, we can't verify it,
    but we should not hold up that response. Thus, returns ``True`` in this case.
    """
    if "content-md5" not in response.headers:
        # We can't check a hash that doesn't exist,
        # but we won't stop responses that don't supply one.
        return True

    hash_ = calc_md5(response.content)
    return response.headers["content-md5"].encode() == hash_
