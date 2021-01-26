"""Amazon MWS Sellers API."""

from mws import MWS
from mws.decorators import next_token_action


class Sellers(MWS):
    """Amazon MWS Sellers API

    Docs:
    https://docs.developer.amazonservices.com/en_US/sellers/Sellers_Overview.html
    """

    URI = "/Sellers/2011-07-01"
    VERSION = "2011-07-01"
    NAMESPACE = "{http://mws.amazonservices.com/schema/Sellers/2011-07-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListMarketplaceParticipations",
    ]

    @next_token_action("ListMarketplaceParticipations")
    def list_marketplace_participations(self, next_token=None):
        """Returns a list of marketplaces that the seller submitting the request can sell in,
        and a list of participations that include seller-specific information in that marketplace.

        Pass `next_token` to call "ListMarketplaceParticipationsByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/sellers/Sellers_ListMarketplaceParticipations.html
        """
        return self.make_request("ListMarketplaceParticipations")

    def list_marketplace_participations_by_next_token(self, token):
        """Alias for `list_marketplace_participations(next_token=token)`

        Docs:
        https://docs.developer.amazonservices.com/en_US/sellers/Sellers_ListMarketplaceParticipationsByNextToken.html
        """
        return self.list_marketplace_participations(next_token=token)
