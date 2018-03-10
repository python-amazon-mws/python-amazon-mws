"""
Amazon MWS Merchant Fulfillment API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils


class MerchantFulfillment(MWS):
    """
    Amazon MWS Merchant Fulfillment API
    """
    URI = "/MerchantFulfillment/2015-06-01"
    VERSION = "2015-06-01"
    NS = '{https://mws.amazonservices.com/MerchantFulfillment/2015-06-01}'

    def get_eligible_shipping_services(self, amazon_order_id=None, seller_orderid=None, item_list=[],
                                       ship_from_address={}, package_dimensions={}, weight={},
                                       must_arrive_by_date=None, ship_date=None,
                                       shipping_service_options={}, label_customization={}):

        data = {
            "Action": "GetEligibleShippingServices",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_orderid,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", item_list))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def create_shipment(self, amazon_order_id=None, seller_orderid=None, item_list=[], ship_from_address={},
                        package_dimensions={}, weight={}, must_arrive_by_date=None, ship_date=None,
                        shipping_service_options={}, label_customization={}, shipping_service_id=None,
                        shipping_service_offer_id=None, hazmat_type=None):

        data = {
            "Action": "CreateShipment",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_orderid,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date,
            "ShippingServiceId": shipping_service_id,
            "ShippingServiceOfferId": shipping_service_offer_id,
            "HazmatType": hazmat_type
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", item_list))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def get_shipment(self, shipment_id=None):
        data = dict(Action="GetShipment", ShipmentId=shipment_id)
        return self.make_request(data)

    def cancel_shipment(self, shipment_id=None):
        data = dict(Action="CancelShipment", ShipmentId=shipment_id)
        return self.make_request(data)
