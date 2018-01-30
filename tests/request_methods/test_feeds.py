"""
Tests for the MWS.Feeds API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class FeedsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Feeds.
    """
    # TODO: Add remaining methods for Feeds
    def setUp(self):
        self.api = mws.Feeds(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True
