"""
Amazon MWS Recommendations API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
# from .. import utils
from ..decorators import next_token_action


class Recommendations(MWS):
    """
    Amazon MWS Recommendations API
    """
    URI = '/Recommendations/2013-04-01'
    VERSION = '2013-04-01'
    NAMESPACE = "{https://mws.amazonservices.com/Recommendations/2013-04-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListRecommendations",
    ]

    def get_last_updated_time_for_recommendations(self, marketplaceid):
        """
        Checks whether there are active recommendations for each category for the given marketplace, and if there are,
        returns the time when recommendations were last updated for each category.
        """
        data = dict(Action='GetLastUpdatedTimeForRecommendations',
                    MarketplaceId=marketplaceid)
        return self.make_request(data, "POST")

    @next_token_action('ListRecommendations')
    def list_recommendations(self, marketplaceid=None,
                             recommendationcategory=None, next_token=None):
        """
        Returns your active recommendations for a specific category or for all categories for a specific marketplace.
        """
        data = dict(Action="ListRecommendations",
                    MarketplaceId=marketplaceid,
                    RecommendationCategory=recommendationcategory)
        return self.make_request(data, "POST")

    def list_recommendations_by_next_token(self, token):
        """
        Deprecated.
        Use `list_recommendations(next_token=token)` instead.
        """
        # data = dict(Action="ListRecommendationsByNextToken",
        #             NextToken=token)
        # return self.make_request(data, "POST")
        warnings.warn(
            "Use `list_recommendations(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_recommendations(next_token=token)
