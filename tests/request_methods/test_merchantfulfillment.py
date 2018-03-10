"""
Tests for the MWS.MerchantFulfillment API class.
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
