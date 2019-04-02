"""
Amazon MWS Inventory Fulfillment API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action


class Inventory(MWS):
    """
    Amazon MWS Inventory Fulfillment API

    Docs:
    http://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_Overview.html
    """
    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInventory/2010-10-01}"
    NEXT_TOKEN_OPERATIONS = [
        'ListInventorySupply',
    ]

    @next_token_action('ListInventorySupply')
    def list_inventory_supply(self, skus=(), datetime_=None,
                              response_group='Basic', next_token=None, marketplace_id=None):
        """
        Returns information on available inventory

        Pass `next_token` to call "ListInventorySupplyByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_ListInventorySupply.html
        """
        data = {
            'Action': 'ListInventorySupply',
            'QueryStartDateTime': datetime_,
            'ResponseGroup': response_group,
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('SellerSkus.member.', skus))
        return self.make_request(data, "POST")

    def list_inventory_supply_by_next_token(self, token):
        """
        Alias for `list_inventory_supply(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_ListInventorySupplyByNextToken.html
        """
        return self.list_inventory_supply(next_token=token)
