"""Tests for the Orders API class."""

import datetime
import unittest
import mws
from mws.utils import clean_date

from .utils import CommonAPIRequestTools


class OrdersTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Orders."""

    api_class = mws.Orders

    # TODO: Add remaining methods for Orders

    def test_list_orders(self):
        """ListOrders operation."""
        created_after = datetime.datetime.utcnow()
        created_before = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        last_updated_after = datetime.datetime.utcnow() + datetime.timedelta(hours=2)
        last_updated_before = datetime.datetime.utcnow() + datetime.timedelta(hours=3)
        max_results = 83
        marketplace_ids = [
            "DV1t7ZOrjM",
            "LbGcgtGwEe",
        ]
        order_statuses = [
            "PendingAvailability",
            "Unshipped",
        ]
        fulfillment_channels = [
            "AFN",
            "MFN",
        ]
        payment_methods = [
            "COD",
            "CVS",
        ]
        buyer_email = "dudley.do.right@example.com"
        seller_order_id = "LbGcgtGwEe"
        tfm_shipment_statuses = [
            "PendingPickUp",
            "AtDestinationFC",
        ]
        params = self.api.list_orders(
            marketplace_ids=marketplace_ids,
            created_after=created_after,
            created_before=created_before,
            last_updated_after=last_updated_after,
            last_updated_before=last_updated_before,
            order_statuses=order_statuses,
            fulfillment_channels=fulfillment_channels,
            payment_methods=payment_methods,
            buyer_email=buyer_email,
            seller_order_id=seller_order_id,
            max_results=max_results,
            tfm_shipment_statuses=tfm_shipment_statuses,
        )
        self.assert_common_params(params, action="ListOrders")
        self.assertEqual(params["CreatedAfter"], clean_date(created_after))
        self.assertEqual(params["CreatedBefore"], clean_date(created_before))
        self.assertEqual(params["LastUpdatedAfter"], clean_date(last_updated_after))
        self.assertEqual(params["LastUpdatedBefore"], clean_date(last_updated_before))
        self.assertEqual(params["BuyerEmail"], "dudley.do.right%40example.com")
        self.assertEqual(params["SellerOrderId"], seller_order_id)
        self.assertEqual(params["MaxResultsPerPage"], str(max_results))
        self.assertEqual(params["OrderStatus.Status.1"], order_statuses[0])
        self.assertEqual(params["OrderStatus.Status.2"], order_statuses[1])
        self.assertEqual(params["MarketplaceId.Id.1"], marketplace_ids[0])
        self.assertEqual(params["MarketplaceId.Id.2"], marketplace_ids[1])
        self.assertEqual(
            params["FulfillmentChannel.Channel.1"], fulfillment_channels[0]
        )
        self.assertEqual(
            params["FulfillmentChannel.Channel.2"], fulfillment_channels[1]
        )
        self.assertEqual(params["PaymentMethod.Method.1"], payment_methods[0])
        self.assertEqual(params["PaymentMethod.Method.2"], payment_methods[1])
        self.assertEqual(params["TFMShipmentStatus.Status.1"], tfm_shipment_statuses[0])
        self.assertEqual(params["TFMShipmentStatus.Status.2"], tfm_shipment_statuses[1])

    def test_list_orders_by_next_token(self):
        """ListOrdersByNextToken operation, via method decorator."""
        next_token = "Wk8EzX62bL"
        params = self.api.list_orders(next_token=next_token)
        self.assert_common_params(params, action="ListOrdersByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_list_orders_by_next_token_alias(self):
        """ListOrdersByNextToken operation, via alias method."""
        next_token = "2tgLTgIrr7"
        params = self.api.list_orders_by_next_token(next_token)
        self.assert_common_params(params, action="ListOrdersByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_order(self):
        """GetOrder operation."""
        amazon_order_ids = [
            "983-3553534-8677372",
            "663-9447020-5093135",
            "918-0947007-5135971",
        ]
        params = self.api.get_order(amazon_order_ids)
        self.assert_common_params(params, action="GetOrder")
        self.assertEqual(params["AmazonOrderId.Id.1"], amazon_order_ids[0])
        self.assertEqual(params["AmazonOrderId.Id.2"], amazon_order_ids[1])
        self.assertEqual(params["AmazonOrderId.Id.3"], amazon_order_ids[2])

    def test_list_order_items(self):
        """ListOrderItems operation."""
        amazon_order_id = "695-3659745-3659863"
        params = self.api.list_order_items(amazon_order_id=amazon_order_id)
        self.assert_common_params(params, action="ListOrderItems")
        self.assertEqual(params["AmazonOrderId"], amazon_order_id)

    def test_list_order_items_by_next_token(self):
        """ListOrderItemsByNextToken operation, via method decorator."""
        next_token = "BaAzLiYLgM"
        params = self.api.list_order_items(next_token=next_token)
        self.assert_common_params(params, action="ListOrderItemsByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_list_order_items_by_next_token_alias(self):
        """ListOrderItemsByNextToken operation, via alias method."""
        next_token = "JuS3AvTNaW"
        params = self.api.list_order_items_by_next_token(next_token)
        self.assert_common_params(params, action="ListOrderItemsByNextToken")
        self.assertEqual(params["NextToken"], next_token)
