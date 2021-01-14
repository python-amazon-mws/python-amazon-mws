"""Amazon MWS Inventory Fulfillment API."""

from mws import MWS
from mws.utils.params import enumerate_param
from mws.decorators import next_token_action


class Inventory(MWS):
    """Amazon MWS Inventory Fulfillment API

    Docs:
    https://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_Overview.html
    """

    URI = "/FulfillmentInventory/2010-10-01"
    VERSION = "2010-10-01"
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInventory/2010-10-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListInventorySupply",
    ]

    @next_token_action("ListInventorySupply")
    def list_inventory_supply(
        self,
        skus=(),
        datetime_=None,
        response_group="Basic",
        marketplace_id=None,
        next_token=None,
    ):
        """Returns information on available inventory

        Pass `next_token` to call "ListInventorySupplyByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_ListInventorySupply.html
        """
        data = {
            "QueryStartDateTime": datetime_,
            "ResponseGroup": response_group,
            "MarketplaceId": marketplace_id,
        }
        data.update(enumerate_param("SellerSkus.member.", skus))
        return self.make_request("ListInventorySupply", data, method="POST")

    def list_inventory_supply_by_next_token(self, token):
        """Alias for `list_inventory_supply(next_token=token)`

        Docs:
        https://docs.developer.amazonservices.com/en_US/fba_inventory/FBAInventory_ListInventorySupplyByNextToken.html
        """
        return self.list_inventory_supply(next_token=token)
