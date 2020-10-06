"""Tests for the Sellers API class."""

import unittest
import mws
from .utils import CommonAPIRequestTools


class SellersTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Sellers."""

    api_class = mws.Sellers

    # TODO: Add remaining methods for Sellers

    def test_list_marketplace_participations(self):
        """ListMarketplaceParticipations operation."""
        params = self.api.list_marketplace_participations()
        self.assert_common_params(params, action="ListMarketplaceParticipations")

    def test_list_marketplace_participations_by_next_token(self):
        """ListMarketplaceParticipationsByNextToken operation, via `next_token` arg."""
        next_token = "token_foobar"
        params = self.api.list_marketplace_participations(next_token=next_token)
        self.assert_common_params(
            params, action="ListMarketplaceParticipationsByNextToken"
        )
        self.assertEqual(params["NextToken"], next_token)

    def test_list_marketplace_participations_by_next_token_alias(self):
        """ListMarketplaceParticipationsByNextToken operation, via alias method."""
        next_token = "token_foobar"
        params = self.api.list_marketplace_participations_by_next_token(next_token)
        self.assert_common_params(
            params, action="ListMarketplaceParticipationsByNextToken"
        )
        self.assertEqual(params["NextToken"], next_token)
