"""Amazon MWS Reports API."""
from enum import Enum
import datetime
import typing
from typing import List, Union

from mws import MWS, Marketplaces
from mws.utils.params import enumerate_param
from mws.utils.params import enumerate_params
from mws.utils.params import coerce_to_bool
from mws.decorators import next_token_action

# DEPRECATIONS
from mws.utils.deprecation import kwargs_renamed_for_v11


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
        output.append("{}={}".format(key, out_val))
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

    @kwargs_renamed_for_v11([("marketplaceids", "marketplace_ids")])
    def request_report(
        self,
        report_type: Union["ReportType", str],
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
        report_types: List[Union["ReportType", str]] = None,
        processing_statuses: List[Union["ProcessingStatus", str]] = None,
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
        report_types: List[Union["ReportType", str]] = None,
        processing_statuses: List[Union["ProcessingStatus", str]] = None,
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
        report_types: List[Union["ReportType", str]] = None,
        processing_statuses: List[Union["ProcessingStatus", str]] = None,
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
        report_types: List[Union["ReportType", str]] = None,
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
        report_types: List[Union["ReportType", str]] = None,
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
        report_type: "ReportType",
        schedule: "Schedule",
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
        report_types: List[Union["ReportType", str]] = None,
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
        report_types: List[Union["ReportType", str]] = None,
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


class ReportType(str, Enum):
    """An enumeration of the types of reports that can be requested from Amazon MWS.

    `MWS Docs: ReportType enumeration
    <https://docs.developer.amazonservices.com/en_US/reports/Reports_ReportType.html>`_
    """

    # Listing Reports
    INVENTORY = "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
    ACTIVE_LISTINGS = "_GET_MERCHANT_LISTINGS_DATA_"
    ALL_LISTINGS = "_GET_MERCHANT_LISTINGS_ALL_DATA_"
    OPEN_LISTINGS = "_GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT_"
    OPEN_LISTINGS_LITE = "_GET_MERCHANT_LISTINGS_DATA_LITE_"
    OPEN_LISTINGS_LITER = "_GET_MERCHANT_LISTINGS_DATA_LITER_"
    CANCELED_LISTINGS = "_GET_MERCHANT_CANCELLED_LISTINGS_DATA_"
    SOLD_LISTINGS = "_GET_CONVERGED_FLAT_FILE_SOLD_LISTINGS_DATA_"
    QUALITY_AND_SUPPRESSED = "_GET_MERCHANT_LISTINGS_DEFECT_DATA_"
    # Order Reports
    ORDERS_UNSHIPPED = "_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_"
    ORDERS_SCHEDULED_XML = "_GET_ORDERS_DATA_"
    ORDERS = "_GET_FLAT_FILE_ORDERS_DATA_"
    ORDERS_CONVERGED = "_GET_CONVERGED_FLAT_FILE_ORDER_REPORT_DATA_"
    # Order Tracking Reports
    TRACKING_BY_LAST_UPDATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    TRACKING_BY_ORDER_DATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    TRACKING_BY_LAST_UPDATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    TRACKING_BY_ORDER_DATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    # Pending Order Reports
    PENDING_ORDERS_FLAT_FILE = "_GET_FLAT_FILE_PENDING_ORDERS_DATA_"
    PENDING_ORDERS_XML = "_GET_PENDING_ORDERS_DATA_"
    PENDING_ORDERS_CONVERGED_FLAT_FILE = "_GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA_"
    # Performance Reports
    PERFORMANCE_FEEDBACK = "_GET_SELLER_FEEDBACK_DATA_"
    PERFORMANCE_CUSTOMER_METRICS_XML = "_GET_V1_SELLER_PERFORMANCE_REPORT_"
    # Settlement Reports
    SETTLEMENT = "_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_"
    SETTLEMENT_V2 = "_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2_"
    # Sales Tax Reports
    SALES_TAX = "_GET_FLAT_FILE_SALES_TAX_DATA_"  # only USA
    VAT_CALCULATION = "_SC_VAT_TAX_REPORT_"  # if activated amazon vat services
    VAT_TRANSACTIONS = "_GET_VAT_TRANSACTION_DATA_"
    # Browse Tree Reports
    BROWSE_TREE = "_GET_XML_BROWSE_TREE_DATA_"
    #####
    # Fulfillment By Amazon (FBA) Reports
    #####
    # FBA Sales Reports
    FBA_SALES_AMAZON_FULFILLED = "_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_"
    FBA_SALES_ALL_LAST_UPDATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    FBA_SALES_ALL_BY_ORDER_DATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    FBA_SALES_ALL_BY_LAST_UPDATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    FBA_SALES_ALL_BY_ORDER_DATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    FBA_SALES_CUSTOMER_SHIPMENT = "_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA_"
    FBA_SALES_PROMOTIONS = "_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_PROMOTION_DATA_"
    FBA_SALES_CUSTOMER_TAXES = "_GET_FBA_FULFILLMENT_CUSTOMER_TAXES_DATA_"
    # FBA Inventory Reports
    FBA_INVENTORY_AFN = "_GET_AFN_INVENTORY_DATA_"
    FBA_INVENTORY_AFN_BY_COUNTRY = (
        "_GET_AFN_INVENTORY_DATA_BY_COUNTRY_"  # unicode not working
    )
    FBA_INVENTORY_HISTORY_DAILY = "_GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA_"
    FBA_INVENTORY_HISTORY_MONTHLY = "_GET_FBA_FULFILLMENT_MONTHLY_INVENTORY_DATA_"
    FBA_INVENTORY_RECEIVED = "_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_"
    FBA_INVENTORY_RESERVED = "_GET_RESERVED_INVENTORY_DATA_"
    FBA_INVENTORY_EVENT_DETAIL = "_GET_FBA_FULFILLMENT_INVENTORY_SUMMARY_DATA_"
    FBA_INVENTORY_ADJUSTMENTS = "_GET_FBA_FULFILLMENT_INVENTORY_ADJUSTMENTS_DATA_"
    FBA_INVENTORY_HEALTH = "_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_"
    FBA_INVENTORY_MANAGE_ACTIVE = "_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_"
    FBA_INVENTORY_MANAGE_ALL = "_GET_FBA_MYI_ALL_INVENTORY_DATA_"
    FBA_INVENTORY_CROSS_BORDER_MOVEMENT = (
        "_GET_FBA_FULFILLMENT_CROSS_BORDER_INVENTORY_MOVEMENT_DATA_"
    )
    FBA_INVENTORY_INBOUND_PERFORMANCE = (
        "_GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA_"
    )
    FBA_INVENTORY_STRANDED = "_GET_STRANDED_INVENTORY_UI_DATA_"
    FBA_INVENTORY_BULK_FIX_STRANDED = "_GET_STRANDED_INVENTORY_LOADER_DATA_"
    FBA_INVENTORY_AGE = "_GET_FBA_INVENTORY_AGED_DATA_"
    FBA_INVENTORY_EXCESS = "_GET_EXCESS_INVENTORY_DATA_"
    # FBA Payments Reports
    FBA_PAYMENTS_FEE_PREVIEW = "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_"
    FBA_PAYMENTS_REIMBURSEMENTS = "_GET_FBA_REIMBURSEMENTS_DATA_"
    # FBA Customer Concessions Reports
    FBA_CONCESSION_RETURNS = "_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_"
    # FBA Removals Reports
    FBA_REMOVAL_RECOMMENDED = "_GET_FBA_RECOMMENDED_REMOVAL_DATA_"
    FBA_REMOVAL_ORDER_DETAIL = "_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_"
    FBA_REMOVAL_SHIPMENT_DETAIL = "_GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA_"


class Schedule(str, Enum):
    """An enumeration of the units of time that reports can be requested.

    `MWS Docs: Schedule enumeration
    <https://docs.developer.amazonservices.com/en_US/reports/Reports_Schedule.html>`_
    """

    # I've introduced what I think are useful names for these schedules,
    # but Amazon didn't seem to have a clear set of consistent naming rules.
    # So, I opted for a lot of aliases, providing several consistent series of options.
    # There are singular and plurals, minutes spelled out vs min, "weekly" as well as
    # "7 days" and "every 1 week", etc.
    # Weird bit at the 3-day mark where MWS chose to say "72 hours", but whatever.
    # Aliases are cheap, so here we go.

    # 15 minutes
    EVERY_15_MIN = "_15_MINUTES_"
    EVERY_15_MINS = "_15_MINUTES_"
    EVERY_15_MINUTE = "_15_MINUTES_"
    EVERY_15_MINUTES = "_15_MINUTES_"
    # 30 minutes
    EVERY_30_MIN = "_30_MINUTES_"
    EVERY_30_MINS = "_30_MINUTES_"
    EVERY_30_MINUTE = "_30_MINUTES_"
    EVERY_30_MINUTES = "_30_MINUTES_"
    # Hourly
    EVERY_HOUR = "_1_HOUR_"
    EVERY_1_HOUR = "_1_HOUR_"
    EVERY_1_HOURS = "_1_HOUR_"
    # 2 hours
    EVERY_2_HOUR = "_2_HOURS_"
    EVERY_2_HOURS = "_2_HOURS_"
    # 4 hours
    EVERY_4_HOUR = "_4_HOURS_"
    EVERY_4_HOURS = "_4_HOURS_"
    # 8 hours
    EVERY_8_HOUR = "_8_HOURS_"
    EVERY_8_HOURS = "_8_HOURS_"
    # 12 hours
    EVERY_12_HOUR = "_12_HOURS_"
    EVERY_12_HOURS = "_12_HOURS_"
    # 1 day
    DAILY = "_1_DAY_"
    EVERY_DAY = "_1_DAY_"
    EVERY_1_DAY = "_1_DAY_"
    EVERY_1_DAYS = "_1_DAY_"
    # 2 days
    EVERY_2_DAY = "_2_DAYS_"
    EVERY_2_DAYS = "_2_DAYS_"
    # Amazon chose to do 72 hours instead of "3 days" (see below),
    # so I'm adding a 48 for consistency.
    EVERY_48_HOUR = "_2_DAYS_"
    EVERY_48_HOURS = "_2_DAYS_"
    # 3 days
    EVERY_3_DAY = "_72_HOURS_"  # Don't ask me, it's their API.
    EVERY_3_DAYS = "_72_HOURS_"
    EVERY_72_HOUR = "_72_HOURS_"
    EVERY_72_HOURS = "_72_HOURS_"
    # 1 week
    WEEKLY = "_1_WEEK_"
    EVERY_WEEK = "_1_WEEK_"
    EVERY_1_WEEK = "_1_WEEK_"
    EVERY_1_WEEKS = "_1_WEEK_"
    EVERY_7_DAY = "_1_WEEK_"
    EVERY_7_DAYS = "_1_WEEK_"
    # 2 weeks
    EVERY_14_DAY = "_14_DAYS_"  # Again with the inconsistency
    EVERY_14_DAYS = "_14_DAYS_"
    EVERY_2_WEEK = "_14_DAYS_"
    EVERY_2_WEEKS = "_14_DAYS_"
    FORTNIGHTLY = "_14_DAYS_"  # Makes sense for some
    # 15 days
    # Technically 'semi-monthly' makes sense here, too,
    # but the definition of that is not 15 days. So, skip it.
    EVERY_15_DAY = "_15_DAYS_"
    EVERY_15_DAYS = "_15_DAYS_"
    # 30 days
    EVERY_30_DAY = "_30_DAYS_"
    EVERY_30_DAYS = "_30_DAYS_"

    DELETE = "_NEVER_"
    """Delete a previously created report request schedule."""


class ProcessingStatus(str, Enum):
    """An optional enumeration of common processing_status values."""

    SUBMITTED = "_SUBMITTED_"
    IN_PROGRESS = "_IN_PROGRESS_"
    CANCELLED = "_CANCELLED_"
    CANCELED = "_CANCELLED_"
    """An alias for "CANCELLED", as some folks spell it with one L and
    there's nothing wrong with that.
    """

    DONE = "_DONE_"
    DONE_NO_DATA = "_DONE_NO_DATA_"


# Attach the Enums to the Reports API for convenience.
Reports.ReportType = ReportType
Reports.Schedule = Schedule
Reports.ProcessingStatus = ProcessingStatus
