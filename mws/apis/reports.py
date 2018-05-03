"""
Amazon MWS Reports API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action

# TODO Add ReportType enumerations as constants
# TODO Add Schedule enumerations as constants


class Reports(MWS):
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

    def request_report(self, report_type, start_date=None, end_date=None, marketplace_ids=None):
        """
        Creates a report request and submits the request to Amazon MWS.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_RequestReport.html
        """
        marketplace_ids = marketplace_ids or []
        data = {
            'Action': 'RequestReport',
            'ReportType': report_type,
            'StartDate': start_date,
            'EndDate': end_date,
        }
        data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplace_ids))
        return self.make_request(data)

    @next_token_action('GetReportRequestList')
    def get_report_request_list(self, request_ids=None, report_types=None, processing_statuses=None,
                                max_count=None, from_date=None, to_date=None, next_token=None):
        """
        Returns a list of report requests that you can use to get the ReportRequestId for a report.

        Pass `next_token` to call "GetReportRequestListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestList.html
        """
        request_ids = request_ids or []
        report_types = report_types or []
        processing_statuses = processing_statuses or []
        data = {
            'Action': 'GetReportRequestList',
            'MaxCount': max_count,
            'RequestedFromDate': from_date,
            'RequestedToDate': to_date,
        }
        data.update(utils.enumerate_params({
            'ReportRequestIdList.Id.': request_ids,
            'ReportTypeList.Type.': report_types,
            'ReportProcessingStatusList.Status.': processing_statuses,
        }))
        return self.make_request(data)

    def get_report_request_list_by_next_token(self, token):
        """
        Alias for `get_report_request_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestListByNextToken.html
        """
        return self.get_report_request_list(next_token=token)

    def get_report_request_count(self, report_types=None, processing_statuses=None,
                                 from_date=None, to_date=None):
        """
        Returns a count of report requests that have been submitted to Amazon MWS for processing.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestCount.html
        """
        report_types = report_types or []
        processing_statuses = processing_statuses or []
        data = {
            'Action': 'GetReportRequestCount',
            'RequestedFromDate': from_date,
            'RequestedToDate': to_date,
        }
        data.update(utils.enumerate_params({
            'ReportTypeList.Type.': report_types,
            'ReportProcessingStatusList.Status.': processing_statuses,
        }))
        return self.make_request(data)

    # # TODO Add:
    # def cancel_report_requests(self):
    #     pass

    @next_token_action('GetReportList')
    def get_report_list(self, request_ids=None, max_count=None, report_types=None, acknowledged=None,
                        from_date=None, to_date=None, next_token=None):
        """
        Returns a list of reports that were created between fromdate and todate
        (defaults to previous 90 days if ommitted).

        Pass `next_token` to call "GetReportListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportList.html
        """
        request_ids = request_ids or []
        report_types = report_types or []
        data = {
            'Action': 'GetReportList',
            'Acknowledged': acknowledged,
            'AvailableFromDate': from_date,
            'AvailableToDate': to_date,
            'MaxCount': max_count,
        }
        data.update(utils.enumerate_params({
            'ReportRequestIdList.Id.': request_ids,
            'ReportTypeList.Type.': report_types,
        }))
        return self.make_request(data)

    def get_report_list_by_next_token(self, token):
        """
        Alias for `get_report_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportListByNextToken.html
        """
        return self.get_report_list(next_token=token)

    def get_report_count(self, report_types=None, acknowledged=None, from_date=None, to_date=None):
        """
        Returns a count of the reports, created in the previous 90 days,
        with a status of _DONE_ and that are available for download.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportCount.html
        """
        report_types = report_types or []
        data = {
            'Action': 'GetReportCount',
            'Acknowledged': acknowledged,
            'AvailableFromDate': from_date,
            'AvailableToDate': to_date,
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
    def get_report_schedule_list(self, report_types=None, next_token=None):
        """
        Returns a list of order report requests that are scheduled to be submitted to Amazon MWS for processing.

        Pass `next_token` to call "GetReportScheduleListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleList.html
        """
        report_types = report_types or []
        data = {
            'Action': 'GetReportScheduleList',
        }
        data.update(utils.enumerate_param('ReportTypeList.Type.', report_types))
        return self.make_request(data)

    def get_report_schedule_list_by_next_token(self, token):
        """
        Alias for `get_report_schedule_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleListByNextToken.html
        """
        return self.get_report_schedule_list(next_token=token)

    def get_report_schedule_count(self, report_types=None):
        """
        Returns a count of order report requests that are scheduled to be submitted to Amazon MWS.

        Docs:
        http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleCount.html
        """
        report_types = report_types or []
        data = {
            'Action': 'GetReportScheduleCount',
        }
        data.update(utils.enumerate_param('ReportTypeList.Type.', report_types))
        return self.make_request(data)

    # # TODO Add:
    # def update_report_acknowledgements(self):
    #     pass
