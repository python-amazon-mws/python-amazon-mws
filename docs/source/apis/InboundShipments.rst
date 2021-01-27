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

.. autoclass:: mws.apis.inbound_shipments.InboundShipments
   :members:

Data models
===========

.. automodule:: mws.models.inbound_shipments

   .. autoclass:: Address
   .. autoclass:: PrepDetails
   .. autoclass:: InboundShipmentPlanRequestItem
   .. autoclass:: InboundShipmentItem
   .. autofunction:: shipment_items_from_plan

Enums
=====

.. autoclass:: PrepInstruction
   :show-inheritance:
   :members:
   :undoc-members:

.. autoclass:: ItemCondition
   :show-inheritance:
   :members:
   :undoc-members:
