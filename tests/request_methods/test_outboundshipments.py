"""
Tests for the MWS.OutboundShipments API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class OutboundShipmentsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for OutboundShipments.
    """
    # TODO: Add remaining methods for OutboundShipments

    def setUp(self):
        self.api = mws.OutboundShipments(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
