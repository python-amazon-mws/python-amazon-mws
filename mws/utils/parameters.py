"""Parameter manipulation utilities."""

from collections.abc import Iterable
from urllib.parse import quote
import datetime
import json

from mws.errors import MWSError


def enumerate_param(param, values):
    """Builds a dictionary of an enumerated parameter, using the param string and some values.
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
    if not isinstance(values, (list, tuple, set)):
        # Coerces a single value to a list before continuing.
        values = [values]
    if not any(values):
        # if not values -> returns ValueError
        return {}
    if not param.endswith("."):
        # Ensure this enumerated param ends in '.'
        param += "."
    # Return final output: dict comprehension of the enumerated param and values.
    return {"{}{}".format(param, idx + 1): val for idx, val in enumerate(values)}


def enumerate_params(params=None):
    """For each param and values, runs enumerate_param,
    returning a flat dict of all results
    """
    if params is None or not isinstance(params, dict):
        return {}
    params_output = {}
    for param, values in params.items():
        params_output.update(enumerate_param(param, values))
    return params_output


def enumerate_keyed_param(param, values):
    """Given a param string and a dict of values, returns a flat dict of keyed, enumerated params.
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
    if not isinstance(values, (list, tuple, set)):
        # If it's a single value, convert it to a list first
        values = [values]
    if not any(values):
        # Shortcut for empty values
        return {}
    if not param.endswith("."):
        # Ensure the enumerated param ends in '.'
        param += "."
    for val in values:
        # Every value in the list must be a dict.
        if not isinstance(val, dict):
            # Value is not a dict: can't work on it here.
            raise ValueError(
                (
                    "Non-dict value detected. "
                    "`values` must be a list, tuple, or set; containing only dicts."
                )
            )
    params = {}
    for idx, val_dict in enumerate(values):
        # Build the final output.
        params.update(
            {
                "{param}{idx}.{key}".format(param=param, idx=idx + 1, key=k): v
                for k, v in val_dict.items()
            }
        )
    return params


def dict_keyed_param(param, dict_from):
    """Given a param string and a dict, returns a flat dict of keyed params without enumerate.

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

    if not param.endswith("."):
        # Ensure the enumerated param ends in '.'
        param += "."
    for k, v in dict_from.items():
        params.update({"{param}{key}".format(param=param, key=k): v})
    return params


def clean_param_value(val):
    """Attempts to clean a value so that it can be sent in a request."""
    if isinstance(val, (dict, list, set, tuple)):
        raise ValueError("Cannot clean parameter value of type %s" % str(type(val)))

    if isinstance(val, (datetime.datetime, datetime.date)):
        return clean_date(val)
    if isinstance(val, bool):
        return clean_bool(val)

    # For all else, assume a string, and clean that.
    return clean_string(str(val))


def clean_string(val):
    """Passes a string value through `urllib.parse.quote` to clean it.

    Safe characters permitted: -_.~
    """
    return quote(val, safe="-_.~")


def clean_bool(val):
    """Converts a boolean value to its JSON string equivalent."""
    if val is not True and val is not False:
        raise ValueError("Expected a boolean, got %s" % val)
    return json.dumps(val)


def clean_date(val):
    """Converts a datetime.datetime or datetime.date to ISO 8601 string.
    Further passes that string through `urllib.parse.quote`.
    """
    return clean_string(val.isoformat())


class RequestParameter:
    """An MWS request parameter, defined by a `key` string and a `value`.

    Using this object with its `to_dict` method, any arbitrarily-nested list or dict
    in `value` will be expanded and flattened, such that each key in a sub-dict is
    concatenated to `key` as a dotted string; and each element in a list is
    enumerated (starting from 1) and concatenated to `key`, also as a dotted string.

    Example:
        value = {
            "a": 1,
            "b": "hello",
            "c": [
                "foo",
                "bar",
                {
                    "what": "have",
                    "you": [
                        5,
                        6,
                        7,
                    ],
                },
            ],
        }
        print(RequestParameter(key="example", value=value).to_dict())
        # Formatted for readability:
        >>> {
            "example.a": 1,
            "example.b": "hello",
            "example.c.1": "foo",
            "example.c.2": "bar",
            "example.c.3.what": "have",
            "example.c.3.you.1": 5,
            "example.c.3.you.2": 6,
            "example.c.3.you.3": 7,
        }

    - The parameter key "example" is placed in front of each new key.
      - An empty `key` can also be used when `value` is a nested object:
        `RequestParameter(value=value)`.
        This will output the same as above, without `example.` in front of each key.
      - When using an empty `key`, having a `value` that is not a dict and
        not a non-string iterable raises ValueError
    - "a" and "b" are simple values, and are returned.
    - "c" contains an iterable (list), which is enumerated with a 1-based index.
      These are joined to "c" with ".", creating keys "c.1" and "c.2".
    - At "c.3", another nested object is located. This is passed recursively to a new
      `RequestParameter`, and the same process repeats (dicts are keyed, iterables
      are enumerated with 1-based index, and simple values are returned).
    - The same occurs for "c.3.you", where an iterable is found and is enumerated.
    - The final output should always be a flat dictionary with key-value pairs.

    The output of `to_dict` is used within the `to_str` method to create a single
    string value from all key-value pairs (keys and values joined by "=",
    and pairs joined by "&").
    """

    def __init__(self, key=None, value=None):
        self.key = key
        self.value = value
        self._validate()

    def _validate(self):
        if self.key:
            return
        # No key provided. All recursive methods provide keys, so the user set this.
        if not self._value_is_dict() and not self._value_is_iterable():
            raise ValueError(
                "Parameter with empty `key` must have a dict or iterable `value`."
            )

    def _value_is_str(self):
        """Return bool, whether the value is a string.

        Used solely in the `_value_is_iterable` test.
        """
        return isinstance(self.value, str)

    def _value_is_dict(self):
        """Return bool, whether the value is a dict."""
        return isinstance(self.value, dict)

    def _value_is_iterable(self):
        """Return bool, whether the value is a "psuedo-iterable".

        As a special case, returns False if the value is a dict or str,
        because we want to treat those objects differently.
        """
        if self._value_is_dict() or self._value_is_str():
            return False
        return isinstance(self.value, Iterable)

    def to_dict(self):
        """Return a flat dict, 1 level deep, by enumerating or keying nested
        lists and dicts in `self.value`.
        """
        if self.value is None:
            # Returns nothing for a `None` value
            return {}
        if self._value_is_dict():
            return self.keyed_value()
        if self._value_is_iterable():
            return self.enumerated_value()
        return {self.key: self.value}

    def to_str(self):
        """Converts the output of `to_dict` to a string.

        Each key-value pair in the flattened dict is output as "key=val",
        and all pairs are joined by "&".
        """
        content = self.to_dict()
        output = []
        for key, val in content.items():
            output.append("{}={}".format(key, val))
        return "&".join(output)

    @property
    def param_key(self):
        """Outputs the key to use when outputting nested parameters.

        If the key is not set, returns an empty string.
        Otherwise returns the key string, ensuring there is a "." appended to it.
        """
        param = ""
        if self.key:
            param = self.key
            if not param.endswith("."):
                param += "."
        return param

    def keyed_value(self):
        """Returns a flat dict for a nested dict `value`.

        For each `sub_key`/`sub_val` pair of the `value` dict,
        `sub_key` is combined with this parameter's `key` and "." to create a new key.

        This new key and `sub_val` are then passed to a new `RequestParameter` object,
        where the output of that sub-parameter's `to_dict()` method is recursively
        added back to the return value dictionary here.
        """
        if not self._value_is_dict():
            raise ValueError("Cannot generate keyed value for non-dict `value`.")
        output = {}
        for sub_key, val in self.value.items():
            new_key = "{}{}".format(self.param_key, sub_key)
            # Update our output with the dict from a nested parameter
            # using this new key and value.
            output.update(RequestParameter(key=new_key, value=val).to_dict())
        return output

    def enumerated_value(self):
        """Returns a flat dict for a nested iterable `value` (similar to `keyed_value`).

        Each element of the `value` iterable is enumerated with a 1-based index `idx`.
        `idx` is then joined to `key` with "." to obtain a new key.

        From there, the same recursive methodology as `keyed_value` is used,
        generating a sub-parameter and dict output that is added back
        to the return value dictionary.
        """
        if not self._value_is_iterable():
            raise ValueError(
                "Cannot generate enumerated value for non-iterable `value`."
            )
        output = {}
        for idx, val in enumerate(self.value):
            new_key = "{}{}".format(self.param_key, idx + 1)
            # Update our output with the dict from a nested parameter
            # using this new key and value.
            output.update(RequestParameter(key=new_key, value=val).to_dict())
        return output
