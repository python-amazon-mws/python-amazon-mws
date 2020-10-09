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

Next, set up your **ship-from address**, which is required for all of the calls related to shipment planning,
creation, or updating.

The simplest way to get started with a ship-from address is to create one using the
:py:class:`Address <mws.models.inbound_shipments.Address>` model:

.. code-block:: python

    from mws.models.inbound_shipments import Address

    my_address = Address(
        name="My Warehouse",
        address_line_1="555 Selling Stuff Lane",
        address_line_2="Suite 404",
        city="New York",
        district_or_county="Brooklyn",
        state_or_province_code="NY",
        country_code="US",
        postal_code="11265",
    )

This model closely follows the structure of MWS's `Datatype of the same name
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#Address>`_.
python-amazon-mws can use these models as arguments to certain request methods, and will
correctly convert them to parameterized keys and values:

.. code-block:: python

    my_address.to_dict()
    # {'Name': 'My Warehouse', 'AddressLine1': '555 Selling Stuff Lane', ...}
