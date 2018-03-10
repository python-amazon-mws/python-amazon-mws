"""
Tests for the MWS.Orders API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class OrdersTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Orders.
    """
    # TODO: Add remaining methods for Orders
    def setUp(self):
        self.api = mws.Orders(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
