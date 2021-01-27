Reports
#######

Reports API reference
=====================

.. autoclass:: mws.apis.reports.Reports

   .. automethod:: request_report
   .. automethod:: get_report_request_list
   .. automethod:: get_report_request_list_by_next_token
   .. automethod:: get_report_request_count
   .. automethod:: cancel_report_requests
   .. automethod:: get_report_list
   .. automethod:: get_report_list_by_next_token
   .. automethod:: get_report_count
   .. automethod:: get_report
   .. automethod:: manage_report_schedule
   .. automethod:: get_report_schedule_list
   .. automethod:: get_report_schedule_list_by_next_token
   .. automethod:: get_report_schedule_count
   .. automethod:: update_report_acknowledgements

Enums
=====

.. autoclass:: mws.apis.reports.ReportType
   :show-inheritance:

   For convenience, this Enum can also be accessed directly from the
   :py:class:`Reports <mws.apis.reports.Reports>` class or an instance of that class:

   .. code-block:: python

      from mws import Reports

      inventory_type = Reports.ReportType.INVENTORY
      # OR
      reports_api = Reports(...)
      inventory_type = reports_api.ReportType.INVENTORY

   .. rubric:: Available values

   You can use either the Enum instance itself or its string value as an
   argument in relevant request methods. Each of the below examples may be
   used in a request for a flat file of open listings:

   .. code-block:: python

      from mws.apis.reports import ReportType

      my_report_type = ReportType.INVENTORY
      # OR
      my_report_type = ReportType.INVENTORY.value
      # OR
      my_report_type = '_GET_FLAT_FILE_OPEN_LISTINGS_DATA_'

   .. autoattribute:: INVENTORY
   .. autoattribute:: ACTIVE_LISTINGS
   .. autoattribute:: OPEN_LISTINGS
   .. autoattribute:: OPEN_LISTINGS_LITE
   .. autoattribute:: OPEN_LISTINGS_LITER
   .. autoattribute:: CANCELED_LISTINGS
   .. autoattribute:: SOLD_LISTINGS
   .. autoattribute:: QUALITY_AND_SUPPRESSED
   .. autoattribute:: ORDERS_UNSHIPPED
   .. autoattribute:: ORDERS_SCHEDULED_XML
   .. autoattribute:: ORDERS
   .. autoattribute:: ORDERS_CONVERGED
   .. autoattribute:: TRACKING_BY_LAST_UPDATE
   .. autoattribute:: TRACKING_BY_ORDER_DATE
   .. autoattribute:: TRACKING_BY_LAST_UPDATE_XML
   .. autoattribute:: TRACKING_BY_ORDER_DATE_XML
   .. autoattribute:: PENDING_ORDERS_FLAT_FILE
   .. autoattribute:: PENDING_ORDERS_XML
   .. autoattribute:: PENDING_ORDERS_CONVERGED_FLAT_FILE
   .. autoattribute:: PERFORMANCE_FEEDBACK
   .. autoattribute:: PERFORMANCE_CUSTOMER_METRICS_XML
   .. autoattribute:: SETTLEMENT
   .. autoattribute:: SETTLEMENT_V2
   .. autoattribute:: SALES_TAX
   .. autoattribute:: VAT_CALCULATION
   .. autoattribute:: VAT_TRANSACTIONS
   .. autoattribute:: BROWSE_TREE
   .. autoattribute:: FBA_SALES_AMAZON_FULFILLED
   .. autoattribute:: FBA_SALES_ALL_LAST_UPDATE
   .. autoattribute:: FBA_SALES_ALL_BY_ORDER_DATE
   .. autoattribute:: FBA_SALES_ALL_BY_LAST_UPDATE_XML
   .. autoattribute:: FBA_SALES_ALL_BY_ORDER_DATE_XML
   .. autoattribute:: FBA_SALES_CUSTOMER_SHIPMENT
   .. autoattribute:: FBA_SALES_PROMOTIONS
   .. autoattribute:: FBA_SALES_CUSTOMER_TAXES
   .. autoattribute:: FBA_INVENTORY_AFN
   .. autoattribute:: FBA_INVENTORY_AFN_BY_COUNTRY
   .. autoattribute:: FBA_INVENTORY_HISTORY_DAILY
   .. autoattribute:: FBA_INVENTORY_HISTORY_MONTHLY
   .. autoattribute:: FBA_INVENTORY_RECEIVED
   .. autoattribute:: FBA_INVENTORY_RESERVED
   .. autoattribute:: FBA_INVENTORY_EVENT_DETAIL
   .. autoattribute:: FBA_INVENTORY_ADJUSTMENTS
   .. autoattribute:: FBA_INVENTORY_HEALTH
   .. autoattribute:: FBA_INVENTORY_MANAGE_ACTIVE
   .. autoattribute:: FBA_INVENTORY_MANAGE_ALL
   .. autoattribute:: FBA_INVENTORY_CROSS_BORDER_MOVEMENT
   .. autoattribute:: FBA_INVENTORY_INBOUND_PERFORMANCE
   .. autoattribute:: FBA_INVENTORY_STRANDED
   .. autoattribute:: FBA_INVENTORY_BULK_FIX_STRANDED
   .. autoattribute:: FBA_INVENTORY_AGE
   .. autoattribute:: FBA_INVENTORY_EXCESS
   .. autoattribute:: FBA_PAYMENTS_FEE_PREVIEW
   .. autoattribute:: FBA_PAYMENTS_REIMBURSEMENTS
   .. autoattribute:: FBA_CONCESSION_RETURNS
   .. autoattribute:: FBA_REMOVAL_RECOMMENDED
   .. autoattribute:: FBA_REMOVAL_ORDER_DETAIL
   .. autoattribute:: FBA_REMOVAL_SHIPMENT_DETAIL

.. autoclass:: mws.apis.reports.Schedule
   :show-inheritance:

   For convenience, this Enum can also be accessed directly from the
   :py:class:`Reports <mws.apis.reports.Reports>` class or an instance of that class:

   .. code-block:: python

      from mws import Reports

      my_schedule = Reports.Schedule.EVERY_15_MIN
      # OR
      reports_api = Reports(...)
      my_schedule = reports_api.Schedule.EVERY_15_MIN

   .. rubric:: Available values

   Several schedule frequencies are provided by Amazon, and this Enum
   provides easy access to all of them through several aliases for each
   schedule type.

   .. rubric:: Every 15 minutes:
   .. autoattribute:: EVERY_15_MIN
   .. autoattribute:: EVERY_15_MINS
   .. autoattribute:: EVERY_15_MINUTE
   .. autoattribute:: EVERY_15_MINUTES

   .. rubric:: Every 30 minutes:
   .. autoattribute:: EVERY_30_MIN
   .. autoattribute:: EVERY_30_MINS
   .. autoattribute:: EVERY_30_MINUTE
   .. autoattribute:: EVERY_30_MINUTES

   .. rubric:: Every hour:
   .. autoattribute:: EVERY_HOUR
   .. autoattribute:: EVERY_1_HOUR
   .. autoattribute:: EVERY_1_HOURS

   .. rubric:: Every 2 hours:
   .. autoattribute:: EVERY_2_HOUR
   .. autoattribute:: EVERY_2_HOURS

   .. rubric:: Every 4 hours:
   .. autoattribute:: EVERY_4_HOUR
   .. autoattribute:: EVERY_4_HOURS

   .. rubric:: Every 8 hours:
   .. autoattribute:: EVERY_8_HOUR
   .. autoattribute:: EVERY_8_HOURS

   .. rubric:: Every 12 hours:
   .. autoattribute:: EVERY_12_HOUR
   .. autoattribute:: EVERY_12_HOURS

   .. rubric:: Every day:
   .. autoattribute:: DAILY
   .. autoattribute:: EVERY_DAY
   .. autoattribute:: EVERY_1_DAY
   .. autoattribute:: EVERY_1_DAYS

   .. rubric:: Every 2 days:
   .. autoattribute:: EVERY_2_DAY
   .. autoattribute:: EVERY_2_DAYS
   .. autoattribute:: EVERY_48_HOUR
   .. autoattribute:: EVERY_48_HOURS

   .. rubric:: Every 3 days:
   .. autoattribute:: EVERY_3_DAY
   .. autoattribute:: EVERY_3_DAYS
   .. autoattribute:: EVERY_72_HOUR
   .. autoattribute:: EVERY_72_HOURS

   .. rubric:: Every week:
   .. autoattribute:: WEEKLY
   .. autoattribute:: EVERY_WEEK
   .. autoattribute:: EVERY_1_WEEK
   .. autoattribute:: EVERY_1_WEEKS
   .. autoattribute:: EVERY_7_DAY
   .. autoattribute:: EVERY_7_DAYS

   .. rubric:: Every 2 weeks:
   .. autoattribute:: EVERY_14_DAY
   .. autoattribute:: EVERY_14_DAYS
   .. autoattribute:: EVERY_2_WEEK
   .. autoattribute:: EVERY_2_WEEKS
   .. autoattribute:: FORTNIGHTLY

   .. rubric:: Every 15 days:
   .. autoattribute:: EVERY_15_DAY
   .. autoattribute:: EVERY_15_DAYS

   .. rubric:: Every 30 days:
   .. autoattribute:: EVERY_30_DAY
   .. autoattribute:: EVERY_30_DAYS

   .. rubric:: Delete a previously created report request schedule:
   .. autoattribute:: DELETE

.. autoclass:: mws.apis.reports.ProcessingStatus
   :show-inheritance:

   For convenience, this Enum can also be accessed directly from the
   :py:class:`Reports <mws.apis.reports.Reports>` class or an instance of that class:

   .. code-block:: python

      from mws import Reports

      my_processing_status = Reports.ProcessingStatus.DONE
      # OR
      reports_api = Reports(...)
      my_processing_status = reports_api.ProcessingStatus.DONE

   .. autoattribute:: SUBMITTED
   .. autoattribute:: IN_PROGRESS
   .. autoattribute:: CANCELLED
   .. autoattribute:: CANCELED
   .. autoattribute:: DONE
   .. autoattribute:: DONE_NO_DATA
