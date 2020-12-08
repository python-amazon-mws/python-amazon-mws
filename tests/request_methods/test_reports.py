"""Tests for the Reports API class."""

import datetime
import unittest
import mws
from mws.utils import clean_bool, clean_date

from .utils import CommonAPIRequestTools


class ReportsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Reports."""

    api_class = mws.Reports

    # TODO: Add remaining methods for Reports

    def test_request_report(self):
        """RequestReport operation."""
        report_type = "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
        start_date = datetime.datetime(2018, 4, 30, 22, 59, 59)
        end_date = datetime.datetime(2018, 4, 30, 23, 59, 59)
        marketplace_ids = [
            "iQzBCmf1y3",
            "wH9q0CiEMp",
        ]
        params = self.api.request_report(
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            marketplace_ids=marketplace_ids,
        )

        self.assert_common_params(params, action="RequestReport")
        self.assertEqual(params["ReportType"], report_type)
        self.assertEqual(params["StartDate"], "2018-04-30T22%3A59%3A59")
        self.assertEqual(params["EndDate"], "2018-04-30T23%3A59%3A59")
        self.assertEqual(params["MarketplaceIdList.Id.1"], marketplace_ids[0])
        self.assertEqual(params["MarketplaceIdList.Id.2"], marketplace_ids[1])

    def test_report_options_dict(self):
        """Asserts a dict used for report_options argument for request_report method
        builds the correct string output.
        """
        report_type = "_GET_MERCHANT_LISTINGS_ALL_DATA_"
        report_options = {"custom": True, "somethingelse": "abc"}
        params = self.api.request_report(
            report_type=report_type,
            report_options=report_options,
        )
        self.assert_common_params(params, action="RequestReport")
        assert params["ReportType"] == report_type
        # Cannot assume the order of the options dict passed on older versions
        # of Python, so two possible outputs are used:
        # Further, the final result should be encoded once before being sent,
        # resulting in the following URL-encoded strings.
        options_possible = (
            "custom%3Dtrue%3Bsomethingelse%3Dabc",
            "somethingelse%3Dabc%3Bcustom%3Dtrue",
        )
        assert params["ReportOptions"] in options_possible

    def test_parameter_error(self):
        """RequestReport wrong parameter"""
        # list will throw error
        report_type = ["_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"]
        start_date = datetime.datetime(2018, 4, 30, 22, 59, 59)
        end_date = datetime.datetime(2018, 4, 30, 23, 59, 59)
        marketplace_ids = [
            "iQzBCmf1y3",
            "wH9q0CiEMp",
        ]
        with self.assertRaises(mws.MWSError):
            self.api.request_report(
                report_type=report_type,
                start_date=start_date,
                end_date=end_date,
                marketplace_ids=marketplace_ids,
            )

    def test_get_report_request_list(self):
        """GetReportRequestList operation."""
        request_ids = [
            "rPlSxpfnR7",
            "qRrkqv03qh",
        ]
        report_types = [
            "_GET_MFN_PAN_EU_OFFER_STATUS_",
            "_GET_FLAT_FILE_ORDERS_DATA_",
        ]
        processing_statuses = [
            "_SUBMITTED_",
            "_DONE_NO_DATA_",
        ]
        max_count = 987
        from_date = datetime.datetime.utcnow()
        to_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.get_report_request_list(
            request_ids=request_ids,
            report_types=report_types,
            processing_statuses=processing_statuses,
            max_count=max_count,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportRequestList")
        self.assertEqual(params["MaxCount"], str(max_count))
        self.assertEqual(params["RequestedFromDate"], clean_date(from_date))
        self.assertEqual(params["RequestedToDate"], clean_date(to_date))
        self.assertEqual(params["ReportRequestIdList.Id.1"], request_ids[0])
        self.assertEqual(params["ReportRequestIdList.Id.2"], request_ids[1])
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])
        self.assertEqual(
            params["ReportProcessingStatusList.Status.1"], processing_statuses[0]
        )
        self.assertEqual(
            params["ReportProcessingStatusList.Status.2"], processing_statuses[1]
        )

    def test_get_report_request_list_by_next_token(self):
        """GetReportRequestListByNextToken operation, via method decorator."""
        next_token = "RXmLZ2bEgE"
        params = self.api.get_report_request_list(next_token=next_token)
        self.assert_common_params(params, action="GetReportRequestListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_request_list_by_next_token_alias(self):
        """GetReportRequestListByNextToken operation, via alias method."""
        next_token = "0hytxbkaOb"
        params = self.api.get_report_request_list_by_next_token(next_token)
        self.assert_common_params(params, action="GetReportRequestListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_request_count(self):
        """GetReportRequestCount operation."""
        report_types = [
            "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_",
            "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_",
        ]
        processing_statuses = [
            "_CANCELLED_",
            "_IN_PROGRESS_",
        ]
        from_date = datetime.datetime.utcnow()
        to_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.get_report_request_count(
            report_types=report_types,
            processing_statuses=processing_statuses,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportRequestCount")
        self.assertEqual(params["RequestedFromDate"], clean_date(from_date))
        self.assertEqual(params["RequestedToDate"], clean_date(to_date))
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])
        self.assertEqual(
            params["ReportProcessingStatusList.Status.1"], processing_statuses[0]
        )
        self.assertEqual(
            params["ReportProcessingStatusList.Status.2"], processing_statuses[1]
        )

    def test_get_report_list(self):
        """GetReportList operation."""
        request_ids = [
            "c4eik8sxXC",
            "NIVgnbHXe0",
        ]
        report_types = [
            "_GET_V1_SELLER_PERFORMANCE_REPORT_",
            "_GET_SELLER_FEEDBACK_DATA_",
        ]
        max_count = 564
        acknowledged = True
        from_date = datetime.datetime.utcnow()
        to_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.get_report_list(
            request_ids=request_ids,
            max_count=max_count,
            report_types=report_types,
            acknowledged=acknowledged,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportList")
        self.assertEqual(params["Acknowledged"], clean_bool(acknowledged))
        self.assertEqual(params["AvailableFromDate"], clean_date(from_date))
        self.assertEqual(params["AvailableToDate"], clean_date(to_date))
        self.assertEqual(params["MaxCount"], str(max_count))
        self.assertEqual(params["ReportRequestIdList.Id.1"], request_ids[0])
        self.assertEqual(params["ReportRequestIdList.Id.2"], request_ids[1])
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])

    def test_get_report_list_by_next_token(self):
        """GetReportListByNextToken operation, via method decorator."""
        next_token = "5u6Of2fS8B"
        params = self.api.get_report_list(next_token=next_token)
        self.assert_common_params(params, action="GetReportListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_list_by_next_token_alias(self):
        """GetReportListByNextToken operation, via alias method."""
        next_token = "3TczcliCkb"
        params = self.api.get_report_list_by_next_token(next_token)
        self.assert_common_params(params, action="GetReportListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_count(self):
        """GetReportCount operation."""
        report_types = [
            "_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_",
            "_GET_AFN_INVENTORY_DATA_BY_COUNTRY_",
        ]
        acknowledged = True
        from_date = datetime.datetime.utcnow()
        to_date = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        params = self.api.get_report_count(
            report_types=report_types,
            acknowledged=acknowledged,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportCount")
        self.assertEqual(params["Acknowledged"], clean_bool(acknowledged))
        self.assertEqual(params["AvailableFromDate"], clean_date(from_date))
        self.assertEqual(params["AvailableToDate"], clean_date(to_date))
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])

    def test_get_report(self):
        """GetReport operation."""
        report_id = "wwqrl4bHvD"
        params = self.api.get_report(report_id=report_id)
        self.assert_common_params(params, action="GetReport")
        self.assertEqual(params["ReportId"], report_id)

    def test_get_report_schedule_list(self):
        """GetReportScheduleList operation."""
        report_types = [
            "_GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA_",
            "_GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT_",
        ]
        params = self.api.get_report_schedule_list(report_types=report_types)
        self.assert_common_params(params, action="GetReportScheduleList")
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])

    def test_get_report_schedule_list_by_next_token(self):
        """GetReportScheduleListByNextToken operation, via method decorator."""
        next_token = "Yj3hOfPcIE"
        params = self.api.get_report_schedule_list(next_token=next_token)
        self.assert_common_params(params, action="GetReportScheduleListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_schedule_list_by_next_token_alias(self):
        """GetReportScheduleListByNextToken operation, via alias method."""
        next_token = "SAlt4JwJGv"
        params = self.api.get_report_schedule_list_by_next_token(next_token)
        self.assert_common_params(params, action="GetReportScheduleListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_report_schedule_count(self):
        """GetReportScheduleCount operation."""
        report_types = [
            "_GET_STRANDED_INVENTORY_UI_DATA_",
            "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_",
        ]
        params = self.api.get_report_schedule_count(report_types=report_types)
        self.assert_common_params(params, action="GetReportScheduleCount")
        self.assertEqual(params["ReportTypeList.Type.1"], report_types[0])
        self.assertEqual(params["ReportTypeList.Type.2"], report_types[1])

    # # TODO Complete when method is available in Reports
    # def test_update_report_acknowledgements(self):
    #     """UpdateReportAcknowledgements operation."""
    #     pass
