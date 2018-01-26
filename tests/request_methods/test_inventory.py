import unittest
import datetime
import mws
from .utils import clean_redundant_params


class InventoryTestCase(unittest.TestCase):
    def setUp(self):
        credentials = ['access', 'secret', 'account']
        self.api = mws.Inventory(*credentials)
        self.api._test_request_params = True

    def test_service_status(self):
        response = self.api.get_service_status()
        response = clean_redundant_params(response)
        expected = {
            'Action': 'GetServiceStatus',
            'Version': '2010-10-01',
        }
        assert response == expected

    def test_list_inventory_supply(self):
        now = datetime.datetime.utcnow()
        now_timestamp = now.isoformat()
        skus = ['thing1', 'thing2']
        response_group = 'Detailed'
        response = self.api.list_inventory_supply(skus, now, response_group=response_group)
        response = clean_redundant_params(response)

        expected = {
            'Action': 'ListInventorySupply',
            'QueryStartDateTime': now_timestamp,
            'ResponseGroup': 'Detailed',
            'SellerSkus.member.1': 'thing1',
            'SellerSkus.member.2': 'thing2',
            'Version': '2010-10-01',
        }
        assert response == expected

    def test_list_inventory_supply_by_next_token(self):
        next_token = 'token_foobar'
        response = self.api.list_inventory_supply(next_token=next_token)
        response = clean_redundant_params(response)
        expected = {
            'Action': 'ListInventorySupplyByNextToken',
            'NextToken': next_token,
            'Version': '2010-10-01',
        }
        assert response == expected
