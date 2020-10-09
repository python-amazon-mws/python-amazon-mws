Managing Fulfillment Inbound (FBA) Shipments
############################################

MWS handles **Fulfillment Inbound Shipments**, also known as **FBA** (for "Fulfillment By Amazon")
through the `Fulfillment Inbound Shipment API section
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html>`_.
Users should familiarize themselves with this section of the API in MWS documentation before getting started.

In python-amazon-mws, this API is covered by
:py:class:`mws.InboundShipments <mws.apis.inbound_shipments.InboundShipments>`.

Setting up your API instance
============================

To begin, create an instance of ``InboundShipments`` as you would any other API class in python-amazon-mws:

.. code-block:: python

    from mws import InboundShipments

    # assuming MWS credentials are stored in environment variables (your setup may vary):
    inbound_api = InboundShipments(
        access_key=os.environ("MWS_ACCESS_KEY"),
        secret_key=os.environ("MWS_SECRET_KEY"),
        account_id=os.environ("MWS_ACCOUNT_ID"),
    )

One more step is needed, unlike other API classes: storing your **ship from address**:

.. code-block:: python

    inbound_api.from_address = {
        "name": "My Warehouse",
        "address_1": "555 Selling Stuff Lane",
        "address_2": "Suite 404",
        "city": "New York",
        "district_or_county": "Brooklyn",
        "state_or_province": "NY",
        "postal_code": "11265",
        "country": "US",
    }

*To be continued*.
