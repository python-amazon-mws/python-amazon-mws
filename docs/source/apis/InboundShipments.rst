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

   .. rubric:: Available values:
   .. autoattribute:: POLYBAGGING
   .. autoattribute:: BUBBLEWRAPPING
   .. autoattribute:: TAPING
   .. autoattribute:: BLACKSHRINKWRAPPING
   .. autoattribute:: LABELING
   .. autoattribute:: HANGGARMENT

.. autoclass:: ItemCondition
   :show-inheritance:

   .. rubric:: Available values:
   .. autoattribute:: NEW_ITEM
   .. autoattribute:: NEW_WITH_WARRANTY
   .. autoattribute:: NEW_OEM
   .. autoattribute:: NEW_OPEN_BOX
   .. autoattribute:: USED_LIKE_NEW
   .. autoattribute:: USED_VERY_GOOD
   .. autoattribute:: USED_GOOD
   .. autoattribute:: USED_ACCEPTABLE
   .. autoattribute:: USED_POOR
   .. autoattribute:: USED_REFURBISHED
   .. autoattribute:: COLLECTIBLE_LIKE_NEW
   .. autoattribute:: COLLECTIBLE_VERY_GOOD
   .. autoattribute:: COLLECTIBLE_GOOD
   .. autoattribute:: COLLECTIBLE_ACCEPTABLE
   .. autoattribute:: COLLECTIBLE_POOR
   .. autoattribute:: REFURBISHED_WITH_WARRANTY
   .. autoattribute:: REFURBISHED
   .. autoattribute:: CLUB
