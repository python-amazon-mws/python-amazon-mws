"""Tests for the MWS.OutboundShipments API class."""

import unittest
import mws
from .utils import CommonAPIRequestTools


class OutboundShipmentsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for OutboundShipments."""

    api_class = mws.OutboundShipments

    # TODO: Add remaining methods for OutboundShipments

    # def test_create_shipment(self):
    #     """
    #     CreateFulfillmentOrder operation.
    #     """
    #     params = self.api.create_shipment()
    #     self.assert_common_params(params, action="CreateFulfillmentOrder")
