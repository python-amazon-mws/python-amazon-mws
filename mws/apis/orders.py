"""
Amazon Orders API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action


class Orders(MWS):
    """
    Amazon Orders API
    """
    URI = "/Orders/2013-09-01"
    VERSION = "2013-09-01"
    NAMESPACE = '{https://mws.amazonservices.com/Orders/2013-09-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListOrders',
        'ListOrderItems',
    ]

    @next_token_action('ListOrders')
    def list_orders(self, marketplaceids=None, created_after=None, created_before=None,
                    lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(),
                    fulfillment_channels=(), payment_methods=(), buyer_email=None,
                    seller_orderid=None, max_results='100', next_token=None):

        data = dict(Action='ListOrders',
                    CreatedAfter=created_after,
                    CreatedBefore=created_before,
                    LastUpdatedAfter=lastupdatedafter,
                    LastUpdatedBefore=lastupdatedbefore,
                    BuyerEmail=buyer_email,
                    SellerOrderId=seller_orderid,
                    MaxResultsPerPage=max_results,
                    )
        data.update(utils.enumerate_param('OrderStatus.Status.', orderstatus))
        data.update(utils.enumerate_param('MarketplaceId.Id.', marketplaceids))
        data.update(utils.enumerate_param('FulfillmentChannel.Channel.', fulfillment_channels))
        data.update(utils.enumerate_param('PaymentMethod.Method.', payment_methods))
        return self.make_request(data)

    def list_orders_by_next_token(self, token):
        """
        Deprecated.
        Use `list_orders(next_token=token)` instead.
        """
        # data = dict(Action='ListOrdersByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_orders(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_orders(next_token=token)

    def get_order(self, amazon_order_ids):
        data = dict(Action='GetOrder')
        data.update(utils.enumerate_param('AmazonOrderId.Id.', amazon_order_ids))
        return self.make_request(data)

    @next_token_action('ListOrderItems')
    def list_order_items(self, amazon_order_id=None, next_token=None):
        data = dict(Action='ListOrderItems', AmazonOrderId=amazon_order_id)
        return self.make_request(data)

    def list_order_items_by_next_token(self, token):
        """
        Deprecated.
        Use `list_order_items(next_token=token)` instead.
        """
        # data = dict(Action='ListOrderItemsByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_order_items(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_order_items(next_token=token)
