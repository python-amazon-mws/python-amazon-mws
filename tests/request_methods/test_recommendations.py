"""Tests for the Recommendations API class."""

import unittest
import mws
from mws.utils import clean_string

from .utils import CommonAPIRequestTools


class RecommendationsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """
    Test cases for Recommendations.
    """

    api_class = mws.Recommendations

    # TODO: Add remaining methods for Recommendations

    def test_get_last_updated_time_for_recommendations(self):
        """GetLastUpdatedTimeForRecommendations operation"""
        marketplace_id = "marketplace_foobar"
        params = self.api.get_last_updated_time_for_recommendations(marketplace_id)
        self.assert_common_params(params, action="GetLastUpdatedTimeForRecommendations")
        self.assertEqual(params["MarketplaceId"], marketplace_id)

    def test_list_recommendations(self):
        """ListRecommendations operation"""
        marketplace_id = "marketplace_bazbar"
        recommendation_category = "muffin balls"
        params = self.api.list_recommendations(
            marketplace_id=marketplace_id,
            recommendation_category=recommendation_category,
        )
        self.assert_common_params(params, action="ListRecommendations")
        self.assertEqual(params["MarketplaceId"], marketplace_id)
        self.assertEqual(
            params["RecommendationCategory"], clean_string(recommendation_category)
        )

    def test_list_recommendations_by_next_token(self):
        """ListRecommendationsByNextToken operation, via next_token arg."""
        next_token = "foobar123"
        params = self.api.list_recommendations(next_token=next_token)
        self.assert_common_params(params, action="ListRecommendationsByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_list_recommendations_by_next_token_alias(self):
        """ListRecommendationsByNextToken operation, via alias method."""
        next_token = "barbaz456"
        params = self.api.list_recommendations_by_next_token(next_token)
        self.assert_common_params(params, action="ListRecommendationsByNextToken")
        self.assertEqual(params["NextToken"], next_token)
