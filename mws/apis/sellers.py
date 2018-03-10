"""
Amazon MWS Sellers API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
# from .. import utils
from ..decorators import next_token_action


class Sellers(MWS):
    """
    Amazon MWS Sellers API
    """
    URI = '/Sellers/2011-07-01'
    VERSION = '2011-07-01'
    NAMESPACE = '{http://mws.amazonservices.com/schema/Sellers/2011-07-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListMarketplaceParticipations',
    ]

    @next_token_action('ListMarketplaceParticipations')
    def list_marketplace_participations(self, next_token=None):
        """
        Returns a list of marketplaces a seller can participate in and
        a list of participations that include seller-specific information in that marketplace.
        The operation returns only those marketplaces where the seller's account is
        in an active state.

        Run with `next_token` kwarg to call related "ByNextToken" action.
        """
        data = dict(Action='ListMarketplaceParticipations')
        return self.make_request(data)

    def list_marketplace_participations_by_next_token(self, token):
        """
        Deprecated.
        Use `list_marketplace_participations(next_token=token)` instead.
        """
        # data = dict(Action='ListMarketplaceParticipations', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_marketplace_participations(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_marketplace_participations(next_token=token)
