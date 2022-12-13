"""Amazon MWS Reports API."""
import datetime
import typing
from enum import Enum
from typing import List, Union

from mws import MWS, Marketplaces
from mws.decorators import next_token_action
from mws.models import reports as models

# DEPRECATIONS
from mws.utils.deprecation import kwargs_renamed_for_v11
from mws.utils.params import coerce_to_bool, enumerate_param, enumerate_params

DateType = Union["datetime.datetime", "datetime.date"]


def report_options_str(report_options: dict) -> str:
    """Given a set of `report_options` as a dict,
    converts those options to a URL-encoded string.

    Each key-value pair in the dict is presented as "key=value", which is then URL-encoded
    to, for instance, "key%3Dvalue". Key-value pairs are then joined with ";".

    See examples in the
    `ReportType_Enumeration docs <https://docs.developer.amazonservices.com/en_US/reports/Reports_ReportType.html>`_
    for details.
    """
    if not report_options:
        return None
    if not isinstance(report_options, dict):
        raise ValueError("`report_options` must be a dict.")
    output = []
    for key, val in report_options.items():
        out_val = val
        if out_val is True or out_val is False:
            # Value is explicitly `True` or `False`.
            # The `is` identity check is necessary, otherwise `1 == True` and `0 == False`
            # (both of which are accurate, because True and False can evaluate to ints 1 and 0).
            # `True` and `False` must be output as a lowercase `"true"` and `"false"`, respectively.
            out_val = str(out_val).lower()
        output.append(f"{key}={out_val}")
    # Join results with ";" separator
    return ";".join(output)


class Reports(MWS):
    """Amazon MWS Reports API.

    `MWS Docs: Reports API Overview
    <https://docs.developer.amazonservices.com/en_US/reports/Reports_Overview.html>`_
    """

    URI = "/Reports/2009-01-01"
    ACCOUNT_TYPE = "Merchant"
    NEXT_TOKEN_OPERATIONS = [
        "GetReportRequestList",
        "GetReportList",
        "GetReportScheduleList",
    ]

    # Models attached to this API
    ReportType = models.ReportType
    ProcessingStatus = models.ProcessingStatus
    Schedule = models.Schedule

    @kwargs_renamed_for_v11([("marketplaceids", "marketplace_ids")])
    def request_report(
        self,
        report_type: Union[models.ReportType, str],
        start_date: DateType = None,
        end_date: DateType = None,
        marketplace_ids: List[Union[Marketplaces, str]] = None,
        report_options: dict = None,
    ):
        """Creates a report request and submits the request to Amazon MWS.

        `MWS Docs: RequestReport
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_RequestReport.html>`_
        """
        marketplace_ids = marketplace_ids or []
        report_options = report_options or {}
        data = {
            "ReportType": report_type,
            "StartDate": start_date,
            "EndDate": end_date,
            "ReportOptions": report_options_str(report_options),
        }
        data.update(enumerate_param("MarketplaceIdList.Id.", marketplace_ids))
        return self.make_request("RequestReport", data)

    @kwargs_renamed_for_v11(
        [
            ("requestids", "request_ids"),
            ("types", "report_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
    )
    @next_token_action("GetReportRequestList")
    def get_report_request_list(
        self,
        request_ids: List[str] = None,
        report_types: List[Union[models.ReportType, str]] = None,
        processing_statuses: List[Union[models.ProcessingStatus, str]] = None,
        max_count: int = None,
        from_date: DateType = None,
        to_date: DateType = None,
        next_token: str = None,
    ):
        """Returns a list of report requests that you can use
        to get the ReportRequestId for a report.

        Pass ``next_token`` with no other arguments to call the
        **GetReportRequestListByNextToken** operation, requesting the next page of results.

        `MWS Docs: GetReportRequestList
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestList.html>`_
        """
        request_ids = request_ids or []
        report_types = report_types or []
        processing_statuses = processing_statuses or []
        data = {
            "MaxCount": max_count,
            "RequestedFromDate": from_date,
            "RequestedToDate": to_date,
        }
        data.update(
            enumerate_params(
                {
                    "ReportRequestIdList.Id.": request_ids,
                    "ReportTypeList.Type.": report_types,
                    "ReportProcessingStatusList.Status.": processing_statuses,
                }
            )
        )
        return self.make_request("GetReportRequestList", data)

    def get_report_request_list_by_next_token(self, token: str):
        """Alias for ``get_report_request_list(next_token=token)``.

        `MWS Docs: GetReportRequestListByNextToken
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestListByNextToken.html>`_
        """
        return self.get_report_request_list(next_token=token)

    @kwargs_renamed_for_v11(
        [
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
    )
    def get_report_request_count(
        self,
        report_types: List[Union[models.ReportType, str]] = None,
        processing_statuses: List[Union[models.ProcessingStatus, str]] = None,
        from_date: DateType = None,
        to_date: DateType = None,
    ):
        """Returns a count of report requests that have been submitted
        to Amazon MWS for processing.

        `MWS Docs: GetReportRequestCount
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportRequestCount.html>`_
        """
        report_types = report_types or []
        processing_statuses = processing_statuses or []
        data = {
            "RequestedFromDate": from_date,
            "RequestedToDate": to_date,
        }
        data.update(
            enumerate_params(
                {
                    "ReportTypeList.Type.": report_types,
                    "ReportProcessingStatusList.Status.": processing_statuses,
                }
            )
        )
        return self.make_request("GetReportRequestCount", data)

    def cancel_report_requests(
        self,
        request_ids: List[str] = None,
        report_types: List[Union[models.ReportType, str]] = None,
        processing_statuses: List[Union[models.ProcessingStatus, str]] = None,
        from_date: DateType = None,
        to_date: DateType = None,
    ):
        """Cancels one or more report requests.

        `MWS Docs: CancelReportRequests
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_CancelReportRequests.html>`_
        """
        request_ids = request_ids or []
        report_types = report_types or []
        processing_statuses = processing_statuses or []
        data = {
            "RequestedFromDate": from_date,
            "RequestedToDate": to_date,
        }
        data.update(
            enumerate_params(
                {
                    "ReportRequestIdList.Id.": request_ids,
                    "ReportTypeList.Type.": report_types,
                    "ReportProcessingStatusList.Status.": processing_statuses,
                }
            )
        )
        return self.make_request("CancelReportRequests", data)

    @kwargs_renamed_for_v11(
        [
            ("requestids", "request_ids"),
            ("types", "report_types"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
    )
    @next_token_action("GetReportList")
    def get_report_list(
        self,
        request_ids: List[str] = None,
        max_count: int = None,
        report_types: List[Union[models.ReportType, str]] = None,
        acknowledged: bool = None,
        from_date: DateType = None,
        to_date: DateType = None,
        next_token: str = None,
    ):
        """Returns a list of reports that were created between fromdate and todate
        (defaults to previous 90 days if ommitted).

        Pass ``next_token`` with no other arguments to call the
        **GetReportListByNextToken** operation, requesting the next page of results.

        `MWS Docs: GetReportList
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportList.html>`_
        """
        request_ids = request_ids or []
        report_types = report_types or []
        if acknowledged is not None:
            acknowledged = coerce_to_bool(acknowledged)
        data = {
            "Acknowledged": acknowledged,
            "AvailableFromDate": from_date,
            "AvailableToDate": to_date,
            "MaxCount": max_count,
        }
        data.update(
            enumerate_params(
                {
                    "ReportRequestIdList.Id.": request_ids,
                    "ReportTypeList.Type.": report_types,
                }
            )
        )
        return self.make_request("GetReportList", data)

    def get_report_list_by_next_token(self, token: str):
        """Alias for ``get_report_list(next_token=token)``.

        `MWS Docs: GetReportListByNextToken
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportListByNextToken.html>`_
        """
        return self.get_report_list(next_token=token)

    @kwargs_renamed_for_v11([("fromdate", "from_date"), ("todate", "to_date")])
    def get_report_count(
        self,
        report_types: List[Union[models.ReportType, str]] = None,
        acknowledged: bool = None,
        from_date: DateType = None,
        to_date: DateType = None,
    ):
        """Returns a count of the reports, created in the previous 90 days,
        with a status of _DONE_ and that are available for download.

        `MWS Docs: GetReportCount
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportCount.html>`_
        """
        report_types = report_types or []
        if acknowledged is not None:
            acknowledged = coerce_to_bool(acknowledged)
        data = {
            "Acknowledged": acknowledged,
            "AvailableFromDate": from_date,
            "AvailableToDate": to_date,
        }
        data.update(enumerate_param("ReportTypeList.Type.", report_types))
        return self.make_request("GetReportCount", data)

    def get_report(self, report_id: str):
        """Returns the contents of a report and the Content-MD5 header for the returned report body.

        `MWS Docs: GetReport
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReport.html>`_
        """
        return self.make_request("GetReport", {"ReportId": report_id})

    def manage_report_schedule(
        self,
        report_type: models.ReportType,
        schedule: models.Schedule,
        schedule_date: DateType = None,
    ):
        """Creates, updates, or deletes a report request schedule for a specified report type.

        `MWS Docs: ManageReportSchedule
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_ManageReportSchedule.html>`_
        """
        data = {
            "ReportType": report_type,
            "Schedule": schedule,
            "ScheduleDate": schedule_date,
        }
        return self.make_request("ManageReportSchedule", data)

    @kwargs_renamed_for_v11([("types", "report_types")])
    @next_token_action("GetReportScheduleList")
    def get_report_schedule_list(
        self,
        report_types: List[Union[models.ReportType, str]] = None,
        next_token: str = None,
    ):
        """Returns a list of order report requests that are scheduled
        to be submitted to Amazon MWS for processing.

        Pass ``next_token`` with no other arguments to call the
        **GetReportScheduleListByNextToken** operation, requesting the next page of results.

        `MWS Docs: GetReportScheduleList
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleList.html>`_
        """
        report_types = report_types or []
        data = enumerate_param("ReportTypeList.Type.", report_types)
        return self.make_request("GetReportScheduleList", data)

    def get_report_schedule_list_by_next_token(self, token: str):
        """Alias for ``get_report_schedule_list(next_token=token)``.

        `MWS Docs: GetReportScheduleListByNextToken
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleListByNextToken.html>`_
        """
        return self.get_report_schedule_list(next_token=token)

    @kwargs_renamed_for_v11([("types", "report_types")])
    def get_report_schedule_count(
        self,
        report_types: List[Union[models.ReportType, str]] = None,
    ):
        """Returns a count of order report requests that are scheduled to be submitted to Amazon MWS.

        `MWS Docs: GetReportScheduleCount
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_GetReportScheduleCount.html>`_
        """
        report_types = report_types or []
        data = enumerate_param("ReportTypeList.Type.", report_types)
        return self.make_request("GetReportScheduleCount", data)

    def update_report_acknowledgements(
        self,
        report_ids: List[str] = None,
        acknowledged: bool = None,
    ):
        """Updates the acknowledged status of one or more reports.

        `MWS Docs: UpdateReportAcknowledgements
        <https://docs.developer.amazonservices.com/en_US/reports/Reports_UpdateReportAcknowledgements.html>`_
        """
        report_ids = report_ids or []
        if acknowledged is not None:
            acknowledged = coerce_to_bool(acknowledged)
        data = {"Acknowledged": acknowledged}
        data.update(enumerate_param("ReportIdList.Id.", report_ids))
        return self.make_request("UpdateReportAcknowledgements", data)
