"""Amazon MWS Recommendations API."""

from mws import MWS
from mws.decorators import next_token_action

# DEPRECATIONS
from mws.utils.deprecation import kwargs_renamed_for_v11


class Recommendations(MWS):
    """Amazon MWS Recommendations API

    Docs:
    https://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_Overview.html
    """

    URI = "/Recommendations/2013-04-01"
    VERSION = "2013-04-01"
    NAMESPACE = "{https://mws.amazonservices.com/Recommendations/2013-04-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListRecommendations",
    ]

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_last_updated_time_for_recommendations(self, marketplace_id):
        """Checks whether there are active recommendations for each category for
        the given marketplace, and if there are, returns the time when recommendations
        were last updated for each category.

        Docs:
        https://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_GetLastUpdatedTimeForRecommendations.html
        """
        return self.make_request(
            "GetLastUpdatedTimeForRecommendations",
            {"MarketplaceId": marketplace_id},
            method="POST",
        )

    @kwargs_renamed_for_v11(
        [
            ("marketplaceid", "marketplace_id"),
            ("recommendationcategory", "recommendation_category"),
        ]
    )
    @next_token_action("ListRecommendations")
    def list_recommendations(
        self, marketplace_id=None, recommendation_category=None, next_token=None
    ):
        """Returns your active recommendations for a specific category or for all
        categories for a specific marketplace.

        Pass `next_token` to call "ListRecommendationsByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_ListRecommendations.html
        """
        return self.make_request(
            "ListRecommendations",
            {
                "MarketplaceId": marketplace_id,
                "RecommendationCategory": recommendation_category,
            },
            method="POST",
        )

    def list_recommendations_by_next_token(self, token):
        """Alias for `list_recommendations(next_token=token)` instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/recommendations/Recommendations_ListRecommendationsByNextToken.html
        """
        return self.list_recommendations(next_token=token)
