"""
Amazon MWS Inventory Fulfillment API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action


class Inventory(MWS):
    """
    Amazon MWS Inventory Fulfillment API
    """

    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInventory/2010-10-01}"
    NEXT_TOKEN_OPERATIONS = [
        'ListInventorySupply',
    ]

    @next_token_action('ListInventorySupply')
    def list_inventory_supply(self, skus=(), datetime_=None,
                              response_group='Basic', next_token=None):
        """
        Returns information on available inventory
        """

        data = dict(
            Action='ListInventorySupply',
            QueryStartDateTime=datetime_,
            ResponseGroup=response_group,
        )
        data.update(utils.enumerate_param('SellerSkus.member.', skus))
        return self.make_request(data, "POST")

    def list_inventory_supply_by_next_token(self, token):
        """
        Deprecated.
        Use `list_inventory_supply(next_token=token)` instead.
        """
        # data = dict(Action='ListInventorySupplyByNextToken', NextToken=token)
        # return self.make_request(data, "POST")
        warnings.warn(
            "Use `list_inventory_supply(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_inventory_supply(next_token=token)
