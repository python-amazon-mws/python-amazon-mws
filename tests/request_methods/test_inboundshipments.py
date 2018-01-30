"""
Tests for the MWS.InboundShipments API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class InboundShipmentsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for InboundShipments.
    """
    # TODO: Add remaining methods for InboundShipments
    def setUp(self):
        self.api = mws.InboundShipments(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
