from enum import Enum

__all__ = [
    "ReportType",
    "ProcessingStatus",
    "Schedule",
]


class ReportType(str, Enum):
    """An enumeration of the types of reports that can be requested from Amazon MWS.

    `MWS Docs: ReportType enumeration
    <https://docs.developer.amazonservices.com/en_US/reports/Reports_ReportType.html>`_
    """

    # Inventory Reports
    INVENTORY = "_GET_FLAT_FILE_OPEN_LISTINGS_DATA_"
    ALL_LISTINGS = "_GET_MERCHANT_LISTINGS_ALL_DATA_"
    ACTIVE_LISTINGS = "_GET_MERCHANT_LISTINGS_DATA_"
    INACTIVE_LISTINGS = "_GET_MERCHANT_LISTINGS_INACTIVE_DATA_"
    OPEN_LISTINGS = "_GET_MERCHANT_LISTINGS_DATA_BACK_COMPAT_"
    OPEN_LISTINGS_LITE = "_GET_MERCHANT_LISTINGS_DATA_LITE_"
    OPEN_LISTINGS_LITER = "_GET_MERCHANT_LISTINGS_DATA_LITER_"
    CANCELED_LISTINGS = "_GET_MERCHANT_CANCELLED_LISTINGS_DATA_"
    SOLD_LISTINGS = "_GET_CONVERGED_FLAT_FILE_SOLD_LISTINGS_DATA_"
    LISTING_QUALITY_AND_SUPPRESSED = "_GET_MERCHANT_LISTINGS_DEFECT_DATA_"
    PAN_EUROPEAN_ELIGIBILITY_FBA_ASINS = "_GET_PAN_EU_OFFER_STATUS_"
    PAN_EUROPEAN_ELIGIBILITY_SELF_FULFILLED_ASINS = "_GET_MFN_PAN_EU_OFFER_STATUS_"
    GLOBAL_EXPANSION_OPPORTUNITIES = "_GET_FLAT_FILE_GEO_OPPORTUNITIES_"
    REFERRAL_FEE_PREVIEW = "_GET_REFERRAL_FEE_PREVIEW_REPORT_"

    # Order Reports
    ORDERS_UNSHIPPED = "_GET_FLAT_FILE_ACTIONABLE_ORDER_DATA_"
    ORDERS_SCHEDULED_XML = "_GET_ORDERS_DATA_"
    ORDERS_REQUESTED_OR_SCHEDULED = "_GET_FLAT_FILE_ORDERS_DATA_"
    ORDERS_CONVERGED = "_GET_CONVERGED_FLAT_FILE_ORDER_REPORT_DATA_"

    # Order Tracking Reports
    TRACKING_BY_LAST_UPDATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    TRACKING_BY_ORDER_DATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    TRACKING_ARCHIVED_ORDERS_FLATFILE = (
        "_GET_FLAT_FILE_ARCHIVED_ORDERS_DATA_BY_ORDER_DATE_"
    )
    TRACKING_BY_LAST_UPDATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    TRACKING_BY_ORDER_DATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_"

    # Pending Order Reports
    PENDING_ORDERS_FLAT_FILE = "_GET_FLAT_FILE_PENDING_ORDERS_DATA_"
    PENDING_ORDERS_XML = "_GET_PENDING_ORDERS_DATA_"
    PENDING_ORDERS_CONVERGED_FLAT_FILE = "_GET_CONVERGED_FLAT_FILE_PENDING_ORDERS_DATA_"

    # Returns reports
    RETURNS_XML_DATA_BY_RETURN_DATE = "_GET_XML_RETURNS_DATA_BY_RETURN_DATE_"
    RETURNS_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE = (
        "_GET_FLAT_FILE_RETURNS_DATA_BY_RETURN_DATE_"
    )
    RETURNS_XML_MFN_PRIME_RETURNS_REPORT = "_GET_XML_MFN_PRIME_RETURNS_REPORT_"
    RETURNS_CSV_MFN_PRIME_RETURNS_REPORT = "_GET_CSV_MFN_PRIME_RETURNS_REPORT_"
    RETURNS_XML_MFN_SKU_RETURN_ATTRIBUTES_REPORT = (
        "_GET_XML_MFN_SKU_RETURN_ATTRIBUTES_REPORT_"
    )
    RETURNS_FLAT_FILE_MFN_SKU_RETURN_ATTRIBUTES_REPORT = (
        "_GET_FLAT_FILE_MFN_SKU_RETURN_ATTRIBUTES_REPORT_"
    )

    # Performance Reports
    PERFORMANCE_FEEDBACK = "_GET_SELLER_FEEDBACK_DATA_"
    PERFORMANCE_CUSTOMER_METRICS_XML = "_GET_V1_SELLER_PERFORMANCE_REPORT_"

    # Settlement Reports
    SETTLEMENT_FLATFILE = "_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_"
    SETTLEMENT_V2_XML = "_GET_V2_SETTLEMENT_REPORT_DATA_XML_"
    SETTLEMENT_V2_FLATFILE = "_GET_V2_SETTLEMENT_REPORT_DATA_FLAT_FILE_V2_"

    # FBA Sales Reports
    FBA_SALES_AMAZON_FULFILLED = "_GET_AMAZON_FULFILLED_SHIPMENTS_DATA_"
    FBA_SALES_ALL_LAST_UPDATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    FBA_SALES_ALL_BY_ORDER_DATE = "_GET_FLAT_FILE_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    FBA_SALES_ALL_BY_LAST_UPDATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_LAST_UPDATE_"
    FBA_SALES_ALL_BY_ORDER_DATE_XML = "_GET_XML_ALL_ORDERS_DATA_BY_ORDER_DATE_"
    FBA_SALES_CUSTOMER_SHIPMENT = "_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_SALES_DATA_"
    FBA_SALES_PROMOTIONS = "_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_PROMOTION_DATA_"
    FBA_SALES_CUSTOMER_TAXES = "_GET_FBA_FULFILLMENT_CUSTOMER_TAXES_DATA_"
    FBA_SALES_REMOTE_FULFILLMENT_ELIGIBILITY = "_GET_REMOTE_FULFILLMENT_ELIGIBILITY_"

    # FBA Inventory Reports
    FBA_INVENTORY_AFN = "_GET_AFN_INVENTORY_DATA_"
    FBA_INVENTORY_AFN_BY_COUNTRY = "_GET_AFN_INVENTORY_DATA_BY_COUNTRY_"
    FBA_INVENTORY_HISTORY_DAILY = "_GET_FBA_FULFILLMENT_CURRENT_INVENTORY_DATA_"
    FBA_INVENTORY_HISTORY_MONTHLY = "_GET_FBA_FULFILLMENT_MONTHLY_INVENTORY_DATA_"
    FBA_INVENTORY_RECEIVED = "_GET_FBA_FULFILLMENT_INVENTORY_RECEIPTS_DATA_"
    FBA_INVENTORY_RESERVED = "_GET_RESERVED_INVENTORY_DATA_"
    FBA_INVENTORY_EVENT_DETAIL = "_GET_FBA_FULFILLMENT_INVENTORY_SUMMARY_DATA_"
    FBA_INVENTORY_ADJUSTMENTS = "_GET_FBA_FULFILLMENT_INVENTORY_ADJUSTMENTS_DATA_"
    FBA_INVENTORY_HEALTH = "_GET_FBA_FULFILLMENT_INVENTORY_HEALTH_DATA_"
    FBA_INVENTORY_MANAGE_ACTIVE = "_GET_FBA_MYI_UNSUPPRESSED_INVENTORY_DATA_"
    FBA_INVENTORY_MANAGE_ALL = "_GET_FBA_MYI_ALL_INVENTORY_DATA_"
    FBA_INVENTORY_RESTOCK_INVENTORY = "_GET_RESTOCK_INVENTORY_RECOMMENDATIONS_REPORT_"
    # TODO can't find a reference for the cross-border report type in MWS docs.
    # is it older? Or coming from a different endpoint, maybe?
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
    FBA_INVENTORY_STORAGE_FEE_CHARGES = "_GET_FBA_STORAGE_FEE_CHARGES_DATA_"
    FBA_INVENTORY_PRODUCT_EXCHANGE = "_GET_PRODUCT_EXCHANGE_DATA_"

    # FBA Payments Reports
    FBA_PAYMENTS_FEE_PREVIEW = "_GET_FBA_ESTIMATED_FBA_FEES_TXT_DATA_"
    FBA_PAYMENTS_REIMBURSEMENTS = "_GET_FBA_REIMBURSEMENTS_DATA_"
    FBA_PAYMENTS_LONGTERM_STORAGE_FEE_CHARGES = (
        "_GET_FBA_FULFILLMENT_LONGTERM_STORAGE_FEE_CHARGES_DATA_"
    )

    # FBA Customer Concessions Reports
    FBA_CONCESSION_RETURNS = "_GET_FBA_FULFILLMENT_CUSTOMER_RETURNS_DATA_"
    FBA_CONCESSION_SHIPMENT_REPLACEMENT = (
        "_GET_FBA_FULFILLMENT_CUSTOMER_SHIPMENT_REPLACEMENT_DATA_"
    )

    # FBA Removals Reports
    FBA_REMOVAL_RECOMMENDED = "_GET_FBA_RECOMMENDED_REMOVAL_DATA_"
    FBA_REMOVAL_ORDER_DETAIL = "_GET_FBA_FULFILLMENT_REMOVAL_ORDER_DETAIL_DATA_"
    FBA_REMOVAL_SHIPMENT_DETAIL = "_GET_FBA_FULFILLMENT_REMOVAL_SHIPMENT_DETAIL_DATA_"

    # FBA Small & Light
    FBA_SMALL_LIGHT_INVENTORY = "_GET_FBA_UNO_INVENTORY_DATA_"

    # Tax Reports
    SALES_TAX = "_GET_FLAT_FILE_SALES_TAX_DATA_"
    VAT_CALCULATION = "_SC_VAT_TAX_REPORT_"
    VAT_TRANSACTIONS = "_GET_VAT_TRANSACTION_DATA_"
    TAX_GST_MERCHANT_B2B = "_GET_GST_MTR_B2B_CUSTOM_"
    TAX_GST_MERCHANT_B2C = "_GET_GST_MTR_B2C_CUSTOM_"

    # Browse Tree Reports
    BROWSE_TREE = "_GET_XML_BROWSE_TREE_DATA_"

    # EasyShip
    EASYSHIP_DOCUMENTS = "_GET_EASYSHIP_DOCUMENTS_"
    EASYSHIP_PICKED_UP = "_GET_EASYSHIP_PICKEDUP_"
    EASYSHIP_WAITING_FOR_PICKUP = "_GET_EASYSHIP_WAITING_FOR_PICKUP_"

    # Amazon Business Reports
    AMZN_BUSINESS_FEE_DISCOUNTS_REPORT = "_FEE_DISCOUNTS_REPORT_"
    AMZN_BUSINESS_RFQD_BULK_DOWNLOAD = "_RFQD_BULK_DOWNLOAD_"

    # AmazonPay reports
    AMAZONPAY_SANDBOX_SETTLEMENT = (
        "_GET_FLAT_FILE_OFFAMAZONPAYMENTS_SANDBOX_SETTLEMENT_DATA_"
    )


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
