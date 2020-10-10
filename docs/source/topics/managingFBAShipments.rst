Managing Fulfillment Inbound (FBA) Shipments
############################################

MWS handles **Fulfillment Inbound Shipments**, also known as **FBA** (for "Fulfillment By Amazon")
through the `Fulfillment Inbound Shipment API section
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html>`_.
Users should familiarize themselves with this section of the API in MWS documentation before getting started.

In python-amazon-mws, this API is covered by
:py:class:`mws.InboundShipments <mws.apis.inbound_shipments.InboundShipments>`.

Basic workflow - planning to creation
=====================================

Let's step through a basic workflow for creating a new FBA shipment. You will need:

- A valid ship-from address, presumably the location of your facility where shipments will originate.
- A list of Seller SKUs for items in your catalog to be added to the shipment(s).

Create the API instance
-----------------------

To begin, create an instance of ``InboundShipments`` as you would any other API class in python-amazon-mws.
You will then use this API class instance to initiate requests to MWS.

.. code-block:: python

    from mws import InboundShipments

    # assuming MWS credentials are stored in environment variables (your setup may vary):
    inbound_api = InboundShipments(
        access_key=os.environ("MWS_ACCESS_KEY"),
        secret_key=os.environ("MWS_SECRET_KEY"),
        account_id=os.environ("MWS_ACCOUNT_ID"),
    )

Store your ship-from address
----------------------------

Next, set up your ship-from address, which is required for the three core operations related to FBA shipments:
planning, creation, and updating.

The simplest way to store your ship-from address is to create an instance of the
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
You should refer to MWS documentation for this Datatype to ensure all necessary elements of your address are included.

Create your list of items
-------------------------

Gather items together to add to a request as a list of dicts.
Each item dict must contain keys ``sku`` and ``quantity``,
and can optionally include keys ``quantity_in_case`` (for case-packed items),
``asin``, and/or ``condition``.

.. code-block:: python

    my_items = [
        {
            'sku': 'MY-SKU-1',
            'quantity': 36,
            # Optional:
            'quantity_in_case': 12,
            'asin': 'B01234567',
            'condition': 'NewItem',
        },
        {
            'sku': 'MY-SKU-1',
            'quantity': 12,
        }
    ]

.. note:: This needs to be replaced by a model. More to come later.

Send your request
-----------------

*TODO*.
