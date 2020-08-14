"""
Tests for the MWS.Inventory API class.
"""
import unittest
import datetime
import mws
from mws.utils import clean_date

from .utils import CommonAPIRequestTools


class InventoryTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Inventory."""

    api_class = mws.Inventory

    def test_list_inventory_supply(self):
        """ListInventorySupply operation."""
        now = datetime.datetime.utcnow()
        skus = ["thing1", "thing2"]
        response_group = "Detailed"
        params = self.api.list_inventory_supply(
            skus, now, response_group=response_group
        )
        self.assert_common_params(params, action="ListInventorySupply")
        self.assertEqual(params["QueryStartDateTime"], clean_date(now))
        self.assertEqual(params["ResponseGroup"], "Detailed")
        self.assertEqual(params["SellerSkus.member.1"], "thing1")
        self.assertEqual(params["SellerSkus.member.2"], "thing2")

    def test_list_inventory_supply_by_next_token(self):
        """ListInventorySupplyByNextToken operation, using `next_token` argument."""
        next_token = "token_foobar"
        params = self.api.list_inventory_supply(next_token=next_token)
        self.assert_common_params(params, action="ListInventorySupplyByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_list_inventory_supply_by_next_token_alias(self):
        """ListInventorySupplyByNextToken operation, using alias method."""
        next_token = "token_foobar"
        params = self.api.list_inventory_supply_by_next_token(next_token)
        self.assert_common_params(params, action="ListInventorySupplyByNextToken")
        self.assertEqual(params["NextToken"], next_token)
