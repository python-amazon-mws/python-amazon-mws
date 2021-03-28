Reports
#######

.. currentmodule:: mws

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/reports/Reports_Overview.html>`_:

  The Reports API section of the Amazon Marketplace Web Service (Amazon MWS)
  API lets you request various reports that help you manage your Sell on
  Amazon business. Report types are specified using the ReportTypes
  enumeration.

Reports API reference
=====================

.. autoclass:: Reports
   :members:
   :exclude-members: ReportType, Schedule, ProcessingStatus

Enums
=====

.. autoclass:: mws.Reports.ReportType
   :show-inheritance:
   :members:
   :undoc-members:

   .. rubric:: Available values

   You can use either the Enum instance itself or its string value as an
   argument in relevant request methods. Each of the below examples may be
   used in a request for a flat file of open listings:

   .. code-block:: python

      from mws import Reports

      my_report_type = Reports.ReportType.INVENTORY
      # OR
      my_report_type = Reports.ReportType.INVENTORY.value
      # OR
      my_report_type = '_GET_FLAT_FILE_OPEN_LISTINGS_DATA_'

.. autoclass:: mws.Reports.Schedule
   :show-inheritance:
   :members:
   :undoc-members:

   .. rubric:: Available values

   Several schedule frequencies are provided by Amazon, and this Enum
   provides easy access to all of them through several aliases for each
   schedule type.

.. autoclass:: mws.Reports.ProcessingStatus
   :show-inheritance:
   :members:
   :undoc-members:
