"""
Tests for the InboundShipments API class.
"""
import datetime
import unittest
import mws
from mws.apis.inbound_shipments import parse_item_args
from mws.mws import MWSError
from .utils import CommonRequestTestTools, transform_date, transform_bool
from .utils import transform_string


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
        inbound_constructed = mws.InboundShipments('', '', '', from_address=address)
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
        self.assertEqual(inbound_constructed.from_address, expected)


class FBAShipmentHandlingTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for InboundShipments involving FBA shipment handling.
    These cases require `from_address` to be set, while others do not.
    """

    def setUp(self):
        self.addr = {
            'name': 'Roland Deschain',
            'address_1': '500 Summat Cully Lane',
            'city': 'Gilead',
            'country': 'Mid-World',
        }
        self.api = mws.InboundShipments(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN,
            from_address=self.addr,
        )
        self.api._test_request_params = True

    def test_create_inbound_shipment_plan_exceptions(self):
        """
        Covers cases that should raise exceptions for the `create_inbound_shipment_plan` method.
        """
        # 1: `items` empty: raises MWSError
        items = []
        with self.assertRaises(MWSError):
            self.api.create_inbound_shipment_plan(items)
        # Set items to proper input
        items = [{'sku': 'something', 'quantity': 6}]

        # 2: wipe out the `from_address` for the API class before calling: raises MWSError
        self.api.from_address = None
        with self.assertRaises(MWSError):
            self.api.create_inbound_shipment_plan(items)

    def test_create_inbound_shipment_plan(self):
        """
        Covers successful data entry for `create_inbound_shipment_plan`.
        """
        items = [
            {'sku': 'ievEKnILd3', 'quantity': 6},
            {'sku': '9IfTM1aJVG', 'quantity': 26},
        ]
        country_code = 'Risa'
        subdivision_code = 'Hotel California'
        label_preference = 'SELLER'
        params = self.api.create_inbound_shipment_plan(
            items=items,
            country_code=country_code,
            subdivision_code=subdivision_code,
            label_preference=label_preference,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'CreateInboundShipmentPlan')
        self.assertEqual(params['ShipToCountryCode'], country_code)
        self.assertEqual(params['ShipToCountrySubdivisionCode'], transform_string(subdivision_code))
        self.assertEqual(params['LabelPrepPreference'], label_preference)
        # from_address expanded
        self.assertEqual(params['ShipFromAddress.Name'], transform_string(self.addr['name']))
        self.assertEqual(params['ShipFromAddress.AddressLine1'],
                         transform_string(self.addr['address_1']))
        self.assertEqual(params['ShipFromAddress.City'], transform_string(self.addr['city']))
        self.assertEqual(params['ShipFromAddress.CountryCode'],
                         transform_string(self.addr['country']))
        # item data
        self.assertEqual(
            params['InboundShipmentPlanRequestItems.member.1.SellerSKU'], items[0]['sku'])
        self.assertEqual(
            params['InboundShipmentPlanRequestItems.member.1.Quantity'], str(items[0]['quantity']))
        self.assertEqual(
            params['InboundShipmentPlanRequestItems.member.2.SellerSKU'], items[1]['sku'])
        self.assertEqual(
            params['InboundShipmentPlanRequestItems.member.2.Quantity'], str(items[1]['quantity']))

    def test_create_inbound_shipment_exceptions(self):
        """
        Covers cases that should raise exceptions for the `create_inbound_shipment` method.
        """
        # Proper inputs (initial setup)
        shipment_id = 'is_a_string'
        shipment_name = 'is_a_string'
        destination = 'is_a_string'
        items = [{'sku': 'something', 'quantity': 6}]

        # 1: `shipment_id` not a string: raises AssertionError
        shipment_id = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.create_inbound_shipment(shipment_id, shipment_name, destination, items)
        shipment_id = 'is_a_string'  # reset

        # 2: `shipment_name` not a string: raises AssertionError
        shipment_name = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.create_inbound_shipment(shipment_id, shipment_name, destination, items)
        shipment_name = 'is_a_string'  # reset

        # 3: `destination` not a string: raises AssertionError
        destination = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.create_inbound_shipment(shipment_id, shipment_name, destination, items)
        destination = 'is_a_string'  # reset

        # 4: `items` empty: raises MWSError
        items = []
        with self.assertRaises(MWSError):
            self.api.create_inbound_shipment(shipment_id, shipment_name, destination, items)
        items = [{'sku': 'something', 'quantity': 6}]  # reset

        # 5: wipe out the `from_address` for the API class before calling: raises MWSError
        self.api.from_address = None
        with self.assertRaises(MWSError):
            self.api.create_inbound_shipment(shipment_id, shipment_name, destination, items)

    def test_create_inbound_shipment(self):
        """
        Covers successful data entry for `create_inbound_shipment`.
        """
        shipment_id = 'b46sEL7sYX'
        shipment_name = 'Stuff Going Places'
        destination = 'Nibiru'
        items = [
            {'sku': 'GtLIws1bRX', 'quantity': 12},
            {'sku': 'vxXN61TIEI', 'quantity': 35},
        ]
        shipment_status = 'RECEIVED'
        label_preference = 'AMAZON'
        case_required = True
        box_contents_source = 'Boxes'
        params = self.api.create_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'CreateInboundShipment')
        self.assertEqual(params['ShipmentId'], shipment_id)
        self.assertEqual(params['InboundShipmentHeader.ShipmentName'],
                         transform_string(shipment_name))
        self.assertEqual(
            params['InboundShipmentHeader.DestinationFulfillmentCenterId'], destination)
        self.assertEqual(params['InboundShipmentHeader.LabelPrepPreference'], label_preference)
        self.assertEqual(params['InboundShipmentHeader.AreCasesRequired'],
                         transform_bool(case_required))
        self.assertEqual(params['InboundShipmentHeader.ShipmentStatus'], shipment_status)
        self.assertEqual(
            params['InboundShipmentHeader.IntendedBoxContentsSource'], box_contents_source)
        # from_address
        self.assertEqual(params['InboundShipmentHeader.ShipFromAddress.Name'],
                         transform_string(self.addr['name']))
        self.assertEqual(
            params['InboundShipmentHeader.ShipFromAddress.AddressLine1'],
            transform_string(self.addr['address_1']))
        self.assertEqual(
            params['InboundShipmentHeader.ShipFromAddress.City'],
            transform_string(self.addr['city']))
        self.assertEqual(
            params['InboundShipmentHeader.ShipFromAddress.CountryCode'],
            transform_string(self.addr['country']))
        # item data
        self.assertEqual(params['InboundShipmentItems.member.1.SellerSKU'], items[0]['sku'])
        self.assertEqual(
            params['InboundShipmentItems.member.1.QuantityShipped'], str(items[0]['quantity']))
        self.assertEqual(params['InboundShipmentItems.member.2.SellerSKU'], items[1]['sku'])
        self.assertEqual(
            params['InboundShipmentItems.member.2.QuantityShipped'], str(items[1]['quantity']))

    def test_update_inbound_shipment_exceptions(self):
        """
        Covers cases that should raise exceptions for the `update_inbound_shipment` method.
        """
        # Proper inputs (initial setup)
        shipment_id = 'is_a_string'
        shipment_name = 'is_a_string'
        destination = 'is_a_string'

        # 1: `shipment_id` not a string: raises AssertionError
        shipment_id = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.update_inbound_shipment(shipment_id, shipment_name, destination)
        shipment_id = 'is_a_string'  # reset

        # 2: `shipment_name` not a string: raises AssertionError
        shipment_name = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.update_inbound_shipment(shipment_id, shipment_name, destination)
        shipment_name = 'is_a_string'  # reset

        # 3: `destination` not a string: raises AssertionError
        destination = {'not': 'a string'}
        with self.assertRaises(AssertionError):
            self.api.update_inbound_shipment(shipment_id, shipment_name, destination)
        destination = 'is_a_string'  # reset

        # 4: wipe out the `from_address` for the API class before calling: raises MWSError
        self.api.from_address = None
        with self.assertRaises(MWSError):
            self.api.update_inbound_shipment(shipment_id, shipment_name, destination)

    def test_update_inbound_shipment(self):
        """
        Covers successful data entry for `update_inbound_shipment`.
        """
        shipment_id = '7DzXpBVxRR'
        shipment_name = 'Stuff Going Places'
        destination = 'Vulcan'
        items = [
            {'sku': 'PwJmnJj3SK', 'quantity': 98},
            {'sku': 'ebzf3HhssN', 'quantity': 65},
        ]
        shipment_status = 'WORKING'
        label_preference = 'SELLER_LABEL'
        case_required = True
        box_contents_source = 'Boxes'
        params_1 = self.api.update_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'UpdateInboundShipment')
        self.assertEqual(params_1['ShipmentId'], shipment_id)
        self.assertEqual(params_1['InboundShipmentHeader.ShipmentName'],
                         transform_string(shipment_name))
        self.assertEqual(
            params_1['InboundShipmentHeader.DestinationFulfillmentCenterId'], destination)
        self.assertEqual(params_1['InboundShipmentHeader.LabelPrepPreference'], label_preference)
        self.assertEqual(params_1['InboundShipmentHeader.AreCasesRequired'],
                         transform_bool(case_required))
        self.assertEqual(params_1['InboundShipmentHeader.ShipmentStatus'], shipment_status)
        self.assertEqual(
            params_1['InboundShipmentHeader.IntendedBoxContentsSource'], box_contents_source)
        # from_address
        self.assertEqual(
            params_1['InboundShipmentHeader.ShipFromAddress.Name'],
            transform_string(self.addr['name']))
        self.assertEqual(
            params_1['InboundShipmentHeader.ShipFromAddress.AddressLine1'],
            transform_string(self.addr['address_1']))
        self.assertEqual(
            params_1['InboundShipmentHeader.ShipFromAddress.City'],
            transform_string(self.addr['city']))
        self.assertEqual(
            params_1['InboundShipmentHeader.ShipFromAddress.CountryCode'], self.addr['country'])
        # item data
        self.assertEqual(params_1['InboundShipmentItems.member.1.SellerSKU'], items[0]['sku'])
        self.assertEqual(
            params_1['InboundShipmentItems.member.1.QuantityShipped'], str(items[0]['quantity']))
        self.assertEqual(params_1['InboundShipmentItems.member.2.SellerSKU'], items[1]['sku'])
        self.assertEqual(
            params_1['InboundShipmentItems.member.2.QuantityShipped'], str(items[1]['quantity']))
        # Additional case: no items required. Params should have no Items keys if not provided
        params_2 = self.api.update_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_2['Action'], 'UpdateInboundShipment')
        self.assertEqual(params_2['ShipmentId'], shipment_id)
        self.assertEqual(params_2['InboundShipmentHeader.ShipmentName'],
                         transform_string(shipment_name))
        self.assertEqual(
            params_2['InboundShipmentHeader.DestinationFulfillmentCenterId'], destination)
        self.assertEqual(params_2['InboundShipmentHeader.LabelPrepPreference'], label_preference)
        self.assertEqual(params_2['InboundShipmentHeader.AreCasesRequired'],
                         transform_bool(case_required))
        self.assertEqual(params_2['InboundShipmentHeader.ShipmentStatus'], shipment_status)
        self.assertEqual(
            params_2['InboundShipmentHeader.IntendedBoxContentsSource'], box_contents_source)
        # from_address
        self.assertEqual(params_2['InboundShipmentHeader.ShipFromAddress.Name'],
                         transform_string(self.addr['name']))
        self.assertEqual(
            params_2['InboundShipmentHeader.ShipFromAddress.AddressLine1'],
            transform_string(self.addr['address_1']))
        self.assertEqual(params_2['InboundShipmentHeader.ShipFromAddress.City'],
                         transform_string(self.addr['city']))
        self.assertEqual(
            params_2['InboundShipmentHeader.ShipFromAddress.CountryCode'], self.addr['country'])
        # items keys should not be present
        param_item_keys = [x for x in params_2.keys() if x.startswith('InboundShipmentItems')]
        # list should be empty, because no keys should be present
        self.assertFalse(param_item_keys)


class InboundShipmentsRequestsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for InboundShipments requests that do not involve FBA shipment handling
    and do not require `from_address` to be set.
    """

    def setUp(self):
        self.api = mws.InboundShipments(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_get_inbound_guidance_for_sku(self):
        """
        GetInboundGuidanceForSKU operation.
        """
        marketplace_id = 'eyuMuohmyP'
        # Case 1: list of SKUs
        sku_list_1 = [
            '5PWmAy4u1A',
            'CtwNnGX08l',
        ]
        params_1 = self.api.get_inbound_guidance_for_sku(
            skus=sku_list_1,
            marketplace_id=marketplace_id,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'GetInboundGuidanceForSKU')
        self.assertEqual(params_1['MarketplaceId'], marketplace_id)
        self.assertEqual(params_1['SellerSKUList.Id.1'], sku_list_1[0])
        self.assertEqual(params_1['SellerSKUList.Id.2'], sku_list_1[1])
        # Case 2: single SKU
        sku_list_2 = '9QWsksBUMI'
        params_2 = self.api.get_inbound_guidance_for_sku(
            skus=sku_list_2,
            marketplace_id=marketplace_id,
        )
        self.assert_common_params(params_2)
        self.assertEqual(params_2['Action'], 'GetInboundGuidanceForSKU')
        self.assertEqual(params_2['MarketplaceId'], marketplace_id)
        self.assertEqual(params_2['SellerSKUList.Id.1'], sku_list_2)

    def test_get_inbound_guidance_for_asin(self):
        """
        GetInboundGuidanceForASIN operation.
        """
        marketplace_id = 'osnufVjvfR'
        # Case 1: list of SKUs
        asin_list_1 = [
            'I2HCJMQ1sB',
            'EBDjm91glL',
        ]
        params_1 = self.api.get_inbound_guidance_for_asin(
            asins=asin_list_1,
            marketplace_id=marketplace_id,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'GetInboundGuidanceForASIN')
        self.assertEqual(params_1['MarketplaceId'], marketplace_id)
        self.assertEqual(params_1['ASINList.Id.1'], asin_list_1[0])
        self.assertEqual(params_1['ASINList.Id.2'], asin_list_1[1])
        # Case 2: single SKU
        asin_list_2 = 'FW2e9soodD'
        params_2 = self.api.get_inbound_guidance_for_asin(
            asins=asin_list_2,
            marketplace_id=marketplace_id,
        )
        self.assert_common_params(params_2)
        self.assertEqual(params_2['Action'], 'GetInboundGuidanceForASIN')
        self.assertEqual(params_2['MarketplaceId'], marketplace_id)
        self.assertEqual(params_2['ASINList.Id.1'], asin_list_2)

    def test_get_preorder_info(self):
        """
        GetPreorderInfo operation.
        """
        shipment_id = 'oYRjQbGLL6'
        params = self.api.get_preorder_info(shipment_id)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetPreorderInfo')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_confirm_preorder(self):
        """
        ConfirmPreorder operation.
        """
        shipment_id = 'H4UiUjY7Fr'
        need_by_date = datetime.datetime.utcnow()
        params = self.api.confirm_preorder(
            shipment_id=shipment_id,
            need_by_date=need_by_date,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ConfirmPreorder')
        self.assertEqual(params['ShipmentId'], shipment_id)
        self.assertEqual(params['NeedByDate'], transform_date(need_by_date))

    def test_get_prep_instructions_for_sku(self):
        """
        GetPrepInstructionsForSKU operation.
        """
        # Case 1: simple list
        skus_1 = [
            'ZITw0KqI3W',
            'qLijuY05j7',
        ]
        country_code = 'Wakanda'
        params_1 = self.api.get_prep_instructions_for_sku(
            skus=skus_1,
            country_code=country_code,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'GetPrepInstructionsForSKU')
        self.assertEqual(params_1['ShipToCountryCode'], country_code)
        self.assertEqual(params_1['SellerSKUList.ID.1'], skus_1[0])
        self.assertEqual(params_1['SellerSKUList.ID.2'], skus_1[1])
        # Case 2: duplicates should be removed before creating params,
        # with their ordering preserved.
        skus_2 = [
            'pvHENgh9GG',
            'yrFQfk66Ku',
            'pvHENgh9GG',  # duplicate should be removed in param build
            '3W2DgshBxW',
            'FBN4E7FK3S',
        ]
        params_2 = self.api.get_prep_instructions_for_sku(
            skus=skus_2,
            country_code=country_code,
        )
        self.assert_common_params(params_2)
        self.assertEqual(params_2['Action'], 'GetPrepInstructionsForSKU')
        self.assertEqual(params_2['ShipToCountryCode'], country_code)
        self.assertEqual(params_2['SellerSKUList.ID.1'], skus_2[0])
        self.assertEqual(params_2['SellerSKUList.ID.2'], skus_2[1])
        # skus_2[2] is a duplicate and should not be expected. skus_2[3] is next unique.
        self.assertEqual(params_2['SellerSKUList.ID.3'], skus_2[3])
        self.assertEqual(params_2['SellerSKUList.ID.4'], skus_2[4])

    def test_get_prep_instructions_for_asin(self):
        """
        GetPrepInstructionsForASIN operation.
        """
        # Case 1: simple list
        asins_1 = [
            'iTgHUxF1a7',
            '56gwMz7j1N',
        ]
        country_code = 'Wakanda'
        params_1 = self.api.get_prep_instructions_for_asin(
            asins=asins_1,
            country_code=country_code,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'GetPrepInstructionsForASIN')
        self.assertEqual(params_1['ShipToCountryCode'], country_code)
        self.assertEqual(params_1['ASINList.ID.1'], asins_1[0])
        self.assertEqual(params_1['ASINList.ID.2'], asins_1[1])
        # Case 2: duplicates should be removed before creating params,
        # with their ordering preserved.
        asins_2 = [
            'FCYeaVUYqY',
            'bma5ysgs8E',
            'IwyBQG9TgX',
            'IwyBQG9TgX',  # duplicate should be removed in param build
            'JPA8CyPAOF',
        ]
        params_2 = self.api.get_prep_instructions_for_asin(
            asins=asins_2,
            country_code=country_code,
        )
        self.assert_common_params(params_2)
        self.assertEqual(params_2['Action'], 'GetPrepInstructionsForASIN')
        self.assertEqual(params_2['ShipToCountryCode'], country_code)
        self.assertEqual(params_2['ASINList.ID.1'], asins_2[0])
        self.assertEqual(params_2['ASINList.ID.2'], asins_2[1])
        self.assertEqual(params_2['ASINList.ID.3'], asins_2[2])
        # asins_2[3] is a duplicate and should not be expected. asins_2[4] is next unique.
        self.assertEqual(params_2['ASINList.ID.4'], asins_2[4])

    # def test_put_transport_content(self):
    #     """
    #     PutTransportContent operation.
    #     """
    #     pass

    def test_estimate_transport_request(self):
        """
        EstimateTransportRequest operation.
        """
        shipment_id = 'w6ayzk2Aov'
        params = self.api.estimate_transport_request(shipment_id)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'EstimateTransportRequest')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_get_transport_content(self):
        """
        GetTransportContent operation.
        """
        shipment_id = 'w6ayzk2Aov'
        params = self.api.get_transport_content(shipment_id)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetTransportContent')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_confirm_transport_request(self):
        """
        ConfirmTransportRequest operation.
        """
        shipment_id = 'UTULruKM6v'
        params = self.api.confirm_transport_request(shipment_id)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ConfirmTransportRequest')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_void_transport_request(self):
        """
        VoidTransportRequest operation.
        """
        shipment_id = 'bJw9pyKcoB'
        params = self.api.void_transport_request(shipment_id)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'VoidTransportRequest')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_get_package_labels(self):
        """
        GetPackageLabels operation.
        """
        shipment_id = 'E7NBQ1O0Ca'
        num_labels = 53
        page_type = 'PackageLabel_Letter_6'
        params = self.api.get_package_labels(
            shipment_id=shipment_id,
            num_labels=num_labels,
            page_type=page_type,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetPackageLabels')
        self.assertEqual(params['ShipmentId'], shipment_id)
        self.assertEqual(params['PageType'], page_type)
        self.assertEqual(params['NumberOfPackages'], str(num_labels))

    def test_get_unique_package_labels(self):
        """
        GetUniquePackageLabels operation.
        """
        shipment_id = 'fMSw3SRJkC'
        page_type = 'PackageLabel_Plain_Paper'
        # Case 1: list of package_ids
        package_ids_1 = [
            'BuqFIFFY6d',
            'wU4NmZWEls',
        ]
        params_1 = self.api.get_unique_package_labels(
            shipment_id=shipment_id,
            page_type=page_type,
            package_ids=package_ids_1,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_1['Action'], 'GetUniquePackageLabels')
        self.assertEqual(params_1['ShipmentId'], shipment_id)
        self.assertEqual(params_1['PageType'], page_type)
        self.assertEqual(params_1['PackageLabelsToPrint.member.1'], package_ids_1[0])
        self.assertEqual(params_1['PackageLabelsToPrint.member.2'], package_ids_1[1])
        # Case 2: single string package_id (should still work)
        package_ids_2 = 'exGsKDTbyb'
        params_2 = self.api.get_unique_package_labels(
            shipment_id=shipment_id,
            page_type=page_type,
            package_ids=package_ids_2,
        )
        self.assert_common_params(params_1)
        self.assertEqual(params_2['Action'], 'GetUniquePackageLabels')
        self.assertEqual(params_2['ShipmentId'], shipment_id)
        self.assertEqual(params_2['PageType'], page_type)
        self.assertEqual(params_2['PackageLabelsToPrint.member.1'], package_ids_2)

    def test_get_pallet_labels(self):
        """
        XYZ operation.
        """
        shipment_id = 'Y3sROqkPfY'
        page_type = 'PackageLabel_A4_4'
        num_labels = 69
        params = self.api.get_pallet_labels(
            shipment_id=shipment_id,
            page_type=page_type,
            num_labels=num_labels,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetPalletLabels')
        self.assertEqual(params['ShipmentId'], shipment_id)
        self.assertEqual(params['PageType'], page_type)
        self.assertEqual(params['NumberOfPallets'], str(num_labels))

    def test_get_bill_of_lading(self):
        """
        GetBillOfLading operation.
        """
        shipment_id = 'nScOqC6Nh6'
        params = self.api.get_bill_of_lading(
            shipment_id=shipment_id,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetBillOfLading')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_list_inbound_shipments(self):
        """
        ListInboundShipments operation.
        """
        shipment_ids = [
            'Fp3kXnLQ72',
            'hAIO0W7VvF',
        ]
        shipment_statuses = [
            'CANCELLED',
            'IN_TRANSIT',
        ]
        last_updated_before = datetime.datetime.utcnow()
        last_updated_after = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.list_inbound_shipments(
            shipment_ids=shipment_ids,
            shipment_statuses=shipment_statuses,
            last_updated_before=last_updated_before,
            last_updated_after=last_updated_after,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipments')
        self.assertEqual(params['LastUpdatedBefore'], transform_date(last_updated_before))
        self.assertEqual(params['LastUpdatedAfter'], transform_date(last_updated_after))
        self.assertEqual(params['ShipmentStatusList.member.1'], shipment_statuses[0])
        self.assertEqual(params['ShipmentStatusList.member.2'], shipment_statuses[1])
        self.assertEqual(params['ShipmentIdList.member.1'], shipment_ids[0])
        self.assertEqual(params['ShipmentIdList.member.2'], shipment_ids[1])

    def test_list_inbound_shipments_by_next_token(self):
        """
        ListInboundShipmentsByNextToken operation, via method decorator.
        """
        next_token = 'rK10wZCE03'
        params = self.api.list_inbound_shipments(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipmentsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_inbound_shipments_by_next_token_alias(self):
        """
        ListInboundShipmentsByNextToken operation, via alias method.
        """
        next_token = 'AscnyUoyhj'
        params = self.api.list_inbound_shipments_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipmentsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_inbound_shipment_items(self):
        """
        ListInboundShipmentItems operation.
        """
        shipment_id = 'P9NLpC2Afi'
        last_updated_before = datetime.datetime.utcnow()
        last_updated_after = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.list_inbound_shipment_items(
            shipment_id=shipment_id,
            last_updated_before=last_updated_before,
            last_updated_after=last_updated_after,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipmentItems')
        self.assertEqual(params['ShipmentId'], shipment_id)
        self.assertEqual(params['LastUpdatedBefore'], transform_date(last_updated_before))
        self.assertEqual(params['LastUpdatedAfter'], transform_date(last_updated_after))

    def test_list_inbound_shipment_items_by_next_token(self):
        """
        ListInboundShipmentItemsByNextToken operation, via method decorator.
        """
        next_token = 'kjoslU1R4y'
        params = self.api.list_inbound_shipment_items(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipmentItemsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_inbound_shipment_items_by_next_token_alias(self):
        """
        ListInboundShipmentItemsByNextToken operation, via alias method.
        """
        next_token = 'p31dr3ceKQ'
        params = self.api.list_inbound_shipment_items_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInboundShipmentItemsByNextToken')
        self.assertEqual(params['NextToken'], next_token)
