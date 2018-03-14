"""
Amazon MWS Recommendations API
"""
from __future__ import absolute_import

from ..mws import MWS
from ..decorators import next_token_action


class Recommendations(MWS):
    """
    Amazon MWS Recommendations API

    Docs:
    http://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_Overview.html
    """
    URI = '/Recommendations/2013-04-01'
    VERSION = '2013-04-01'
    NAMESPACE = "{https://mws.amazonservices.com/Recommendations/2013-04-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListRecommendations",
    ]

    def get_last_updated_time_for_recommendations(self, marketplace_id):
        """
        Checks whether there are active recommendations for each category for the given marketplace, and if there are,
        returns the time when recommendations were last updated for each category.

        Docs:
        http://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_GetLastUpdatedTimeForRecommendations.html
        """
        data = {
            'Action': 'GetLastUpdatedTimeForRecommendations',
            'MarketplaceId': marketplace_id,
        }
        return self.make_request(data, "POST")

    @next_token_action('ListRecommendations')
    def list_recommendations(self, marketplace_id=None, recommendation_category=None, next_token=None):
        """
        Returns your active recommendations for a specific category or for all categories for a specific marketplace.

        Pass `next_token` to call "ListRecommendationsByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_ListRecommendations.html
        """
        data = {
            'Action': "ListRecommendations",
            'MarketplaceId': marketplace_id,
            'RecommendationCategory': recommendation_category,
        }
        return self.make_request(data, "POST")

    def list_recommendations_by_next_token(self, token):
        """
        Alias for `list_recommendations(next_token=token)` instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_ListRecommendationsByNextToken.html
        """
        return self.list_recommendations(next_token=token)
