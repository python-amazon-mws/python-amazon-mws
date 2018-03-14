"""
Tests for the InboundShipments API class.
"""
import unittest
import mws
from mws.apis.inbound_shipments import parse_item_args
from mws.mws import MWSError
from .utils import CommonRequestTestTools


class ParseItemArgsTestCase(unittest.TestCase):
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


class SetShipFromAddressTestCase(unittest.TestCase):
    """
    Test case covering msw.InboundShipments.set_ship_from_address
    """
    def setUp(self):
        self.inbound = mws.InboundShipments('', '', '')

    def test_address_empty_raises_exception(self):
        """
        Empty address dict should raise MWSError.
        """
        address = {}
        with self.assertRaises(MWSError):
            self.inbound.set_ship_from_address(address)

    def test_address_not_dict_raises_exception(self):
        """
        Non-dict argument should raise MWSError.
        """
        address = 'this is not a dict'
        with self.assertRaises(MWSError):
            self.inbound.set_ship_from_address(address)

    def test_required_keys_missing(self):
        """
        Any missing required key should raise MWSError
        """
        # Missing name
        address_1 = {
            'address_1': '500 Summat Cully Lane',
            'city': 'Gilead',
        }
        # Missing address_1 (address line 1)
        address_2 = {
            'name': 'Roland Deschain',
            'city': 'Gilead',
        }
        # Missing city
        address_3 = {
            'name': 'Roland Deschain',
            'address_1': '500 Summat Cully Lane',
        }
        with self.assertRaises(MWSError):
            self.inbound.set_ship_from_address(address_1)
        with self.assertRaises(MWSError):
            self.inbound.set_ship_from_address(address_2)
        with self.assertRaises(MWSError):
            self.inbound.set_ship_from_address(address_3)

    def test_full_address_built_properly(self):
        """
        An address with all fields covered should be contructed properly.
        """
        address = {
            'name': 'Roland Deschain',
            'address_1': '500 Summat Cully Lane',
            'address_2': 'Apartment 19',
            'city': 'Gilead',
            'district_or_county': 'West-Town',
            'state_or_province': 'New Canaan',
            'postal_code': '13019',
            'country': 'Mid-World',
        }
        self.inbound.set_ship_from_address(address)
        expected = {
            'ShipFromAddress.Name': 'Roland Deschain',
            'ShipFromAddress.AddressLine1': '500 Summat Cully Lane',
            'ShipFromAddress.AddressLine2': 'Apartment 19',
            'ShipFromAddress.City': 'Gilead',
            'ShipFromAddress.DistrictOrCounty': 'West-Town',
            'ShipFromAddress.StateOrProvinceCode': 'New Canaan',
            'ShipFromAddress.PostalCode': '13019',
            'ShipFromAddress.CountryCode': 'Mid-World',
        }
        self.assertEqual(self.inbound.from_address, expected)

    def test_partial_address_built_properly(self):
        """
        An address with only required fields covered should be contructed properly,
        with ommitted keys filled in with defaults.
        """
        address = {
            'name': 'Roland Deschain',
            'address_1': '500 Summat Cully Lane',
            'city': 'Gilead',
        }
        self.inbound.set_ship_from_address(address)
        expected = {
            'ShipFromAddress.Name': 'Roland Deschain',
            'ShipFromAddress.AddressLine1': '500 Summat Cully Lane',
            'ShipFromAddress.AddressLine2': None,
            'ShipFromAddress.City': 'Gilead',
            'ShipFromAddress.DistrictOrCounty': None,
            'ShipFromAddress.StateOrProvinceCode': None,
            'ShipFromAddress.PostalCode': None,
            'ShipFromAddress.CountryCode': 'US',
        }
        self.assertEqual(self.inbound.from_address, expected)

    def test_set_address_with_constructor(self):
        """
        An address passed to the InboundShipments constructor as a `from_address` kwarg
        should automatically set the `from_address` attribute accordingly.
        (Ignoring the self.inbound attribute in this case.)
        """
        address = {
            'name': 'Roland Deschain',
            'address_1': '500 Summat Cully Lane',
            'city': 'Gilead',
        }
        inbound = mws.InboundShipments('', '', '', from_address=address)
        expected = {
            'ShipFromAddress.Name': 'Roland Deschain',
            'ShipFromAddress.AddressLine1': '500 Summat Cully Lane',
            'ShipFromAddress.AddressLine2': None,
            'ShipFromAddress.City': 'Gilead',
            'ShipFromAddress.DistrictOrCounty': None,
            'ShipFromAddress.StateOrProvinceCode': None,
            'ShipFromAddress.PostalCode': None,
            'ShipFromAddress.CountryCode': 'US',
        }
        self.assertEqual(inbound.from_address, expected)


class InboundShipmentsRequestsTestCase(unittest.TestCase, CommonRequestTestTools):
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
