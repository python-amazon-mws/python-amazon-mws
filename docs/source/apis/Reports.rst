Reports
#######

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/reports/Reports_Overview.html>`_:

  The Reports API section of the Amazon Marketplace Web Service (Amazon MWS)
  API lets you request various reports that help you manage your Sell on
  Amazon business. Report types are specified using the ReportTypes
  enumeration.

Reports API reference
=====================

.. autoclass:: mws.apis.reports.Reports
   :members:
   :exclude-members: ReportType, Schedule, ProcessingStatus

Enums
=====

.. autoclass:: mws.apis.reports.ReportType
   :show-inheritance:
   :members:
   :undoc-members:

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

.. autoclass:: mws.apis.reports.Schedule
   :show-inheritance:
   :members:
   :undoc-members:

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

.. autoclass:: mws.apis.reports.ProcessingStatus
   :show-inheritance:
   :members:
   :undoc-members:

   For convenience, this Enum can also be accessed directly from the
   :py:class:`Reports <mws.apis.reports.Reports>` class or an instance of that class:

   .. code-block:: python

      from mws import Reports

      my_processing_status = Reports.ProcessingStatus.DONE
      # OR
      reports_api = Reports(...)
      my_processing_status = reports_api.ProcessingStatus.DONE
