"""
Tests for the MWS.Finances API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class FinancesTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Finances.
    """
    # TODO: Add remaining methods for Finances
    def setUp(self):
        self.api = mws.Finances(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
