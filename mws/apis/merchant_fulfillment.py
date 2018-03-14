"""
Amazon MWS Merchant Fulfillment API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils


class MerchantFulfillment(MWS):
    """
    Amazon MWS Merchant Fulfillment API

    Docs:
    http://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_Overview.html
    """
    URI = "/MerchantFulfillment/2015-06-01"
    VERSION = "2015-06-01"
    NS = '{https://mws.amazonservices.com/MerchantFulfillment/2015-06-01}'

    def get_eligible_shipping_services(self, amazon_order_id=None, seller_order_id=None, items=None,
                                       ship_from_address=None, package_dimensions=None, weight=None,
                                       must_arrive_by_date=None, ship_date=None,
                                       shipping_service_options=None, label_customization=None):

        """
        Returns a list of shipping service offers.

        :param amazon_order_id: Required
        :param seller_order_id:
        :param items: Required
        :param ship_from_address: Required
        :param package_dimensions: Required
        :param weight: Required
        :param must_arrive_by_date:
        :param ship_date:
        :param shipping_service_options: Required
        :param label_customization:
        :return:

        Docs:
        http://docs.developer.amazonservices.com/en_UK/merch_fulfill/MerchFulfill_GetEligibleShippingServices.html
        """

        if ship_from_address is None:
            ship_from_address = {}
        if package_dimensions is None:
            package_dimensions = {}
        if weight is None:
            weight = {}
        if items is None:
            items = []
        if shipping_service_options is None:
            shipping_service_options = {}
        if label_customization is None:
            label_customization = {}

        data = {
            "Action": "GetEligibleShippingServices",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_order_id,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", items))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def create_shipment(self, amazon_order_id=None, seller_order_id=None, items=None, ship_from_address=None,
                        package_dimensions=None, weight=None, must_arrive_by_date=None, ship_date=None,
                        shipping_service_options=None, label_customization=None, shipping_service_id=None,
                        shipping_service_offer_id=None, hazmat_type=None):
        """
        Purchases shipping and returns PDF, PNG, or ZPL document data for a shipping label, depending on the carrier;
        as well as a Base64-encoded MD5 hash to validate the document data.

        :param amazon_order_id: Required
        :param seller_order_id:
        :param items: Required
        :param ship_from_address: Required
        :param package_dimensions: Required
        :param weight: Required
        :param must_arrive_by_date:
        :param ship_date:
        :param shipping_service_options:
        :param label_customization:
        :param shipping_service_id: Required
        :param shipping_service_offer_id:
        :param hazmat_type:
        :return:

        Docs:
        http://docs.developer.amazonservices.com/en_UK/merch_fulfill/MerchFulfill_CreateShipment.html
        """

        if items is None:
            items = []
        if ship_from_address is None:
            ship_from_address = {}
        if package_dimensions is None:
            package_dimensions = {}
        if weight is None:
            weight = {}
        if shipping_service_options is None:
            shipping_service_options = {}
        if label_customization is None:
            label_customization = {}

        data = {
            "Action": "CreateShipment",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_order_id,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date,
            "ShippingServiceId": shipping_service_id,
            "ShippingServiceOfferId": shipping_service_offer_id,
            "HazmatType": hazmat_type
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", items))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def get_shipment(self, shipment_id=None):
        """
        Returns an existing shipment for a given identifier.

        Docs:
        http://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_GetShipment.html
        """
        data = {
            'Action': "GetShipment",
            'ShipmentId': shipment_id,
        }
        return self.make_request(data)

    def cancel_shipment(self, shipment_id=None):
        """
        Cancels an existing shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_CancelShipment.html
        """
        data = {
            'Action': "CancelShipment",
            'ShipmentId': shipment_id,
        }
        return self.make_request(data)
