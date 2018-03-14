"""
Tests for the MerchantFulfillment API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class MerchantFulfillmentTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for MerchantFulfillment.
    """
    # TODO: Add remaining methods for MerchantFulfillment
    def setUp(self):
        self.api = mws.MerchantFulfillment(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    # def test_get_eligible_shipping_services(self):
    #     """
    #     XYZ operation.
    #     """
    #     params = self.api.get_eligible_shipping_services()
    #     self.assert_common_params(params)
    #     self.assertEqual(params['Action'], 'GetEligibleShippingServices')

    # def test_create_shipment(self):
    #     """
    #     XYZ operation.
    #     """
    #     params = self.api.create_shipment()
    #     self.assert_common_params(params)
    #     self.assertEqual(params['Action'], 'CreateShipment')

    def test_get_shipment(self):
        """
        XYZ operation.
        """
        shipment_id = 'UCXN7ZubAj'
        params = self.api.get_shipment(
            shipment_id=shipment_id,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetShipment')
        self.assertEqual(params['ShipmentId'], shipment_id)

    def test_cancel_shipment(self):
        """
        XYZ operation.
        """
        shipment_id = 'C6Pvk0b2yZ'
        params = self.api.cancel_shipment(
            shipment_id=shipment_id,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'CancelShipment')
        self.assertEqual(params['ShipmentId'], shipment_id)
