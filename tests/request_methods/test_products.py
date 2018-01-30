"""
Tests for the MWS.Products API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class ProductsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Products.
    """
    # TODO: Add remaining methods for Products
    def setUp(self):
        self.api = mws.Products(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
