"""
Tests for the MWS.Inventory API class.
"""
import unittest
import datetime
import mws
from .utils import CommonRequestTestTools


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
        now_timestamp = now.isoformat()
        skus = ['thing1', 'thing2']
        response_group = 'Detailed'
        params = self.api.list_inventory_supply(skus, now, response_group=response_group)
        self.assert_common_params(params)
        assert params['Action'] == 'ListInventorySupply'
        assert params['QueryStartDateTime'] == now_timestamp
        assert params['ResponseGroup'] == 'Detailed'
        assert params['SellerSkus.member.1'] == 'thing1'
        assert params['SellerSkus.member.2'] == 'thing2'

    def test_list_inventory_supply_by_next_token(self):
        """
        ListInventorySupplyByNextToken operation
        """
        next_token = 'token_foobar'
        params = self.api.list_inventory_supply(next_token=next_token)
        self.assert_common_params(params)
        assert params['Action'] == 'ListInventorySupplyByNextToken'
        assert params['NextToken'] == next_token

    def test_list_inventory_supply_by_next_token_alias(self):
        """
        ListInventorySupplyByNextToken operation by way of the alias method
        list_inventory_supply_by_next_token
        """
        next_token = 'token_foobar'
        params = self.api.list_inventory_supply_by_next_token(next_token)
        self.assert_common_params(params)
        assert params['Action'] == 'ListInventorySupplyByNextToken'
        assert params['NextToken'] == next_token
