"""
Tests for the Sellers API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class SellersTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Sellers.
    """
    # TODO: Add remaining methods for Sellers
    def setUp(self):
        self.api = mws.Sellers(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_list_marketplace_participations(self):
        """
        ListMarketplaceParticipations operation
        """
        params = self.api.list_marketplace_participations()
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListMarketplaceParticipations')

    def test_list_marketplace_participations_by_next_token(self):
        """
        ListMarketplaceParticipationsByNextToken operation, by way of method decorator.
        """
        next_token = 'token_foobar'
        params = self.api.list_marketplace_participations(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListMarketplaceParticipationsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_marketplace_participations_by_next_token_alias(self):
        """
        ListMarketplaceParticipationsByNextToken operation, by way of alias method.
        """
        next_token = 'token_foobar'
        params = self.api.list_marketplace_participations_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListMarketplaceParticipationsByNextToken')
        self.assertEqual(params['NextToken'], next_token)
