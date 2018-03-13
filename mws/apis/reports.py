"""
Amazon MWS Reports API
"""
from __future__ import absolute_import

import mws
from .. import utils
from ..decorators import next_token_action

# TODO Add ReportType enumerations as constants
# TODO Add Schedule enumerations as constants


class Reports(mws.MWS):
    """
    Amazon MWS Reports API

    Docs:
    http://docs.developer.amazonservices.com/en_US/reports/Reports_Overview.html
    """
    ACCOUNT_TYPE = "Merchant"
    NEXT_TOKEN_OPERATIONS = [
        'GetReportRequestList',
        'GetReportList',
        'GetReportScheduleList',
    ]

    def request_report(self, report_type, start_date=None, end_date=None, marketplaceids=()):
        """
        Creates a report request and submits the request to Amazon MWS.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_RequestReport.html
        """
        data = {
            'Action': 'RequestReport',
            'ReportType': report_type,
            'StartDate': start_date,
            'EndDate': end_date,
        }
        data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        return self.make_request(data)

    @next_token_action('GetReportRequestList')
    def get_report_request_list(self, requestids=(), types=(), processingstatuses=(),
                                max_count=None, fromdate=None, todate=None, next_token=None):
        """
        Returns a list of report requests that you can use to get the ReportRequestId for a report.

        Pass `next_token` to call "GetReportRequestListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestList.html
        """
        data = {
            'Action': 'GetReportRequestList',
            'MaxCount': max_count,
            'RequestedFromDate': fromdate,
            'RequestedToDate': todate,
        }
        data.update(utils.enumerate_params({
            'ReportRequestIdList.Id.': requestids,
            'ReportTypeList.Type.': types,
            'ReportProcessingStatusList.Status.': processingstatuses,
        }))
        return self.make_request(data)

    def get_report_request_list_by_next_token(self, token):
        """
        Alias for `get_report_request_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestListByNextToken.html
        """
        return self.get_report_request_list(next_token=token)

    def get_report_request_count(self, report_types=(), processingstatuses=(),
                                 fromdate=None, todate=None):
        """
        Returns a count of report requests that have been submitted to Amazon MWS for processing.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestCount.html
        """
        data = {
            'Action': 'GetReportRequestCount',
            'RequestedFromDate': fromdate,
            'RequestedToDate': todate,
        }
        data.update(utils.enumerate_params({
            'ReportTypeList.Type.': report_types,
            'ReportProcessingStatusList.Status.': processingstatuses,
        }))
        return self.make_request(data)

    # # TODO Add:
    # def cancel_report_requests(self):
    #     pass

    @next_token_action('GetReportList')
    def get_report_list(self, requestids=(), max_count=None, types=(), acknowledged=None,
                        fromdate=None, todate=None, next_token=None):
        """
        Returns a list of reports that were created between fromdate and todate
        (defaults to previous 90 days if ommitted).

        Pass `next_token` to call "GetReportListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportList.html
        """
        data = {
            'Action': 'GetReportList',
            'Acknowledged': acknowledged,
            'AvailableFromDate': fromdate,
            'AvailableToDate': todate,
            'MaxCount': max_count,
        }
        data.update(utils.enumerate_params({
            'ReportRequestIdList.Id.': requestids,
            'ReportTypeList.Type.': types,
        }))
        return self.make_request(data)

    def get_report_list_by_next_token(self, token):
        """
        Alias for `get_report_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportListByNextToken.html
        """
        return self.get_report_list(next_token=token)

    def get_report_count(self, report_types=(), acknowledged=None, fromdate=None, todate=None):
        """
        Returns a count of the reports, created in the previous 90 days,
        with a status of _DONE_ and that are available for download.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportCount.html
        """
        data = {
            'Action': 'GetReportCount',
            'Acknowledged': acknowledged,
            'AvailableFromDate': fromdate,
            'AvailableToDate': todate,
        }
        data.update(utils.enumerate_param('ReportTypeList.Type.', report_types))
        return self.make_request(data)

    def get_report(self, report_id):
        """
        Returns the contents of a report and the Content-MD5 header for the returned report body.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReport.html
        """
        data = {
            'Action': 'GetReport',
            'ReportId': report_id,
        }
        return self.make_request(data)

    # # TODO Add:
    # def manage_report_schedule(self):
    #     pass

    @next_token_action('GetReportScheduleList')
    def get_report_schedule_list(self, types=(), next_token=None):
        """
        Returns a list of order report requests that are scheduled to be submitted to Amazon MWS for processing.

        Pass `next_token` to call "GetReportScheduleListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleList.html
        """
        data = {
            'Action': 'GetReportScheduleList',
        }
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    def get_report_schedule_list_by_next_token(self, token):
        """
        Alias for `get_report_schedule_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleListByNextToken.html
        """
        return self.get_report_schedule_list(next_token=token)

    def get_report_schedule_count(self, types=()):
        """
        Returns a count of order report requests that are scheduled to be submitted to Amazon MWS.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleCount.html
        """
        data = {
            'Action': 'GetReportScheduleCount',
        }
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    # # TODO Add:
    # def update_report_acknowledgements(self):
    #     pass
