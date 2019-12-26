"""
Amazon MWS Reports API
"""
from __future__ import absolute_import
from enum import Enum

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action

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


class ReportType(Enum):
    """Better names for reports."""

    # Listing Reports
    INVENTORY = '_GET_FLAT_FILE_OPEN_LISTINGS_DATA_'
    ACTIVE_LISTINGS = '_GET_MERCHANT_LISTINGS_DATA_'
    OPEN_LISTINGS = '_GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT_'
    OPEN_LISTINGS_LITE = '_GET_MERCHANT_LISTINGS_DATA_LITE_'
    OPEN_LISTINGS_LITER = '_GET_MERCHANT_LISTINGS_DATA_LITER_'
    CANCELED_LISTINGS = '_GET_MERCHANT_CANCELLED_LISTINGS_DATA_'
    SOLD_LISTINGS = '_GET_CONVERGED_FLAT_FILE_SOLD_LISTINGS_DATA_'
    QUALITY_AND_SUPPRESSED = '_GET_MERCHANT_LISTINGS_DEFECT_DATA_'
    # Order Reports
    ORDERS_UNSHIPPED = '_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_'
    ORDERS_SCHEDULED_XML = '_GET_ORDERS_DATA_'
    ORDERS = '_GET_FLAT_FILE_ORDERS_DATA_'
    ORDERS_CONVERGED = '_GET_CONVERGED_FLAT_FILE_ORDER_REPORT_DATA_'
    # Order Tracking Reports
    TRACKING_BY_LAST_UPDATE = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_'
    TRACKING_BY_ORDER_DATE = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'
    TRACKING_BY_LAST_UPDATE_XML = '_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_'
    TRACKING_BY_ORDER_DATE_XML = '_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_'
    # Pending Order Reports
    PENDING_ORDERS_FLAT_FILE = '_GET_FLAT_FILE_PENDING_ORDERS_DATA_'
    PENDING_ORDERS_XML = '_GET_PENDING_ORDERS_DATA_'
    PENDING_ORDERS_CONVERGED_FLAT_FILE = '_GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA_'
    # Performance Reports
    PERFORMANCE_FEEDBACK = '_GET_SELLER_FEEDBACK_DATA_'
    PERFORMANCE_CUSTOMER_METRICS_XML = '_GET_V1_SELLER_PERFORMANCE_REPORT_'
    # Settlement Reports
    SETTLEMENT = '_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_'
    SETTLEMENT_V2 = '_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2_'
    # Sales Tax Reports
    SALES_TAX = '_GET_FLAT_FILE_SALES_TAX_DATA_'  # only USA
    VAT_CALCULATION = '_SC_VAT_TAX_REPORT_'  # if activated amazon vat services
    VAT_TRANSACTIONS = '_GET_VAT_TRANSACTION_DATA_'
    # Browse Tree Reports
    BROWSE_TREE = '_GET_XML_BROWSE_TREE_DATA_'
    #####
    # Fulfillment By Amazon (FBA) Reports
    #####
    # FBA Sales Reports
    FBA_SALES_AMAZON_FULFILLED = '_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_'
    FBA_SALES_ALL_LAST_UPDATE = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_'
    FBA_SALES_ALL_BY_ORDER_DATE = '_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_'
    FBA_SALES_ALL_BY_LAST_UPDATE_XML = '_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_'
    FBA_SALES_ALL_BY_ORDER_DATE_XML = '_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_'
    FBA_SALES_CUSTOMER_SHIPMENT = '_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA_'
    FBA_SALES_PROMOTIONS = '_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_PROMOTION_DATA_'
    FBA_SALES_CUSTOMER_TAXES = '_GET_FBA_FULFILLMENT_CUSTOMER_TAXES_DATA_'
    # FBA Inventory Reports
    FBA_INVENTORY_AFN = '_GET_AFN_INVENTORY_DATA_'
    FBA_INVENTORY_AFN_BY_COUNTRY = '_GET_AFN_INVENTORY_DATA_BY_COUNTRY_'  # unicode not working
    FBA_INVENTORY_HISTORY_DAILY = '_GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA_'
    FBA_INVENTORY_HISTORY_MONTHLY = '_GET_FBA_FULFILLMENT_MONTHLY_INVENTORY_DATA_'
    FBA_INVENTORY_RECEIVED = '_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_'
    FBA_INVENTORY_RESERVED = '_GET_RESERVED_INVENTORY_DATA_'
    FBA_INVENTORY_EVENT_DETAIL = '_GET_FBA_FULFILLMENT_INVENTORY_SUMMARY_DATA_'
    FBA_INVENTORY_ADJUSTMENTS = '_GET_FBA_FULFILLMENT_INVENTORY_ADJUSTMENTS_DATA_'
    FBA_INVENTORY_HEALTH = '_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_'
    FBA_INVENTORY_MANAGE_ACTIVE = '_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_'
    FBA_INVENTORY_MANAGE_ALL = '_GET_FBA_MYI_ALL_INVENTORY_DATA_'
    FBA_INVENTORY_CROSS_BORDER_MOVEMENT = '_GET_FBA_FULFILLMENT_CROSS_BORDER_INVENTORY_MOVEMENT_DATA_'
    FBA_INVENTORY_INBOUND_PERFORMANCE = '_GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA_'
    FBA_INVENTORY_STRANDED = '_GET_STRANDED_INVENTORY_UI_DATA_'
    FBA_INVENTORY_BULK_FIX_STRANDED = '_GET_STRANDED_INVENTORY_LOADER_DATA_'
    FBA_INVENTORY_AGE = '_GET_FBA_INVENTORY_AGED_DATA_'
    FBA_INVENTORY_EXCESS = '_GET_EXCESS_INVENTORY_DATA_'
    # FBA Payments Reports
    FBA_PAYMENTS_FEE_PREVIEW = '_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_'
    FBA_PAYMENTS_REIMBURSEMENTS = '_GET_FBA_REIMBURSEMENTS_DATA_'
    # FBA Customer Concessions Reports
    FBA_CONCESSION_RETURNS = '_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_'
    # FBA Removals Reports
    FBA_REMOVAL_RECOMMENDED = '_GET_FBA_RECOMMENDED_REMOVAL_DATA_'
    FBA_REMOVAL_ORDER_DETAIL = '_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_'
    FBA_REMOVAL_SHIPMENT_DETAIL = '_GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA_'
