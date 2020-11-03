"""Amazon Orders API."""

from mws import MWS
from mws.utils.params import enumerate_param
from mws.utils.params import enumerate_params
from mws.decorators import next_token_action

# DEPRECATIONS
from mws.utils.deprecation import kwargs_renamed_for_v11


class Orders(MWS):
    """Amazon Orders API

    Docs:
    https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_Overview.html
    """

    URI = "/Orders/2013-09-01"
    VERSION = "2013-09-01"
    NAMESPACE = "{https://mws.amazonservices.com/Orders/2013-09-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListOrders",
        "ListOrderItems",
    ]

    @kwargs_renamed_for_v11(
        [
            ("marketplaceids", "marketplace_ids"),
            ("lastupdatedafter", "last_updated_after"),
            ("lastupdatedbefore", "last_updated_before"),
            ("orderstatus", "order_statuses"),
            ("seller_orderid", "seller_order_id"),
        ]
    )
    @next_token_action("ListOrders")
    def list_orders(
        self,
        marketplace_ids=None,
        created_after=None,
        created_before=None,
        last_updated_after=None,
        last_updated_before=None,
        order_statuses=None,
        fulfillment_channels=None,
        payment_methods=None,
        buyer_email=None,
        seller_order_id=None,
        max_results=None,
        tfm_shipment_statuses=None,
        easyship_statuses=None,
        next_token=None,
    ):
        """Returns orders created or updated during a time frame that you specify.

        Pass `next_token` to call "ListOrdersByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrders.html
        """
        marketplace_ids = marketplace_ids or []
        order_statuses = order_statuses or []
        fulfillment_channels = fulfillment_channels or []
        payment_methods = payment_methods or []
        tfm_shipment_statuses = tfm_shipment_statuses or []
        # for easyship orders, available only for India marketplace
        easyship_statuses = easyship_statuses or []
        data = {
            "CreatedAfter": created_after,
            "CreatedBefore": created_before,
            "LastUpdatedAfter": last_updated_after,
            "LastUpdatedBefore": last_updated_before,
            "BuyerEmail": buyer_email,
            "SellerOrderId": seller_order_id,
            "MaxResultsPerPage": max_results,
        }
        data.update(
            enumerate_params(
                {
                    "OrderStatus.Status.": order_statuses,
                    "MarketplaceId.Id.": marketplace_ids,
                    "FulfillmentChannel.Channel.": fulfillment_channels,
                    "PaymentMethod.Method.": payment_methods,
                    "TFMShipmentStatus.Status.": tfm_shipment_statuses,
                    "EasyShipShipmentStatus.Status": easyship_statuses,
                }
            )
        )
        return self.make_request("ListOrders", data)

    def list_orders_by_next_token(self, token):
        """Alias for `list_orders(next_token=token)`

        Docs:
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrdersByNextToken.html
        """
        return self.list_orders(next_token=token)

    def get_order(self, amazon_order_ids):
        """Returns orders based on the AmazonOrderId values that you specify.

        Docs:
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_GetOrder.html
        """
        data = enumerate_param("AmazonOrderId.Id.", amazon_order_ids)
        return self.make_request("GetOrder", data)

    @next_token_action("ListOrderItems")
    def list_order_items(self, amazon_order_id=None, next_token=None):
        """Returns order items based on the AmazonOrderId that you specify.

        Pass `next_token` to call "ListOrderItemsByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrderItems.html
        """
        return self.make_request("ListOrderItems", {"AmazonOrderId": amazon_order_id})

    def list_order_items_by_next_token(self, token):
        """Alias for `list_order_items(next_token=token)`

        Docs:
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrderItemsByNextToken.html
        """
        return self.list_order_items(next_token=token)
