"""
Testing for enumerate_param, enumerate_params, and enumerate_keyed_param
"""
import unittest
import mws

# pylint: disable=invalid-name


class TestParamsRaiseExceptions(unittest.TestCase):
    """
    Simple test that asserts a ValueError is raised by an improper entry to
    `utils.enumerate_keyed_param`.
    """

    def test_keyed_param_fails_without_dict(self):
        """
        Should raise ValueError for values not being a dict.
        """
        param = "something"
        values = ["this is not a dict like it should be!"]
        with self.assertRaises(ValueError):
            mws.utils.enumerate_keyed_param(param, values)


def test_single_param_default():
    """
    Test each method type for their default empty dicts.
    """
    # Single
    assert mws.utils.enumerate_param("something", []) == {}
    # Multi
    assert mws.utils.enumerate_params() == {}
    assert mws.utils.enumerate_params("antler") == {}
    # Keyed
    assert mws.utils.enumerate_keyed_param("acorn", []) == {}


def test_single_param_not_dotted_list_values():
    """
    A param string with no dot at the end and a list of ints.
    List should be ingested in order.
    """
    param = "SomethingOrOther"
    values = (123, 765, 3512, 756437, 3125)
    result = mws.utils.enumerate_param(param, values)
    assert result == {
        "SomethingOrOther.1": 123,
        "SomethingOrOther.2": 765,
        "SomethingOrOther.3": 3512,
        "SomethingOrOther.4": 756437,
        "SomethingOrOther.5": 3125,
    }


def test_single_param_dotted_single_value():
    """
    A param string with a dot at the end and a single string value.
    Values that are not list, tuple, or set should coerce to a list and provide a single output.
    """
    param = "FooBar."
    values = "eleven"
    result = mws.utils.enumerate_param(param, values)
    assert result == {
        "FooBar.1": "eleven",
    }


def test_multi_params():
    """
    A series of params sent as a list of dicts to enumerate_params.
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
    result = mws.utils.enumerate_params(
        {
            param1: values1,
            param2: values2,
            param3: values3,
        }
    )
    assert result == {
        "Summat.1": "colorful",
        "Summat.2": "cheery",
        "Summat.3": "turkey",
        "FooBaz.what.1": "singular",
        "hot_dog.1": "something",
        "hot_dog.2": "or",
        "hot_dog.3": "other",
    }


def test_keyed_params():
    """
    Asserting the result through enumerate_keyed_param is as expected.
    """
    # Example:
    #     param = "InboundShipmentPlanRequestItems.member"
    #     values = [
    #         {'SellerSKU': 'Football2415',
    #         'Quantity': 3},
    #         {'SellerSKU': 'TeeballBall3251',
    #         'Quantity': 5},
    #         ...
    #     ]

    # Returns:
    #     {
    #         'InboundShipmentPlanRequestItems.member.1.SellerSKU': 'Football2415',
    #         'InboundShipmentPlanRequestItems.member.1.Quantity': 3,
    #         'InboundShipmentPlanRequestItems.member.2.SellerSKU': 'TeeballBall3251',
    #         'InboundShipmentPlanRequestItems.member.2.Quantity': 5,
    #         ...
    #     }
    param = "AthingToKeyUp.member"
    item1 = {
        "thing": "stuff",
        "foo": "baz",
    }
    item2 = {
        "thing": 123,
        "foo": 908,
        "bar": "hello",
    }
    item3 = {
        "stuff": "foobarbazmatazz",
        "stuff2": "foobarbazmatazz5",
    }
    result = mws.utils.enumerate_keyed_param(param, [item1, item2, item3])
    assert result == {
        "AthingToKeyUp.member.1.thing": "stuff",
        "AthingToKeyUp.member.1.foo": "baz",
        "AthingToKeyUp.member.2.thing": 123,
        "AthingToKeyUp.member.2.foo": 908,
        "AthingToKeyUp.member.2.bar": "hello",
        "AthingToKeyUp.member.3.stuff": "foobarbazmatazz",
        "AthingToKeyUp.member.3.stuff2": "foobarbazmatazz5",
    }
