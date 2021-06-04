import datetime

import pytest

from mws import Reports, Marketplaces, MWSError

from .common import APITestCase


class ReportsAPITestCase(APITestCase):
    api_class = Reports


class TestReportsAPI(ReportsAPITestCase):
    """Test cases covering the ``Reports`` API."""

    @pytest.mark.parametrize(
        "report_type",
        [
            "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_",
            Reports.ReportType.INVENTORY.value,
            Reports.ReportType.INVENTORY,
        ],
    )
    @pytest.mark.parametrize(
        "marketplace_id",
        [
            "ATVPDKIKX0DER",
            Marketplaces.US.marketplace_id,
            Marketplaces.US.value,
            Marketplaces.US,
        ],
    )
    def test_request_report_enums_accepted(
        self, api_instance: Reports, report_type, marketplace_id
    ):
        """Operations should be able to accept Enum values naturally."""
        params = api_instance.request_report(
            report_type=report_type,
            marketplace_ids=marketplace_id,
        )
        assert params["ReportType"] == "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
        assert params["MarketplaceIdList.Id.1"] == "ATVPDKIKX0DER"

    def test_request_report(self, api_instance: Reports):
        """RequestReport operation."""
        report_type = "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
        start_date = datetime.datetime(2018, 4, 30, 22, 59, 59)
        end_date = datetime.datetime(2018, 4, 30, 23, 59, 59)
        marketplace_ids = [
            "iQzBCmf1y3",
            "wH9q0CiEMp",
        ]
        params = api_instance.request_report(
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            marketplace_ids=marketplace_ids,
        )
        self.assert_common_params(params, action="RequestReport")
        assert params["ReportType"] == "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
        assert params["StartDate"] == "2018-04-30T22:59:59"
        assert params["EndDate"] == "2018-04-30T23:59:59"
        assert params["MarketplaceIdList.Id.1"] == marketplace_ids[0]
        assert params["MarketplaceIdList.Id.2"] == marketplace_ids[1]

    def test_report_options_dict(self, api_instance: Reports):
        """Asserts a dict used for report_options argument for request_report method
        builds the correct string output.
        """
        report_type = "_GET_MERCHANT_LISTINGS_ALL_DATA_"
        report_options = {"custom": True, "somethingelse": "abc"}
        params = api_instance.request_report(
            report_type=report_type,
            report_options=report_options,
        )
        self.assert_common_params(params, action="RequestReport")
        assert params["ReportType"] == "_GET_MERCHANT_LISTINGS_ALL_DATA_"
        # Cannot assume the order of the options dict passed on older versions
        # of Python, so two possible outputs are used:
        # Further, the final result should be encoded once before being sent,
        # resulting in the following URL-encoded strings.
        options_possible = (
            "custom=true;somethingelse=abc",
            "somethingelse=abc;custom=true",
        )
        assert params["ReportOptions"] in options_possible

    def test_request_report_error(self, api_instance: Reports):
        """RequestReport wrong parameter"""
        # list will throw error
        report_type = ["_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"]
        start_date = datetime.datetime(2018, 4, 30, 22, 59, 59)
        end_date = datetime.datetime(2018, 4, 30, 23, 59, 59)
        marketplace_ids = [
            "iQzBCmf1y3",
            "wH9q0CiEMp",
        ]
        with pytest.raises(MWSError):
            api_instance.request_report(
                report_type=report_type,
                start_date=start_date,
                end_date=end_date,
                marketplace_ids=marketplace_ids,
            )

    def test_get_report_request_list(self, api_instance: Reports):
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
        from_date = datetime.datetime(2021, 1, 26, 22, 59, 59)
        to_date = datetime.datetime(2021, 1, 26, 23, 59, 59)
        params = api_instance.get_report_request_list(
            request_ids=request_ids,
            report_types=report_types,
            processing_statuses=processing_statuses,
            max_count=max_count,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportRequestList")
        assert params["MaxCount"] == str(max_count)
        assert params["RequestedFromDate"] == "2021-01-26T22:59:59"
        assert params["RequestedToDate"] == "2021-01-26T23:59:59"
        assert params["ReportRequestIdList.Id.1"] == "rPlSxpfnR7"
        assert params["ReportRequestIdList.Id.2"] == "qRrkqv03qh"
        assert params["ReportTypeList.Type.1"] == "_GET_MFN_PAN_EU_OFFER_STATUS_"
        assert params["ReportTypeList.Type.2"] == "_GET_FLAT_FILE_ORDERS_DATA_"
        assert params["ReportProcessingStatusList.Status.1"] == "_SUBMITTED_"
        assert params["ReportProcessingStatusList.Status.2"] == "_DONE_NO_DATA_"

    def test_get_report_request_list_by_next_token(self, api_instance: Reports):
        """GetReportRequestListByNextToken operation, via method decorator."""
        params = api_instance.get_report_request_list(next_token="RXmLZ2bEgE")
        self.assert_common_params(params, action="GetReportRequestListByNextToken")
        assert params["NextToken"] == "RXmLZ2bEgE"

    def test_get_report_request_list_by_next_token_alias(self, api_instance: Reports):
        """GetReportRequestListByNextToken operation, via alias method."""
        params = api_instance.get_report_request_list_by_next_token("0hytxbkaOb")
        self.assert_common_params(params, action="GetReportRequestListByNextToken")
        assert params["NextToken"] == "0hytxbkaOb"

    def test_get_report_request_count(self, api_instance: Reports):
        """GetReportRequestCount operation."""
        report_types = [
            "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_",
            "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_",
        ]
        processing_statuses = [
            "_CANCELLED_",
            "_IN_PROGRESS_",
        ]
        from_date = datetime.datetime(2021, 1, 26, 22, 59, 59)
        to_date = datetime.datetime(2021, 1, 26, 23, 59, 59)
        params = api_instance.get_report_request_count(
            report_types=report_types,
            processing_statuses=processing_statuses,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportRequestCount")
        assert params["RequestedFromDate"] == "2021-01-26T22:59:59"
        assert params["RequestedToDate"] == "2021-01-26T23:59:59"
        assert (
            params["ReportTypeList.Type.1"]
            == "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
        )
        assert (
            params["ReportTypeList.Type.2"]
            == "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_"
        )
        assert params["ReportProcessingStatusList.Status.1"] == "_CANCELLED_"
        assert params["ReportProcessingStatusList.Status.2"] == "_IN_PROGRESS_"

    def test_get_report_list(self, api_instance: Reports):
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
        from_date = datetime.datetime(2021, 1, 26, 22, 59, 59)
        to_date = datetime.datetime(2021, 1, 26, 23, 59, 59)
        params = api_instance.get_report_list(
            request_ids=request_ids,
            max_count=max_count,
            report_types=report_types,
            acknowledged=acknowledged,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportList")
        assert params["Acknowledged"] == "true"
        assert params["AvailableFromDate"] == "2021-01-26T22:59:59"
        assert params["AvailableToDate"] == "2021-01-26T23:59:59"
        assert params["MaxCount"] == "564"
        assert params["ReportRequestIdList.Id.1"] == "c4eik8sxXC"
        assert params["ReportRequestIdList.Id.2"] == "NIVgnbHXe0"
        assert params["ReportTypeList.Type.1"] == "_GET_V1_SELLER_PERFORMANCE_REPORT_"
        assert params["ReportTypeList.Type.2"] == "_GET_SELLER_FEEDBACK_DATA_"

    def test_get_report_list_by_next_token(self, api_instance: Reports):
        """GetReportListByNextToken operation, via method decorator."""
        params = api_instance.get_report_list(next_token="5u6Of2fS8B")
        self.assert_common_params(params, action="GetReportListByNextToken")
        assert params["NextToken"] == "5u6Of2fS8B"

    def test_get_report_list_by_next_token_alias(self, api_instance: Reports):
        """GetReportListByNextToken operation, via alias method."""
        params = api_instance.get_report_list_by_next_token("3TczcliCkb")
        self.assert_common_params(params, action="GetReportListByNextToken")
        assert params["NextToken"] == "3TczcliCkb"

    def test_get_report_count(self, api_instance: Reports):
        """GetReportCount operation."""
        report_types = [
            "_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_",
            "_GET_AFN_INVENTORY_DATA_BY_COUNTRY_",
        ]
        acknowledged = True
        from_date = datetime.datetime(2021, 1, 26, 22, 59, 59)
        to_date = datetime.datetime(2021, 1, 26, 23, 59, 59)
        params = api_instance.get_report_count(
            report_types=report_types,
            acknowledged=acknowledged,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetReportCount")
        assert params["Acknowledged"] == "true"
        assert params["AvailableFromDate"] == "2021-01-26T22:59:59"
        assert params["AvailableToDate"] == "2021-01-26T23:59:59"
        assert (
            params["ReportTypeList.Type.1"] == "_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_"
        )
        assert params["ReportTypeList.Type.2"] == "_GET_AFN_INVENTORY_DATA_BY_COUNTRY_"

    def test_get_report(self, api_instance: Reports):
        """GetReport operation."""
        params = api_instance.get_report(report_id="wwqrl4bHvD")
        self.assert_common_params(params, action="GetReport")
        assert params["ReportId"] == "wwqrl4bHvD"

    def test_get_report_schedule_list(self, api_instance: Reports):
        """GetReportScheduleList operation."""
        params = api_instance.get_report_schedule_list(
            report_types=[
                "_GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA_",
                "_GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT_",
            ]
        )
        self.assert_common_params(params, action="GetReportScheduleList")
        assert (
            params["ReportTypeList.Type.1"]
            == "_GET_FBA_FULFILLMENT_INBOUND_NONCOMPLIANCE_DATA_"
        )
        assert (
            params["ReportTypeList.Type.2"]
            == "_GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT_"
        )

    def test_get_report_schedule_list_by_next_token(self, api_instance: Reports):
        """GetReportScheduleListByNextToken operation, via method decorator."""
        params = api_instance.get_report_schedule_list(next_token="Yj3hOfPcIE")
        self.assert_common_params(params, action="GetReportScheduleListByNextToken")
        assert params["NextToken"] == "Yj3hOfPcIE"

    def test_get_report_schedule_list_by_next_token_alias(self, api_instance: Reports):
        """GetReportScheduleListByNextToken operation, via alias method."""
        params = api_instance.get_report_schedule_list_by_next_token("SAlt4JwJGv")
        self.assert_common_params(params, action="GetReportScheduleListByNextToken")
        assert params["NextToken"] == "SAlt4JwJGv"

    def test_get_report_schedule_count(self, api_instance: Reports):
        """GetReportScheduleCount operation."""
        params = api_instance.get_report_schedule_count(
            report_types=[
                "_GET_STRANDED_INVENTORY_UI_DATA_",
                "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_",
            ]
        )
        self.assert_common_params(params, action="GetReportScheduleCount")
        assert params["ReportTypeList.Type.1"] == "_GET_STRANDED_INVENTORY_UI_DATA_"
        assert (
            params["ReportTypeList.Type.2"] == "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_"
        )

    def test_manage_report_schedule(self, api_instance: Reports):
        """ManageReportSchedule operation."""
        schedule_date = datetime.datetime(2021, 1, 26)
        params = api_instance.manage_report_schedule(
            report_type="_GET_AFN_INVENTORY_DATA_",
            schedule="_15_MINUTES_",
            schedule_date=schedule_date,
        )
        self.assert_common_params(params, action="ManageReportSchedule")
        assert params["ReportType"] == "_GET_AFN_INVENTORY_DATA_"
        assert params["Schedule"] == "_15_MINUTES_"
        assert params["ScheduleDate"] == "2021-01-26T00:00:00"

    @pytest.mark.parametrize(
        "report_type",
        [
            "_GET_STRANDED_INVENTORY_UI_DATA_",
            Reports.ReportType.FBA_INVENTORY_STRANDED.value,
            Reports.ReportType.FBA_INVENTORY_STRANDED,
        ],
    )
    @pytest.mark.parametrize(
        "schedule",
        [
            "_30_MINUTES_",
            Reports.Schedule.EVERY_30_MIN.value,
            # And aliases
            Reports.Schedule.EVERY_30_MINS.value,
            Reports.Schedule.EVERY_30_MINUTE.value,
            Reports.Schedule.EVERY_30_MINUTES.value,
            Reports.Schedule.EVERY_30_MIN,
            Reports.Schedule.EVERY_30_MINS,
            Reports.Schedule.EVERY_30_MINUTE,
            Reports.Schedule.EVERY_30_MINUTES,
        ],
    )
    def test_manage_report_schedule_enums(
        self, api_instance: Reports, report_type, schedule
    ):
        """Using enums for report_type and schedule should produce the correct
        string literals when cleaned.
        """
        params = api_instance.manage_report_schedule(
            report_type=report_type,
            schedule=schedule,
        )
        self.assert_common_params(params, action="ManageReportSchedule")
        assert params["ReportType"] == "_GET_STRANDED_INVENTORY_UI_DATA_"
        assert params["Schedule"] == "_30_MINUTES_"

    def test_cancel_report_requests(self, api_instance: Reports):
        """CancelReportRequests operation."""
        request_ids = [
            "bV414Uy8Ab",
            "wCP115hLSn",
        ]
        report_types = [
            "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_",
            "_GET_FBA_REIMBURSEMENTS_DATA_",
        ]
        processing_statuses = [
            "_SUBMITTED_",
            "_DONE_NO_DATA_",
        ]
        from_date = datetime.datetime(2021, 1, 27, 22, 59, 59)
        to_date = datetime.datetime(2021, 1, 27, 23, 59, 59)
        params = api_instance.cancel_report_requests(
            request_ids=request_ids,
            report_types=report_types,
            processing_statuses=processing_statuses,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="CancelReportRequests")
        assert params["RequestedFromDate"] == "2021-01-27T22:59:59"
        assert params["RequestedToDate"] == "2021-01-27T23:59:59"
        assert params["ReportRequestIdList.Id.1"] == "bV414Uy8Ab"
        assert params["ReportRequestIdList.Id.2"] == "wCP115hLSn"
        assert (
            params["ReportTypeList.Type.1"] == "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_"
        )
        assert params["ReportTypeList.Type.2"] == "_GET_FBA_REIMBURSEMENTS_DATA_"
        assert params["ReportProcessingStatusList.Status.1"] == "_SUBMITTED_"
        assert params["ReportProcessingStatusList.Status.2"] == "_DONE_NO_DATA_"

    @pytest.mark.parametrize(
        "processing_status",
        [
            "_DONE_NO_DATA_",
            Reports.ProcessingStatus.DONE_NO_DATA.value,
            Reports.ProcessingStatus.DONE_NO_DATA,
        ],
    )
    def test_cancel_report_requests_processing_enums(
        self, api_instance: Reports, processing_status
    ):
        """Using enums for processing_status should produce the correct
        string literal when cleaned.
        """
        params = api_instance.cancel_report_requests(
            processing_statuses=processing_status,
        )
        assert params["ReportProcessingStatusList.Status.1"] == "_DONE_NO_DATA_"
