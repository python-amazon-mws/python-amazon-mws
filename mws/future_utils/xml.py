"""Utilities for working with XML documents, particularly those
that are returned in a majority of MWS responses.
"""

import re

from mws.future_utils.collections import DotDict

# from mws.utils import DotDict
MWS_ENCODING = "iso-8859-1"
"""Amazon documents this as the encoding to expect in responses.
If it doesn't work, :shrug:, we'll have to wing it.
"""


def remove_xml_namespaces(data):
    """Return namespaces found in the XML `data`, in either str or bytes format."""
    pattern = r'xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)'
    replacement = ""
    if not isinstance(data, str):
        # Encode the pattern and substitute to use them on bytes data.
        pattern = pattern.encode()
        replacement = replacement.encode()
    return re.sub(pattern, replacement, data)


def mws_xml_to_dict(data, encoding=MWS_ENCODING, force_cdata=False, **kwargs):
    raise NotImplementedError("This method is only available in 1.0+")


def mws_xml_to_dotdict(data, encoding=MWS_ENCODING, result_key=None, force_cdata=False):
    raise NotImplementedError("This method is only available in 1.0+")
