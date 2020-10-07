"""Tests to ensure deprecation warnings are raised for objects being removed in v1.1"""

import pytest

from mws.utils.deprecation import RemovedInPAM11Warning
from mws.utils.parsers import (
    DataWrapper,
    DictWrapper,
    ObjectDict,
    XML2Dict,
)


### DEPRECATION TESTING - REMOVE IN v1.1 ###
def test_datawrapper_removed_in_v11():
    """DataWrapper class."""
    data = b"abc\tdef"
    hash_ = "Zj+Bh1BJ8HzBb9ToK28qFQ=="
    with pytest.warns(RemovedInPAM11Warning):
        DataWrapper(data, {"content-md5": hash_})


def test_dictwrapper_removed_in_v11():
    """DictWrapper class."""
    data = b"<Some><Content>We don't care about!</Content></Some>"
    with pytest.warns(RemovedInPAM11Warning):
        DictWrapper(data)


def test_objectdict_removed_in_v11():
    """ObjectDict class."""
    with pytest.warns(RemovedInPAM11Warning):
        ObjectDict({"This": "is", "going": "away", "in": "favor", "of": "DotDict!"})


def test_xml2dict_removed_in_v11():
    """XML2Dict class."""
    with pytest.warns(RemovedInPAM11Warning):
        # Strangely, nothing in __init__
        # Only real use was the `fromstring` method, which wasn't even a class method.
        # Typical usage was:
        #   XML2Dict().fromstring(remove_xml_namespaces("content"))
        # which itself was only called in `DictWrapper` class.
        # Just... odd, really. Better to replace the entire mess with a pure function.
        XML2Dict()


# TODO tests that check methods decorated with `kwargs_renamed_for_v11`.
# Individual methods? Parametrize them with the old, the new, check for deprecation,
# and expect a certain key to be in params output.
# Might be difficult for certain tests, though.
# @pytest.mark.parametrize("api_class, method, old, new, expected_param", [
#     ()
# ])
# def test_kwargs_renamed_working(method, old, new, expected_param):
#     pass
