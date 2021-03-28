InboundShipments
################

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html>`_:

  With the Fulfillment Inbound Shipment API section of Amazon Marketplace Web
  Service (Amazon MWS), you can create and update inbound shipments of inventory
  in Amazon's fulfillment network. You can also request lists of inbound
  shipments or inbound shipment items based on criteria that you specify.
  After your inventory has been received in the fulfillment network, Amazon
  can fulfill your orders regardless of whether you are selling on Amazon's
  retail web site or through other retail channels.

InboundShipments API reference
==============================

.. autoclass:: mws.InboundShipments
   :members:
   :exclude-members:
     Address,
     PrepDetails,
     InboundShipmentPlanRequestItem,
     InboundShipmentItem,
     PrepInstruction,
     ItemCondition,
     ExtraItemData,
     shipment_items_from_plan

Other tools
===========

.. module:: mws.models.inbound_shipments
.. note:: The following classes and utility functions are attached to the
   :py:class:`InboundShipments` class for convenient access. For example,
   the :py:class:`Address` model can be accessed like so:

   .. code-block:: python

      from mws import InboundShipments

      my_address = InboundShipments.Address(...)

      # or from an instance of InboundShipments:

      inbound_api = InboundShipments(...)
      my_address = inbound_api.Address(...)

.. todo:: get rid of the :type directives throughout code.

Data models
-----------

.. autoclass:: Address
   :members:
   :inherited-members:

.. autoclass:: PrepDetails
   :members:
   :inherited-members:

.. autoclass:: InboundShipmentPlanRequestItem
   :members:
   :inherited-members:

.. autoclass:: InboundShipmentItem
   :members:
   :inherited-members:

Enums
-----

.. autoclass:: PrepInstruction
   :show-inheritance:
   :members:
   :undoc-members:

.. autoclass:: ItemCondition
   :show-inheritance:
   :members:
   :undoc-members:

Utilities
---------

.. autofunction:: shipment_items_from_plan

   For example usage, see: :ref:`converting_plan_items_to_shipment_items`

.. autoclass:: ExtraItemData
