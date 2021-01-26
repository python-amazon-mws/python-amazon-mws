"""Amazon MWS Merchant Fulfillment API."""

from mws import MWS
from mws.utils.params import enumerate_keyed_param
from mws.utils.params import dict_keyed_param
from mws.utils.params import coerce_to_bool


class MerchantFulfillment(MWS):
    """Amazon MWS Merchant Fulfillment API

    Docs:
    https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_Overview.html
    """

    URI = "/MerchantFulfillment/2015-06-01"
    VERSION = "2015-06-01"
    NS = "{https://mws.amazonservices.com/MerchantFulfillment/2015-06-01}"

    def get_eligible_shipping_services(
        self,
        amazon_order_id=None,
        seller_order_id=None,
        items=None,
        ship_from_address=None,
        package_dimensions=None,
        weight=None,
        must_arrive_by_date=None,
        ship_date=None,
        shipping_service_options=None,
        label_customization=None,
        include_complex_options=None,
    ):
        """Returns a list of shipping service offers.

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
        https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_GetEligibleShippingServices.html
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
        if include_complex_options is not None:
            include_complex_options = coerce_to_bool(include_complex_options)

        data = {
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_order_id,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date,
            "ShippingOfferingFilter.IncludeComplexShippingOptions": include_complex_options,
        }
        data.update(
            enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", items)
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.ShipFromAddress", ship_from_address
            )
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.PackageDimensions", package_dimensions
            )
        )
        data.update(dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.ShippingServiceOptions",
                shipping_service_options,
            )
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.LabelCustomization", label_customization
            )
        )
        return self.make_request("GetEligibleShippingServices", data)

    def get_additional_seller_inputs(
        self, order_id, shipping_service_id, ship_from_address
    ):
        """Returns a list of additional seller inputs that are required from the seller
        to purchase the shipping service that you specify.

        Docs:
        https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_GetAdditionalSellerInputs.html

        - `order_id` refers to an AmazonOrderId for a given order.
        - `shipping_service_id` should be an identifier returned by a previous call to
          `get_eligible_shipping_services`.
        - `ship_from_address` should be a dict with keys matching the
          `Address` datatype:
          https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_Datatypes.html#Address
          (passing a non-dict value will result in a ValueError exception)
        """
        # TODO replace `ship_from_address` dict with a more useful dataclass.
        if not isinstance(ship_from_address, dict):
            raise ValueError("`ship_from_address` must be a dict object.")

        data = {
            "OrderId": order_id,
            "ShippingServiceId": shipping_service_id,
        }
        data.update(dict_keyed_param("ShipFromAddress", ship_from_address))
        return self.make_request("GetAdditionalSellerInputs", data)

    def create_shipment(
        self,
        amazon_order_id=None,
        seller_order_id=None,
        items=None,
        ship_from_address=None,
        package_dimensions=None,
        weight=None,
        must_arrive_by_date=None,
        ship_date=None,
        shipping_service_options=None,
        label_customization=None,
        shipping_service_id=None,
        shipping_service_offer_id=None,
        hazmat_type=None,
    ):
        """Purchases shipping and returns PDF, PNG, or ZPL document data for a shipping label, depending on the carrier;
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
        https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_CreateShipment.html
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
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_order_id,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date,
            "ShippingServiceId": shipping_service_id,
            "ShippingServiceOfferId": shipping_service_offer_id,
            "HazmatType": hazmat_type,
        }
        data.update(
            enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", items)
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.ShipFromAddress", ship_from_address
            )
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.PackageDimensions", package_dimensions
            )
        )
        data.update(dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.ShippingServiceOptions",
                shipping_service_options,
            )
        )
        data.update(
            dict_keyed_param(
                "ShipmentRequestDetails.LabelCustomization", label_customization
            )
        )
        return self.make_request("CreateShipment", data)

    def get_shipment(self, shipment_id=None):
        """Returns an existing shipment for a given identifier.

        Docs:
        https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_GetShipment.html
        """
        return self.make_request("GetShipment", {"ShipmentId": shipment_id})

    def cancel_shipment(self, shipment_id=None):
        """Cancels an existing shipment.

        Docs:
        https://docs.developer.amazonservices.com/en_US/merch_fulfill/MerchFulfill_CancelShipment.html
        """
        return self.make_request("CancelShipment", {"ShipmentId": shipment_id})
