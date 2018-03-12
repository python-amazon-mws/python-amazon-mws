"""
Tests for the Subscriptions API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class SubscriptionsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Subscriptions.
    """
    # TODO: Add remaining methods for Subscriptions
    def setUp(self):
        self.api = mws.Subscriptions(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
