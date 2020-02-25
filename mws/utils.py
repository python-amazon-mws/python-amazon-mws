# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 15:42:07 2012
Borrowed from https://github.com/timotheus/ebaysdk-python
@author: pierre
"""
from __future__ import absolute_import
import base64
import datetime
import hashlib
import pprint
try:
    from collections.abc import Mapping, MutableSequence
except ImportError:
    from collections import Mapping, MutableSequence


def calc_md5(string):
    """
    Calculate the MD5 encryption for the given bytestring.
    """
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b'\n')


def enumerate_param(param, values):
    """
    Builds a dictionary of an enumerated parameter, using the param string and some values.
    If values is not a list, tuple, or set, it will be coerced to a list
    with a single item.
    Example:
        enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
    Returns:
        {
            MarketplaceIdList.Id.1: 123,
            MarketplaceIdList.Id.2: 345,
            MarketplaceIdList.Id.3: 4343
        }
    """
    if not values:
        # Shortcut for empty values
        return {}
    if not isinstance(values, (list, tuple, set)):
        # Coerces a single value to a list before continuing.
        values = [values, ]
    if not param.endswith('.'):
        # Ensure this enumerated param ends in '.'
        param += '.'
    # Return final output: dict comprehension of the enumerated param and values.
    return {
        '{}{}'.format(param, idx+1): val
        for idx, val in enumerate(values)
    }


def enumerate_params(params=None):
    """
    For each param and values, runs enumerate_param,
    returning a flat dict of all results
    """
    if params is None or not isinstance(params, dict):
        return {}
    params_output = {}
    for param, values in params.items():
        params_output.update(enumerate_param(param, values))
    return params_output


def enumerate_keyed_param(param, values):
    """
    Given a param string and a dict of values, returns a flat dict of keyed, enumerated params.
    Each dict in the values list must pertain to a single item and its data points.
    Example:
        param = "InboundShipmentPlanRequestItems.member"
        values = [
            {'SellerSKU': 'Football2415',
            'Quantity': 3},
            {'SellerSKU': 'TeeballBall3251',
            'Quantity': 5},
            ...
        ]
    Returns:
        {
            'InboundShipmentPlanRequestItems.member.1.SellerSKU': 'Football2415',
            'InboundShipmentPlanRequestItems.member.1.Quantity': 3,
            'InboundShipmentPlanRequestItems.member.2.SellerSKU': 'TeeballBall3251',
            'InboundShipmentPlanRequestItems.member.2.Quantity': 5,
            ...
        }
    """
    if not values:
        # Shortcut for empty values
        return {}
    if not param.endswith('.'):
        # Ensure the enumerated param ends in '.'
        param += '.'
    if not isinstance(values, (list, tuple, set)):
        # If it's a single value, convert it to a list first
        values = [values, ]
    for val in values:
        # Every value in the list must be a dict.
        if not isinstance(val, dict):
            # Value is not a dict: can't work on it here.
            raise ValueError((
                "Non-dict value detected. "
                "`values` must be a list, tuple, or set; containing only dicts."
            ))
    params = {}
    for idx, val_dict in enumerate(values):
        # Build the final output.
        params.update({
            '{param}{idx}.{key}'.format(param=param, idx=idx+1, key=k): v
            for k, v in val_dict.items()
        })
    return params


def dict_keyed_param(param, dict_from):
    """
    Given a param string and a dict, returns a flat dict of keyed params without enumerate.
    Example:
        param = "ShipmentRequestDetails.PackageDimensions"
        dict_from = {'Length': 5, 'Width': 5, 'Height': 5, 'Unit': 'inches'}
    Returns:
        {
            'ShipmentRequestDetails.PackageDimensions.Length': 5,
            'ShipmentRequestDetails.PackageDimensions.Width': 5,
            'ShipmentRequestDetails.PackageDimensions.Height': 5,
            'ShipmentRequestDetails.PackageDimensions.Unit': 'inches',
            ...
        }
    """
    params = {}

    if not param.endswith('.'):
        # Ensure the enumerated param ends in '.'
        param += '.'
    for k, v in dict_from.items():
        params.update({
            "{param}{key}".format(param=param, key=k): v
        })
    return params


def unique_list_order_preserved(seq):
    """
    Returns a unique list of items from the sequence
    while preserving original ordering.
    The first occurence of an item is returned in the new sequence:
    any subsequent occurrences of the same item are ignored.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_utc_timestamp():
    """
    Returns the current UTC timestamp in ISO-8601 format.
    """
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()


class DotDict:
    """
    A read-only dict like class for navigating a JSON-like object.

    x = DotDict(xmltodict(apiresponse))
    accessing values:
    using attribute notation:
        position_in_list = 0
        x.key1.nestedkey2[position_in_list]
    standard subscriptable like: dict['key'] or list[0]
    implemented a get(key, default) function , you can use like:
    x.RequestReportResult.get('ReportRequestInfo', 'alt1').EndDate
    """

    def __init__(self, mapping):
        """
        Instantiate a copy of the passed dictionary from xmltodict.
        """
        self.__data = mapping

    def __getattr__(self, name):
        """
        Run if no attribute has the same name.

        Example when not: DotDict(obj).get()
        """
        if hasattr(self.__data, name):
            # Looks for data attributes like dict.keys()
            return getattr(self.__data, name)
        else:
            # pyhon 2 fix
            if name == '__nonzero__':
                return None
            # it's not an attribute, so use it as a key for the data
            return DotDict.build(self.__data[name])

    def __getitem__(self, key):
        """
        Allow subscription like: dict['key'].
        """
        assert isinstance(self.__data, Mapping) is True
        return DotDict.build(self.__data[key])

    def __repr__(self):
        return str(self.__dict__['_DotDict__data'])

    def __str__(self):
        """
        Pprint is standard printout.
        """
        return pprint.pformat(self.__dict__['_DotDict__data'])

    def get(self, key, default=None):
        """
        Use it like the dictionary get method.
        """
        try:
            assert isinstance(self.__data, Mapping) is True
            return DotDict.build(self.__data[key])
        except KeyError:
            return default

    @classmethod
    def build(cls, obj):
        """
        Fetch objects. A constructor providing the main functionality.
        """
        if isinstance(obj, Mapping):
            return cls(obj)  # Build a DotDict object
        elif isinstance(obj, MutableSequence):
            # The dict is from xmltodict, so a MutableSequence must be a list
            return [cls.build(item) for item in obj]
        else:  # If it's not a list or a dict return the item as it is
            return obj
