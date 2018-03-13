"""
Tests for the Reports API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools


class ReportsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Reports.
    """
    # TODO: Add remaining methods for Reports
    def setUp(self):
        self.api = mws.Reports(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_request_report(self):
        """
        RequestReport operation.
        """
        pass

    def test_get_report_request_list(self):
        """
        GetReportRequestList operation.
        """
        pass

    def test_get_report_request_list_by_next_token(self):
        """
        GetReportRequestListByNextToken operation, via method decorator.
        """
        next_token = 'RXmLZ2bEgE'
        params = self.api.get_report_request_list(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportRequestListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_request_list_by_next_token_alias(self):
        """
        GetReportRequestListByNextToken operation, via alias method.
        """
        next_token = '0hytxbkaOb'
        params = self.api.get_report_request_list_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportRequestListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_request_count(self):
        """
        GetReportRequestCount operation.
        """
        pass

    def test_get_report_list(self):
        """
        GetReportList operation.
        """
        pass

    def test_get_report_list_by_next_token(self):
        """
        GetReportListByNextToken operation, via method decorator.
        """
        next_token = '5u6Of2fS8B'
        params = self.api.get_report_list(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_list_by_next_token_alias(self):
        """
        GetReportListByNextToken operation, via alias method.
        """
        next_token = '3TczcliCkb'
        params = self.api.get_report_list_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_count(self):
        """
        GetReportCount operation.
        """
        pass

    def test_get_report(self):
        """
        GetReport operation.
        """
        pass

    def test_get_report_schedule_list(self):
        """
        GetReportScheduleList operation.
        """
        pass

    def test_get_report_schedule_list_by_next_token(self):
        """
        GetReportScheduleListByNextToken operation, via method decorator.
        """
        next_token = 'Yj3hOfPcIE'
        params = self.api.get_report_schedule_list(next_token=next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportScheduleListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_schedule_list_by_next_token_alias(self):
        """
        GetReportScheduleListByNextToken operation, via alias method.
        """
        next_token = 'SAlt4JwJGv'
        params = self.api.get_report_schedule_list_by_next_token(next_token)
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetReportScheduleListByNextToken')
        self.assertEqual(params['NextToken'], next_token)

    def test_get_report_schedule_count(self):
        """
        GetReportScheduleCount operation.
        """
        pass

    # # TODO Complete when method is available in Reports
    # def test_update_report_acknowledgements(self):
    #     """
    #     UpdateReportAcknowledgements operation.
    #     """
    #     pass
