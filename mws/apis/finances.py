"""
Amazon MWS Finances API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
# from .. import utils
from ..decorators import next_token_action


class Finances(MWS):
    """
    Amazon MWS Finances API
    """
    URI = "/Finances/2015-05-01"
    VERSION = "2015-05-01"
    NS = '{https://mws.amazonservices.com/Finances/2015-05-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListFinancialEventGroups',
        'ListFinancialEvents',
    ]

    @next_token_action('ListFinancialEventGroups')
    def list_financial_event_groups(self, created_after=None, created_before=None, max_results=None, next_token=None):
        """
        Returns a list of financial event groups
        """
        data = dict(
            Action='ListFinancialEventGroups',
            FinancialEventGroupStartedAfter=created_after,
            FinancialEventGroupStartedBefore=created_before,
            MaxResultsPerPage=max_results,
        )
        return self.make_request(data)

    def list_financial_event_groups_by_next_token(self, token):
        """
        Deprecated.
        Use `list_financial_event_groups(next_token=token)` instead.
        """
        warnings.warn(
            "Use `list_financial_event_groups(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_financial_event_groups(next_token=token)

    @next_token_action('ListFinancialEvents')
    def list_financial_events(self, financial_event_group_id=None, amazon_order_id=None, posted_after=None,
                              posted_before=None, max_results=None, next_token=None):
        """
        Returns financial events for a user-provided FinancialEventGroupId or AmazonOrderId
        """
        data = dict(
            Action='ListFinancialEvents',
            FinancialEventGroupId=financial_event_group_id,
            AmazonOrderId=amazon_order_id,
            PostedAfter=posted_after,
            PostedBefore=posted_before,
            MaxResultsPerPage=max_results,
        )
        return self.make_request(data)

    def list_financial_events_by_next_token(self, token):
        """
        Deprecated.
        Use `list_financial_events(next_token=token)` instead.
        """
        warnings.warn(
            "Use `list_financial_events(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_financial_events(next_token=token)
