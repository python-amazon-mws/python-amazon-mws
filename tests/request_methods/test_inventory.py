"""
Tests for the MWS.Inventory API class.
"""
import unittest
import datetime
import mws
from .utils import CommonRequestTestTools, transform_date


class InventoryTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Inventory.
    """

    def setUp(self):
        self.api = mws.Inventory(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_list_inventory_supply(self):
        """
        ListInventorySupply operation
        """
        now = datetime.datetime.utcnow()
        skus = ['thing1', 'thing2']
        response_group = 'Detailed'
        params = self.api.list_inventory_supply(skus, now, response_group=response_group)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInventorySupply')
        self.assertEqual(params['QueryStartDateTime'], transform_date(now))
        self.assertEqual(params['ResponseGroup'], 'Detailed')
        self.assertEqual(params['SellerSkus.member.1'], 'thing1')
        self.assertEqual(params['SellerSkus.member.2'], 'thing2')

    def test_list_inventory_supply_by_next_token(self):
        """
        ListInventorySupplyByNextToken operation
        """
        next_token = 'token_foobar'
        params = self.api.list_inventory_supply(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInventorySupplyByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_inventory_supply_by_next_token_alias(self):
        """
        ListInventorySupplyByNextToken operation by way of the alias method
        list_inventory_supply_by_next_token
        """
        next_token = 'token_foobar'
        params = self.api.list_inventory_supply_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListInventorySupplyByNextToken')
        self.assertEqual(params['NextToken'], next_token)
