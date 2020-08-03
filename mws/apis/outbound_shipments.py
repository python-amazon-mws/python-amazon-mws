"""Amazon MWS Fulfillment Outbound Shipments API."""

from mws import MWS, utils
from mws.decorators import next_token_action


class OutboundShipments(MWS):
    """Amazon MWS Fulfillment Outbound Shipments API.

    Docs:
    http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_Overview.html
    """

    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NEXT_TOKEN_OPERATIONS = [
        "ListAllFulfillmentOrders",
    ]

    # TODO: Complete these methods
    def create_fulfillment_order(
        self,
        marketplace_id=None,
        seller_fulfillment_order_id=None,
        fulfillment_action=None,
        displayable_order_id=None,
        displayable_order_datetime=None,
        displayable_order_comment=None,
        shipping_speed_category=None,
        destination_address=None,
        fulfillment_policy=None,
        notification_email_list=None,
        cod_settings=None,
        items=None,
        delivery_window=None,
    ):
        """Requests that Amazon ship items from the seller's inventory in Amazon's
        fulfillment network to a destination address.

        :param marketplace_id:
        :param seller_fulfillment_order_id: Required
        :param fulfillment_action:
        :param displayable_order_id: Required
        :param displayable_order_datetime: Required
        :param displayable_order_comment: Required
        :param shipping_speed_category: Required
        :param destination_address: Required
        :param fulfillment_policy:
        :param notification_email_list:
        :param cod_settings:
        :param items: Required
        :param delivery_window:

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CreateFulfillmentOrder.html
        """
        data = {
            "Action": "CreateFulfillmentOrder",
            "MarketplaceId": marketplace_id,
            "SellerFulfillmentOrderId": seller_fulfillment_order_id,
            "FulfillmentAction": fulfillment_action,
            "DisplayableOrderId": displayable_order_id,
            "DisplayableOrderDateTime": displayable_order_datetime,
            "DisplayableOrderComment": displayable_order_comment,
            "ShippingSpeedCategory": shipping_speed_category,
            "FulfillmentPolicy": fulfillment_policy,
        }
        data.update(utils.enumerate_keyed_param("Items.member", items or []))
        data.update(
            utils.dict_keyed_param("DestinationAddress", destination_address or {})
        )
        data.update(utils.dict_keyed_param("CODSettings", cod_settings or {}))
        data.update(utils.dict_keyed_param("DeliveryWindow", delivery_window or {}))
        data.update(
            utils.enumerate_param(
                "NotificationEmailList.member", notification_email_list or []
            )
        )
        return self.make_request(data)

    def update_fulfillment_order(self):
        """Updates and/or requests shipment for a fulfillment order with an order hold on it.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_UpdateFulfillmentOrder.html
        """
        raise NotImplementedError

    def get_fulfillment_order(self, seller_fulfillment_order_id):
        """Returns a fulfillment order based on a specified SellerFulfillmentOrderId.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetFulfillmentOrder.html
        """
        data = dict(
            Action="GetFulfillmentOrder",
            SellerFulfillmentOrderId=seller_fulfillment_order_id,
        )
        return self.make_request(data)

    @next_token_action("ListAllFulfillmentOrders")
    def list_all_fulfillment_orders(self, query_start_date_time=None, next_token=None):
        """Returns a list of fulfillment orders fulfilled after (or at) a specified date.

        Pass `next_token` to call "ListAllFulfillmentOrdersByNextToken" instead

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListAllFulfillmentOrders.html
        """
        data = {
            "Action": "ListAllFulfillmentOrders",
            "QueryStartDateTime": query_start_date_time,
        }
        return self.make_request(data)

    def list_all_fulfillment_orders_by_next_token(self, token):
        """Alias for `list_all_fulfillment_orders(next_token=token)`.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListAllFulfillmentOrdersByNextToken.html
        """
        return self.list_all_fulfillment_orders(next_token=token)

    def get_package_tracking_details(self, package_number):
        """Returns delivery tracking information for a package
        in an outbound shipment for a Multi-Channel Fulfillment order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_GetPackageTrackingDetails.html
        """
        data = dict(Action="GetPackageTrackingDetails", PackageNumber=package_number)
        return self.make_request(data)

    def cancel_fulfillment_order(self):
        """Requests that Amazon stop attempting to fulfill an existing fulfillment order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CancelFulfillmentOrder.html
        """
        raise NotImplementedError

    def list_return_reason_codes(self):
        """Returns a list of return reason codes for a seller SKU in a given marketplace.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_ListReturnReasonCodes.html
        """
        raise NotImplementedError

    def create_fulfillment_return(self):
        """Creates a fulfillment return.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_outbound/FBAOutbound_CreateFulfillmentReturn.html
        """
        raise NotImplementedError
