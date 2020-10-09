"""Parameter manipulation utilities."""

from collections.abc import Iterable, Mapping
from urllib.parse import quote
import datetime
import json

# Removed top-level import to correct circular imports
# (we're in backport territory, these things happen)
# from mws.mws import MWSError


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
    param = dot_appended_param(param)
    # Return final output: dict comprehension of the enumerated param and values.
    return {"{}{}".format(param, idx): val for idx, val in enumerate(values, start=1)}


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
    """Given a param string and a list of values dicts, returns a flat dict of keyed, enumerated params.
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

    param = dot_appended_param(param)
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
    for idx, val_dict in enumerate(values, start=1):
        # Build the final output.
        params.update(
            {
                "{param}{idx}.{key}".format(param=param, idx=idx, key=k): v
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

    param = dot_appended_param(param)
    for k, v in dict_from.items():
        params.update({"{param}{key}".format(param=param, key=k): v})
    return params


def flat_param_dict(value, prefix=""):
    """Returns a flattened params dictionary by collapsing nested dicts and
    non-string iterables.
    Any arbitrarily-nested dict or iterable will be expanded and flattened.
    - Each key in a child dict will be concatenated to its parent key.
    - Elements of a non-string iterable will be enumerated using a 1-based index,
      with the index number concatenated to the parent key.
    - In both cases, keys and sub-keys are joined by ``.``.
    If ``prefix`` is set, all keys in the resulting output will begin with
    ``prefix + '.'``.
    """
    prefix = "" if not prefix else str(prefix)
    # Prefix is now either an empty string or a valid prefix string ending in '.'
    # NOTE should ensure that a `None` value is changed to empty string, as well.

    if isinstance(value, str) or not isinstance(value, (Mapping, Iterable)):
        # Value is not one of the types we want to expand.
        if prefix:
            # Can return a single dict of the prefix and value as a base case
            prefix = dot_appended_param(prefix, reverse=True)
            return {prefix: value}
        raise ValueError(
            (
                "Non-dict, non-iterable value requires a prefix "
                "(would return a mapping of `prefix: value`)"
            )
        )

    # Past here, the value is something that must be expanded.
    # We'll build that output with recursive calls to `flat_param_dict`.

    if prefix:
        prefix = dot_appended_param(prefix)

    output = {}
    if isinstance(value, Mapping):
        for key, val in value.items():
            new_key = "{}{}".format(prefix, key)
            output.update(flat_param_dict(val, prefix=new_key))
    else:
        # value must be an Iterable
        for idx, val in enumerate(value, start=1):
            new_key = "{}{}".format(prefix, idx)
            output.update(flat_param_dict(val, prefix=new_key))
    return output


def dot_appended_param(param_key, reverse=False):
    """Returns ``param_key`` string, ensuring that it ends with ``'.'``.
    Set ``reverse`` to ``True`` (default ``False``) to reverse this behavior,
    ensuring that ``param_key`` *does not* end with ``'.'``.
    """
    if not param_key.endswith("."):
        # Ensure this enumerated param ends in '.'
        param_key += "."
    if reverse:
        # Since param_key is guaranteed to end with '.' by this point,
        # if `reverse` flag was set, now we just get rid of it.
        param_key = param_key[:-1]
    return param_key


BOOL_FALSE_STRINGS = ("no", "n", "none", "off", "false", "0")


def coerce_to_bool(val):
    """Coerces ``val`` to a boolean for use in MWS requests.
    If ``val`` is a string, converts certain (case-insensitive) string values
    to "False", such as:
    - "no"
    - "n"
    - "none"
    - "off"
    - "false"
    - "0"
    Otherwise, ``val`` is simply cast using built-in ``bool()`` function.
    """
    if isinstance(val, str) and val.lower() in BOOL_FALSE_STRINGS:
        return False
    return bool(val)


def remove_empty_param_keys(params):
    """Returns a copy of ``params`` dict where any key with a value of ``None``
    or ``""`` (empty string) are removed.
    """
    return {k: v for k, v in params.items() if v is not None and v != ""}


def clean_params_dict(params):
    """Clean multiple param values in a dict, returning a new dict
    containing the original keys and cleaned values.
    """
    cleaned_params = dict()
    for key, val in params.items():
        try:
            cleaned_params[key] = clean_value(val)
        except ValueError as exc:
            from mws.mws import MWSError

            raise MWSError(str(exc)) from exc
    return cleaned_params


def clean_value(val):
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
