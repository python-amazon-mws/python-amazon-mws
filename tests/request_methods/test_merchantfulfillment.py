"""Tests for the MerchantFulfillment API class."""
import datetime
import unittest

import mws
from .utils import (
    CommonAPIRequestTools,
    clean_date,
    clean_string,
    clean_bool,
)


class MerchantFulfillmentTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for MerchantFulfillment."""

    api_class = mws.MerchantFulfillment

    # TODO: Add remaining methods for MerchantFulfillment

    def test_get_eligible_shipping_services(self):
        """GetEligibleShippingServices operation."""
        amazon_order_id = "903-9939455-1336669"
        seller_order_id = "something-or-other"
        items = [
            {"OrderItemId": "1234567890", "Quantity": "1"},
            {"OrderItemId": "0987654321", "Quantity": "5"},
        ]
        # Fake generated name and address, not likely a real person or phone number.
        ship_from_address = {
            "Name": "Socorro M Rosa",
            "AddressLine1": "2025 Foley Street",
            "City": "Miramar",
            "StateOrProvinceCode": "FL",
            "PostalCode": "33025",
            "CountryCode": "US",
            "Email": "dory@example.com",
            "Phone": "954-655-0094",
        }
        package_dimensions = {
            "Length": "12",
            "Width": "34",
            "Height": "25",
            "Unit": "centimeters",
        }
        weight = {
            "Value": "308",
            "Unit": "grams",
        }
        must_arrive_by_date = datetime.datetime.utcnow()
        ship_date = datetime.datetime.utcnow() + datetime.timedelta(days=14)
        shipping_service_options = {
            "DeliveryExperience": "DeliveryConfirmationWithoutSignature",
            "CarrierWillPickUp": False,
            "DeclaredValue.Amount": "10.00",
            "DeclaredValue.CurrencyCode": "USD",
        }
        label_customization = {
            "CustomTextForLabel": "NO ALLIGATORS!",
            "StandardIdForLabel": "AmazonOrderId",
        }
        include_complex_options = True

        # Get request params
        params = self.api.get_eligible_shipping_services(
            amazon_order_id=amazon_order_id,
            seller_order_id=seller_order_id,
            items=items,
            ship_from_address=ship_from_address,
            package_dimensions=package_dimensions,
            weight=weight,
            must_arrive_by_date=must_arrive_by_date,
            ship_date=ship_date,
            shipping_service_options=shipping_service_options,
            label_customization=label_customization,
            include_complex_options=include_complex_options,
        )

        self.assert_common_params(params, action="GetEligibleShippingServices")

        # Check for our expected params
        # fmt: off
        expected = {
            "ShipmentRequestDetails.AmazonOrderId": clean_string(amazon_order_id),
            "ShipmentRequestDetails.SellerOrderId": clean_string(seller_order_id),
            "ShipmentRequestDetails.MustArriveByDate": clean_date(must_arrive_by_date),
            "ShipmentRequestDetails.PackageDimensions.Length": clean_string(package_dimensions["Length"]),
            "ShipmentRequestDetails.PackageDimensions.Width": clean_string(package_dimensions["Width"]),
            "ShipmentRequestDetails.PackageDimensions.Height": clean_string(package_dimensions["Height"]),
            "ShipmentRequestDetails.PackageDimensions.Unit": clean_string(package_dimensions["Unit"]),
            "ShipmentRequestDetails.Weight.Value": clean_string(weight["Value"]),
            "ShipmentRequestDetails.Weight.Unit": clean_string(weight["Unit"]),
            "ShipmentRequestDetails.ShipDate": clean_date(ship_date),
            "ShipmentRequestDetails.ShipFromAddress.Name": clean_string(ship_from_address["Name"]),
            "ShipmentRequestDetails.ShipFromAddress.AddressLine1": clean_string(ship_from_address["AddressLine1"]),
            "ShipmentRequestDetails.ShipFromAddress.City": clean_string(ship_from_address["City"]),
            "ShipmentRequestDetails.ShipFromAddress.StateOrProvinceCode": clean_string(ship_from_address["StateOrProvinceCode"]),
            "ShipmentRequestDetails.ShipFromAddress.PostalCode": clean_string(ship_from_address["PostalCode"]),
            "ShipmentRequestDetails.ShipFromAddress.CountryCode": clean_string(ship_from_address["CountryCode"]),
            "ShipmentRequestDetails.ShipFromAddress.Email": clean_string(ship_from_address["Email"]),
            "ShipmentRequestDetails.ShipFromAddress.Phone": clean_string(ship_from_address["Phone"]),
            "ShipmentRequestDetails.ShippingServiceOptions.DeliveryExperience": clean_string(shipping_service_options["DeliveryExperience"]),
            "ShipmentRequestDetails.ShippingServiceOptions.CarrierWillPickUp": clean_bool(shipping_service_options["CarrierWillPickUp"]),
            "ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.CurrencyCode": clean_string(shipping_service_options["DeclaredValue.CurrencyCode"]),
            "ShipmentRequestDetails.ShippingServiceOptions.DeclaredValue.Amount": clean_string(shipping_service_options["DeclaredValue.Amount"]),
            "ShipmentRequestDetails.ItemList.Item.1.OrderItemId": clean_string(items[0]["OrderItemId"]),
            "ShipmentRequestDetails.ItemList.Item.1.Quantity": clean_string(items[0]["Quantity"]),
            "ShipmentRequestDetails.ItemList.Item.2.OrderItemId": clean_string(items[1]["OrderItemId"]),
            "ShipmentRequestDetails.ItemList.Item.2.Quantity": clean_string(items[1]["Quantity"]),
            "ShippingOfferingFilter.IncludeComplexShippingOptions": clean_bool(include_complex_options),
        }
        # fmt: on

        for key, val in expected.items():
            self.assertEqual(params[key], val)

    # def test_create_shipment(self):
    #     """CreateShipment operation."""
    #     params = self.api.create_shipment()
    #     self.assert_common_params(params, action="CreateShipment")

    def test_get_additional_seller_inputs(self):
        """GetAdditionalSellerInputs operation."""
        order_id = "922-2942641-9412606"
        shipping_service_id = "CHINA_POST_E_COURIER_PRI"
        ship_from_address = {
            "Name": "Shenzhen Address",
            "AddressLine1": "test address",
            "City": "Shenzhen",
            "StateOrProvinceCode": "Guangdong",
            "PostalCode": "510810",
            "CountryCode": "CN",
            "Email": "example@email.com",
            "Phone": "555-555-5555",
        }

        params = self.api.get_additional_seller_inputs(
            order_id=order_id,
            shipping_service_id=shipping_service_id,
            ship_from_address=ship_from_address,
        )

        self.assert_common_params(params, action="GetAdditionalSellerInputs")

        # fmt: off
        expected = {
            "OrderId": clean_string(order_id),
            "ShippingServiceId": clean_string(shipping_service_id),
            "ShipFromAddress.Name": clean_string(ship_from_address["Name"]),
            "ShipFromAddress.AddressLine1": clean_string(ship_from_address["AddressLine1"]),
            "ShipFromAddress.City": clean_string(ship_from_address["City"]),
            "ShipFromAddress.StateOrProvinceCode": clean_string(ship_from_address["StateOrProvinceCode"]),
            "ShipFromAddress.PostalCode": clean_string(ship_from_address["PostalCode"]),
            "ShipFromAddress.CountryCode": clean_string(ship_from_address["CountryCode"]),
            "ShipFromAddress.Email": clean_string(ship_from_address["Email"]),
            "ShipFromAddress.Phone": clean_string(ship_from_address["Phone"]),
        }
        # fmt: on

        for key, val in expected.items():
            self.assertEqual(params[key], val)

    def test_get_shipment(self):
        """GetShipment operation."""
        shipment_id = "UCXN7ZubAj"
        params = self.api.get_shipment(
            shipment_id=shipment_id,
        )
        self.assert_common_params(params, action="GetShipment")
        self.assertEqual(params["ShipmentId"], shipment_id)

    def test_cancel_shipment(self):
        """CancelShipment operation."""
        shipment_id = "C6Pvk0b2yZ"
        params = self.api.cancel_shipment(
            shipment_id=shipment_id,
        )
        self.assert_common_params(params, action="CancelShipment")
        self.assertEqual(params["ShipmentId"], shipment_id)
