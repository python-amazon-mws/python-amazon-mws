"""
Tests for the Finances API class.
"""
import unittest
import datetime
import mws
from .utils import CommonRequestTestTools


class FinancesTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Finances.
    """
    # TODO: Add remaining methods for Finances
    def setUp(self):
        self.api = mws.Finances(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_list_financial_event_groups(self):
        """
        ListFinancialEventGroups operation.
        """
        created_after = datetime.datetime.utcnow()
        created_after_stamp = created_after.isoformat()
        created_before = datetime.datetime.utcnow()
        created_before_stamp = created_before.isoformat()
        max_results = 659
        params = self.api.list_financial_event_groups(
            created_after=created_after,
            created_before=created_before,
            max_results=max_results,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEventGroups')
        self.assertEqual(params['FinancialEventGroupStartedAfter'], created_after_stamp)
        self.assertEqual(params['FinancialEventGroupStartedBefore'], created_before_stamp)
        self.assertEqual(params['MaxResultsPerPage'], max_results)

    def test_list_financial_event_groups_by_next_token(self):
        """
        ListFinancialEventGroupsByNextToken operation, via method decorator.
        """
        next_token = 'VcNq06R0dO'
        params = self.api.list_financial_event_groups(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEventGroupsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_financial_event_groups_by_next_token_alias(self):
        """
        ListFinancialEventGroupsByNextToken operation, via alias method.
        """
        next_token = 'uhEPBAvUYR'
        params = self.api.list_financial_event_groups_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEventGroupsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_financial_events(self):
        """
        ListFinancialEvents operation.
        """
        posted_after = datetime.datetime.utcnow()
        posted_after_stamp = posted_after.isoformat()
        posted_before = datetime.datetime.utcnow()
        posted_before_stamp = posted_before.isoformat()
        amazon_order_id = '123-4567890-1234567'
        financial_event_group_id = '22YgYW55IGNhcm5hbCBwbGVhEXAMPLE'
        max_results = 156
        params = self.api.list_financial_events(
            financial_event_group_id=financial_event_group_id,
            amazon_order_id=amazon_order_id,
            posted_after=posted_after,
            posted_before=posted_before,
            max_results=max_results,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEvents')
        self.assertEqual(params['FinancialEventGroupId'], financial_event_group_id)
        self.assertEqual(params['AmazonOrderId'], amazon_order_id)
        self.assertEqual(params['PostedAfter'], posted_after_stamp)
        self.assertEqual(params['PostedBefore'], posted_before_stamp)
        self.assertEqual(params['MaxResultsPerPage'], max_results)

    def test_list_financial_events_by_next_token(self):
        """
        ListFinancialEventsByNextToken operation, via method decorator.
        """
        next_token = '2t1DdnGqgf'
        params = self.api.list_financial_events(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEventsByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_list_financial_events_by_next_token_alias(self):
        """
        ListFinancialEventsByNextToken operation, via alias method.
        """
        next_token = '7Ijm9Kmrgp'
        params = self.api.list_financial_events_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListFinancialEventsByNextToken')
        self.assertEqual(params['NextToken'], next_token)
