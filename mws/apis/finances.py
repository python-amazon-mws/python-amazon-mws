"""Amazon MWS Finances API."""

from mws import MWS
from mws.decorators import next_token_action


class Finances(MWS):
    """Amazon MWS Finances API

    Docs:
    https://docs.developer.amazonservices.com/en_US/finances/Finances_Overview.html
    """

    URI = "/Finances/2015-05-01"
    VERSION = "2015-05-01"
    NS = "{https://mws.amazonservices.com/Finances/2015-05-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListFinancialEventGroups",
        "ListFinancialEvents",
    ]

    @next_token_action("ListFinancialEventGroups")
    def list_financial_event_groups(
        self, created_after=None, created_before=None, max_results=None, next_token=None
    ):
        """Returns financial event groups for a given date range.
        If `created_before` is ommitted, defaults to now minus 2 minutes.

        Pass `next_token` to call "ListFinancialEventGroupsByNextToken" instead.

        Docs:
        https://docs.developer.amazonservices.com/en_US/finances/Finances_ListFinancialEventGroups.html
        """
        return self.make_request(
            "ListFinancialEventGroups",
            {
                "FinancialEventGroupStartedAfter": created_after,
                "FinancialEventGroupStartedBefore": created_before,
                "MaxResultsPerPage": max_results,
            },
        )

    def list_financial_event_groups_by_next_token(self, token):
        """Alias for `list_financial_event_groups(next_token=token)`.

        Docs:
        https://docs.developer.amazonservices.com/en_US/finances/Finances_ListFinancialEventGroupsByNextToken.html
        """
        return self.list_financial_event_groups(next_token=token)

    @next_token_action("ListFinancialEvents")
    def list_financial_events(
        self,
        financial_event_group_id=None,
        amazon_order_id=None,
        posted_after=None,
        posted_before=None,
        max_results=None,
        next_token=None,
    ):
        """Returns financial events for a user-provided
        FinancialEventGroupId or AmazonOrderId

        Pass `next_token` to call "ListFinancialEventsByNextToken" instead

        Docs:
        https://docs.developer.amazonservices.com/en_US/finances/Finances_ListFinancialEvents.html
        """
        return self.make_request(
            "ListFinancialEvents",
            {
                "FinancialEventGroupId": financial_event_group_id,
                "AmazonOrderId": amazon_order_id,
                "PostedAfter": posted_after,
                "PostedBefore": posted_before,
                "MaxResultsPerPage": max_results,
            },
        )

    def list_financial_events_by_next_token(self, token):
        """Alias for `list_financial_events(next_token=token)`

        Docs:
        https://docs.developer.amazonservices.com/en_US/finances/Finances_ListFinancialEventsByNextToken.html
        """
        return self.list_financial_events(next_token=token)
