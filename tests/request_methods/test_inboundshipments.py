"""
Tests for the InboundShipments API class.
"""
import unittest
import mws
from mws.apis.inbound_shipments import parse_item_args
from mws.mws import MWSError
from .utils import CommonRequestTestTools


def test_parse_item_args()
class TestParseItemArgsExceptions(unittest.TestCase):
    """
    Test cases that ensure `parse_item_args` raises exceptions where appropriate.
    """
    def test_empty_args_list(self):
        """
        Should raise `MWSError` for an empty set of arguments.
        """
        item_args = []
        operation = 'dummy'
        with self.assertRaises(MWSError):
            parse_item_args(item_args, operation)

    def test_item_not_a_dict(self):
        """
        Should raise `MWSError` if item arguments are not all dict objects
        """
        item_args = ['this is not a dict']
        operation = 'dummy'
        with self.assertRaises(MWSError):
            parse_item_args(item_args, operation)

    def test_required_keys_missing_CreateInboundShipmentPlan(self):
        """
        Should raise `MWSError` if a required key is missing from at least one item dict
        for the CreateInboundShipmentPlan operation
        """
        operation = 'CreateInboundShipmentPlan'
        # SKU missing
        item_args_1 = [
            {
                'quantity': 34,
            },
        ]
        with self.assertRaises(MWSError):
            parse_item_args(item_args_1, operation)
        # Quantity missing
        item_args_2 = [
            {
                'sku': 'something',
            },
        ]
        with self.assertRaises(MWSError):
            parse_item_args(item_args_2, operation)

    def test_required_keys_missing_other_operation(self):
        """
        Should raise `MWSError` if a required key is missing from at least one item dict
        for operations other than CreateInboundShipmentPlan.
        """
        operation = 'other operation'
        # SKU missing
        item_args_1 = [
            {
                'quantity': 56,
            },
        ]
        with self.assertRaises(MWSError):
            parse_item_args(item_args_1, operation)
        # Quantity missing
        item_args_2 = [
            {
                'sku': 'soemthingelse',
            },
        ]
        with self.assertRaises(MWSError):
            parse_item_args(item_args_2, operation)

    def test_args_built_CreateInboundShipmentPlan(self):
        """
        Item args should build successfully for the CreateInboundShipmentPlan operation.
        """
        operation = 'CreateInboundShipmentPlan'
        # SKU missing
        item_args = [
            {
                'sku': 'somethingelse',
                'quantity': 56,
                'quantity_in_case': 12,
                'asin': 'ANYTHING',
                'condition': 'Used',
            },
            {
                'sku': 'something',
                'quantity': 34,
            },
        ]
        parsed_items = parse_item_args(item_args, operation)
        expected = [
            {
                'SellerSKU': 'somethingelse',
                'Quantity': 56,
                'QuantityInCase': 12,
                'ASIN': 'ANYTHING',
                'Condition': 'Used',
            },
            {
                'SellerSKU': 'something',
                'Quantity': 34,
                'QuantityInCase': None,
                'ASIN': None,
                'Condition': None,
            },
        ]
        self.assertEqual(parsed_items[0], expected[0])
        self.assertEqual(parsed_items[1], expected[1])

    def test_args_built_other_operation(self):
        """
        Item args should build successfully for operations other than CreateInboundShipmentPlan.
        """
        operation = 'other_operation'
        # SKU missing
        item_args = [
            {
                'sku': 'one_thing',
                'quantity': 34,
                'quantity_in_case': 5,
            },
            {
                'sku': 'the_other_thing',
                'quantity': 7,
            },
        ]
        parsed_items = parse_item_args(item_args, operation)
        expected = [
            {
                'SellerSKU': 'one_thing',
                'QuantityShipped': 34,
                'QuantityInCase': 5,
            },
            {
                'SellerSKU': 'the_other_thing',
                'QuantityShipped': 7,
                'QuantityInCase': None,
            },
        ]
        self.assertEqual(parsed_items[0], expected[0])
        self.assertEqual(parsed_items[1], expected[1])


class InboundShipmentsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for InboundShipments.
    """
    # TODO: Add remaining methods for InboundShipments
    def setUp(self):
        self.api = mws.InboundShipments(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
