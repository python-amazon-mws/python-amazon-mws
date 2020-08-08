"""Utilities for hashing and cryptography."""


import base64
import hashlib


def calc_md5(string):
    """Generates base64-encoded MD5 hash of `string`."""
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b"\n")
