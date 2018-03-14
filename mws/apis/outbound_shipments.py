"""
Amazon MWS Fulfillment Outbound Shipments API
"""
from __future__ import absolute_import
# import warnings

from ..mws import MWS
# from .. import utils
from ..decorators import next_token_action


class OutboundShipments(MWS):
    """
    Amazon MWS Fulfillment Outbound Shipments API

    Docs:
    http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_Overview.html
    """
    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NEXT_TOKEN_OPERATIONS = [
        'ListAllFulfillmentOrders',
    ]

    # TODO: Complete these methods
    def get_fulfillment_preview(self):
        """
        Returns a list of fulfillment order previews based on shipping criteria that you specify.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetFulfillmentPreview.html
        """
        raise NotImplementedError

    def create_fulfillment_order(self):
        """
        Requests that Amazon ship items from the seller's inventory in Amazon's fulfillment network
        to a destination address.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CreateFulfillmentOrder.html
        """
        raise NotImplementedError

    def update_fulfillment_order(self):
        """
        Updates and/or requests shipment for a fulfillment order with an order hold on it.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_UpdateFulfillmentOrder.html
        """
        raise NotImplementedError

    def get_fulfillment_order(self):
        """
        Returns a fulfillment order based on a specified SellerFulfillmentOrderId.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetFulfillmentOrder.html
        """
        raise NotImplementedError

    @next_token_action('ListAllFulfillmentOrders')
    def list_all_fulfillment_orders(self, next_token=None):
        """
        Returns a list of fulfillment orders fulfilled after (or at) a specified date.

        Pass `next_token` to call "ListAllFulfillmentOrdersByNextToken" instead

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListAllFulfillmentOrders.html
        """
        raise NotImplementedError

    def list_all_fulfillment_orders_by_next_token(self, token):
        """
        Alias for `list_all_fulfillment_orders(next_token=token)`.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListAllFulfillmentOrdersByNextToken.html
        """
        raise NotImplementedError
        # return self.list_all_fulfillment_orders(next_token=token)

    def get_package_tracking_details(self):
        """
        Returns delivery tracking information for a package in an outbound shipment for a
        Multi-Channel Fulfillment order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetPackageTrackingDetails.html
        """
        raise NotImplementedError

    def cancel_fulfillment_order(self):
        """
        Requests that Amazon stop attempting to fulfill an existing fulfillment order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CancelFulfillmentOrder.html
        """
        raise NotImplementedError

    def list_return_reason_codes(self):
        """
        Returns a list of return reason codes for a seller SKU in a given marketplace.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListReturnReasonCodes.html
        """
        raise NotImplementedError

    def create_fulfillment_return(self):
        """
        Creates a fulfillment return.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CreateFulfillmentReturn.html
        """
        raise NotImplementedError
