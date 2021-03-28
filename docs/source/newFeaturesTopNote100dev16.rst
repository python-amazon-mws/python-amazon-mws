.. warning:: The following includes features added in **v1.0dev16** related to Datatype models.
   Models can be called from the API class that uses them. For example, to use the
   :py:class:`Address <mws.InboundShipments.Address>` model attached to the
   :py:class:`InboundShipments <mws.InboundShipments>` API:

   .. code-block:: python

      from mws import InboundShipments

      # from the class itself:
      my_address = InboundShipments.Address(...)

      # or from an instance of the class:
      inbound_shipments_api = InboundShipments(...)
      my_address = inbound_shipments_api.Address(...)
