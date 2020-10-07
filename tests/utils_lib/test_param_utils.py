"""Testing for param utilities."""

import pytest

from mws.utils.params import enumerate_param
from mws.utils.params import enumerate_params
from mws.utils.params import enumerate_keyed_param
from mws.utils.params import dict_keyed_param
from mws.utils.params import flat_param_dict


def test_keyed_param_fails_without_dict():
    """Should raise ValueError for values not being a dict."""
    param = "something"
    values = ["this is not a dict like it should be!"]
    with pytest.raises(ValueError):
        enumerate_keyed_param(param, values)


def test_param_defaults_single():
    """Sending a param and an empty list == empty dict."""
    assert enumerate_param("something", []) == {}


def test_param_defaults_multi_empty():
    """Sending no params == empty dict."""
    assert enumerate_params() == {}


def test_param_defaults_multi_nondict():
    """Sending anything other than a dict containing the params == empty dict."""
    assert enumerate_params("antler") == {}


def test_param_defaults_keyed():
    # Sending a param with an empty list == empty dict
    # (The case for the list not empty and not containing dicts as expected
    # is handled by TestParamsRaiseExceptions)
    assert enumerate_keyed_param("acorn", []) == {}


def test_single_param_not_dotted_list_values():
    """A param string with no dot at the end and a list of ints.
    List should be ingested in order.
    """
    param = "SomethingOrOther"
    values = (123, 765, 3512, 756437, 3125)
    result = enumerate_param(param, values)
    expected = {
        "SomethingOrOther.1": 123,
        "SomethingOrOther.2": 765,
        "SomethingOrOther.3": 3512,
        "SomethingOrOther.4": 756437,
        "SomethingOrOther.5": 3125,
    }
    assert result == expected


def test_single_param_dotted_single_value():
    """A param string with a dot at the end and a single string value.
    Values that are not list, tuple, or set should coerce to a list
    and provide a single output.
    """
    param = "FooBar."
    values = "eleven"
    result = enumerate_param(param, values)
    expected = {
        "FooBar.1": "eleven",
    }
    assert result == expected


def test_multi_params():
    """A series of params sent as a list of dicts to enumerate_params.
    Each param should generate a unique set of keys and values.
    Final result should be a flat dict.
    """
    param1 = "Summat."
    values1 = ("colorful", "cheery", "turkey")
    param2 = "FooBaz.what"
    values2 = "singular"
    param3 = "hot_dog"
    values3 = ["something", "or", "other"]
    # We could test with values as a set, but we cannot be 100% of the order of the output,
    # and I don't feel it necessary to flesh this out enough to account for it.
    result = enumerate_params({param1: values1, param2: values2, param3: values3})
    expected = {
        "Summat.1": "colorful",
        "Summat.2": "cheery",
        "Summat.3": "turkey",
        "FooBaz.what.1": "singular",
        "hot_dog.1": "something",
        "hot_dog.2": "or",
        "hot_dog.3": "other",
    }
    assert result == expected


enum_key_items1 = [
    {"thing": "stuff", "foo": "baz"},
    {"thing": 123, "foo": 908, "bar": "hello"},
    {"stuff": "foobarbazmatazz", "stuff2": "foobarbazmatazz5"},
]
enum_key_expected1 = {
    "AthingToKeyUp.member.1.thing": "stuff",
    "AthingToKeyUp.member.1.foo": "baz",
    "AthingToKeyUp.member.2.thing": 123,
    "AthingToKeyUp.member.2.foo": 908,
    "AthingToKeyUp.member.2.bar": "hello",
    "AthingToKeyUp.member.3.stuff": "foobarbazmatazz",
    "AthingToKeyUp.member.3.stuff2": "foobarbazmatazz5",
}

enum_key_items2 = {"stuff": "foobarbazmatazz", "stuff2": "foobarbazmatazz5"}
enum_key_expected2 = {
    "AthingToKeyUp.member.1.stuff": "foobarbazmatazz",
    "AthingToKeyUp.member.1.stuff2": "foobarbazmatazz5",
}


### Parametrized tests for enumerate_keyed_param
# Should expect the same outputs whether the param ends in '.' or not.
@pytest.mark.parametrize("param", ("AthingToKeyUp.member", "AthingToKeyUp.member."))
@pytest.mark.parametrize(
    "items, expected",
    (
        (enum_key_items1, enum_key_expected1),
        (enum_key_items2, enum_key_expected2),
    ),
)
def test_enumerate_keyed_param(param, items, expected):
    """Asserting the result through enumerate_keyed_param is as expected."""
    result = enumerate_keyed_param(param, items)
    assert result == expected


def test_dict_keyed_param_not_dotted():
    """Testing results of dict_keyed_param, for param not dotted"""
    param = "ShipmentRequestDetails.PackageDimensions"
    dict_from = {"Length": 5, "Width": 5, "Height": 5, "Unit": "inches"}
    result = dict_keyed_param(param, dict_from)
    expected = {
        "ShipmentRequestDetails.PackageDimensions.Length": 5,
        "ShipmentRequestDetails.PackageDimensions.Width": 5,
        "ShipmentRequestDetails.PackageDimensions.Height": 5,
        "ShipmentRequestDetails.PackageDimensions.Unit": "inches",
    }
    assert result == expected


def test_dict_keyed_param_dotted():
    """Testing results of dict_keyed_param, for param not dotted"""
    param = "ShipmentRequestDetails.PackageDimensions."
    dict_from = {"Length": 5, "Width": 5, "Height": 5, "Unit": "inches"}
    result = dict_keyed_param(param, dict_from)
    expected = {
        "ShipmentRequestDetails.PackageDimensions.Length": 5,
        "ShipmentRequestDetails.PackageDimensions.Width": 5,
        "ShipmentRequestDetails.PackageDimensions.Height": 5,
        "ShipmentRequestDetails.PackageDimensions.Unit": "inches",
    }
    assert result == expected


def test_flat_param_dict():
    """Checks the output of `mws.utils.params.flat_param_dict`."""
    value = {
        "a": 1,
        "b": "hello",
        "c": ["foo", "bar", {"spam": "ham", "eggs": [5, 6, 7]}],
    }

    output = flat_param_dict(value)

    expected = {
        "a": 1,
        "b": "hello",
        "c.1": "foo",
        "c.2": "bar",
        "c.3.spam": "ham",
        "c.3.eggs.1": 5,
        "c.3.eggs.2": 6,
        "c.3.eggs.3": 7,
    }

    assert output == expected


def test_flat_param_dict_prefixed():
    """Checks the output of `mws.utils.params.flat_param_dict` with a prefix."""
    value = {
        "a": 1,
        "b": "hello",
        "c": ["foo", "bar", {"spam": "ham", "eggs": [5, 6, 7]}],
    }

    output = flat_param_dict(value, prefix="foobarbaz")

    expected = {
        "foobarbaz.a": 1,
        "foobarbaz.b": "hello",
        "foobarbaz.c.1": "foo",
        "foobarbaz.c.2": "bar",
        "foobarbaz.c.3.spam": "ham",
        "foobarbaz.c.3.eggs.1": 5,
        "foobarbaz.c.3.eggs.2": 6,
        "foobarbaz.c.3.eggs.3": 7,
    }

    assert output == expected


@pytest.mark.parametrize(
    "value, prefix",
    (
        ("spam", None),  # string value (which is excluded from checks for Iterables)
        ("spam", ""),  # also check the prefix empty string
        (5, None),  # basically any other value that isn't a dict or Iterable
        (5, ""),
    ),
)
def test_flat_param_dict_exceptions(value, prefix):
    """Check that certain inputs to `mws.utils.params.flat_param_dict`
    raise expected exceptions.
    """
    with pytest.raises(ValueError):
        flat_param_dict(value, prefix=prefix)
