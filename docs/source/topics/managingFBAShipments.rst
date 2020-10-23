Managing Fulfillment Inbound (FBA) Shipments
############################################

.. note:: Examples in this document use :doc:`MWSResponse preview features
   <../reference/MWSResponse>`.

MWS handles **Fulfillment Inbound Shipments**, also known as **FBA** (for "Fulfillment By Amazon")
through the `Fulfillment Inbound Shipment API section
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html>`_.
Users should familiarize themselves with this section of the API in MWS documentation before getting started.

In python-amazon-mws, this API is covered by
:py:class:`mws.InboundShipments <mws.apis.inbound_shipments.InboundShipments>`.

Basic steps to create a shipment in MWS
=======================================

For a quick overview, MWS requires the following pattern to creating FBA shipments:

1. Send a request to
   :py:meth:`create_inbound_shipment_plan <mws.apis.inbound_shipments.InboundShipments.create_inbound_shipment_plan>`
   with all items you wish to ship, along with their quantities, conditions, prep details, and so on.
2. MWS will respond with one or more **shipment plans**, indicating where to send each of your items. Multiple shipments
   may be requested, and the same item may have its quantities split between these shipments. Each plan also returns
   the FBA Shipment ID needed to create a shipment, as well as the ID and address of the Fulfillment Center that will
   expect that shipment.
3. For each shipment plan, send a
   :py:meth:`create_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.create_inbound_shipment>`
   request with the items, quantities, and other details identified in the plan.

   - Optionally, it is possible to use
     :py:meth:`update_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.update_inbound_shipment>`
     to add planned items for a new shipment to an existing shipment under certain conditions.
     **Using this option improperly may violate the terms of your seller account, so use with caution!**

We'll look at each of these steps in detail below.

.. warning:: MWS does not provide a sandbox for testing functionality. If you use examples from this
   guide for testing purposes, you will need to use **live data** to do it, and will be creating
   **real FBA shipments**. Please use this guide at your own risk.

   Some things to keep in mind when testing this functionality:

   - Make note of any Shipment IDs for shipments you generate with these examples.
   - Use custom shipment names to help identify test shipments, such as "TEST_IGNORE",
     so you can more easily find those shipments in Seller Central, if you lose track of them in testing.
   - Inform other members of your organization that you are conducting tests, particularly if they use Seller Central
     or other MWS-related tooling to check on shipment statuses.
   - Leaving test shipments in WORKING or SHIPPED statuses may have an impact on your product inventory.
     We advise changing these to CANCELLED when you complete your testing.

Requesting a shipment plan
==========================

We start by informing Amazon we have items we wish to ship, requesting a **shipment plan** through MWS.

You will need:

- MWS credentials to authenticate with MWS (not in scope for these docs).
- A valid **ship-from address**, presumably the address of the facility where you will be shipping items from.
- A list of Seller SKUs for items in your product catalog to add to new shipments.

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

Create your ship-from address
-----------------------------

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

.. note:: If you're curious, you can use any model's ``.to_params()`` method to return a dictionary containing the
   request parameters of that model and their values.

   .. code-block:: python

       my_address.to_params()
       # {'Name': 'My Warehouse', 'AddressLine1': '555 Selling Stuff Lane', 'AddressLine2': 'Suite 404', 'City': 'New York', 'DistrictOrCounty': 'Brooklyn', 'StateOrProvinceCode': 'NY', 'CountryCode': 'US', 'PostalCode': '11265'}

   This method also accepts a ``prefix`` argument, which adds the prefix string plus ``'.'`` before each parameter key:

   .. code-block:: python

       my_address.to_params("ShipFromAddress")
       # {'ShipFromAddress.Name': 'My Warehouse', 'ShipFromAddress.AddressLine1': '555 Selling Stuff Lane', 'ShipFromAddress.AddressLine2': 'Suite 404', 'ShipFromAddress.City': 'New York', 'ShipFromAddress.DistrictOrCounty': 'Brooklyn', 'ShipFromAddress.StateOrProvinceCode': 'NY', 'ShipFromAddress.CountryCode': 'US', 'ShipFromAddress.PostalCode': '11265'}

   Using ``.to_params()`` in your own code is usually not necessary, as most request methods will convert the
   model instance to parameters automatically.

*Optional*: Store your ship-from address on the API instance
************************************************************

If you plan to make several requests in a row related to the same ship-from address, you can store the address on
an instance of ``InboundShipments`` API as ``.from_address``:

.. code-block:: python

    inbound_api.from_address = my_address

When using this option, you can omit passing ``from_address=my_address`` as an argument in the request examples below.
All relevant request methods (``create_inbound_shipment_plan``, ``create_inbound_shipment``, and
``update_inbound_shipment``) will pass the stored ``from_address`` to these requests automatically.

Request a shipment plan
------------------------

Amazon's workflow for creating a shipment uses the following pattern:

1. Create a **shipment plan** by sending a ``CreateInboundShipmentPlan`` request. This informs Amazon which items
   you intend to ship and the total quantity for each, as well as any prep details, item conditions, and so on.
2. MWS responds with one or more planned shipments for those items. They may request certain items are sent to
   certain fulfillment centers, and may even split quantities for some items to multiple facilities. You must use
   the planned shipments to create your actual shipments.
3. Send a ``CreateInboundShipment`` request for *each* planned shipment. This should include the ShipmentId,
   DestinationFulfillmentCenterId, and any items and quantities returned in the response from
   ``CreateInboundShipmentPlan``, so that the new shipment matches the planned one.
4. A successful request to ``CreateInboundShipment`` will create an FBA Shipment, which you can further interact with
   through MWS or on Seller Central.

We'll start by creating the shipment plan, for which we need a list of items.

Building a list of planned items
********************************

Each item in your shipment plan can be represented by an instance of
:py:class:`InboundShipmentPlanRequestItem <mws.models.inbound_shipments.InboundShipmentPlanRequestItem>`,
which closely follows the `MWS Datatype of the same name
<https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#InboundShipmentPlanRequestItem>`_:

.. code-block:: python

    from mws.models.inbound_shipments import InboundShipmentPlanRequestItem

    item1 = InboundShipmentPlanRequestItem('MY-SKU-1', 36)
    item2 = InboundShipmentPlanRequestItem('MY-SKU-2', 12)

    my_items = [item1, item2]

The only required arguments for the model are ``sku`` and ``quantity``, which are sufficient for loose item
shipments of new items when prep details do not need to be specified.

.. note:: You can add more detail to an ``InboundShipmentPlanRequestItem`` instance, depending on your needs.
   If you were sending, for example, an item that comes in case-packs of 12, in NewOEM condition, with a particular
   ASIN, and requires Amazon to prep each item with Polybagging; you might create that item model like so:

   .. code-block:: python

       from mws.models.inbound_shipments import (
           InboundShipmentPlanRequestItem,
           ItemCondition,
           PrepDetails,
           PrepInstruction,
       )

       detailed_item = InboundShipmentPlanRequestItem(
           sku='MY-OTHER-SKU',
           quantity=48,
           quantity_in_case=12,
           asin='B0123456789',
           condition=ItemCondition.NEW_OEM,  # or the string "NewOEM"
           prep_details_list=[
               PrepDetails(
                   prep_instruction=PrepInstruction.POLYBAGGING,  # or "Polybagging"
                   prep_owner=PrepDetails.AMAZON  # or "AMAZON"
               )
           ]
       )

   Again for the curious, ``detailed_item.to_params()`` looks like so:

   .. code-block:: python

      detailed_item.to_params()
      # {'SellerSKU': 'MY-OTHER-SKU', 'ASIN': 'B0123456789', 'Condition': 'NewOEM', 'Quantity': 48, 'QuantityInCase': 12, 'PrepDetailsList.member.1.PrepInstruction': 'Polybagging', 'PrepDetailsList.member.1.PrepOwner': 'AMAZON'}

Sending the request
*******************

Now that we have our items handy, it's time to make our request for a shipment plan:

.. code-block:: python

    # using `inbound_api`, `my_address` and `my_items` from previous examples
    resp = inbound_api.create_inbound_shipment_plan(my_items, from_address=my_address)

Processing shipment plans
=========================

If our request to create shipment plans was successful, MWS will respond with an XML document containing plan details.
python-amazon-mws will :doc:`automatically parse this response <parsedXMLResponses>`, giving us access to the
Python representation of the response in ``resp.parsed``.

For reference, let's look at an example of an XML response from ``create_inbound_shipment_plan``. You can access
this document in your own response by checking ``resp.original.text``:

.. code-block:: xml

    <?xml version="1.0"?>
    <CreateInboundShipmentPlanResponse
      xmlns="http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/">
      <CreateInboundShipmentPlanResult>
        <InboundShipmentPlans>
          <member>
            <DestinationFulfillmentCenterId>ABE2</DestinationFulfillmentCenterId>
            <LabelPrepType>SELLER_LABEL</LabelPrepType>
            <ShipToAddress>
              <City>Breinigsville</City>
              <CountryCode>US</CountryCode>
              <PostalCode>18031</PostalCode>
              <Name>Amazon.com</Name>
              <AddressLine1>705 Boulder Drive</AddressLine1>
              <StateOrProvinceCode>PA</StateOrProvinceCode>
            </ShipToAddress>
            <EstimatedBoxContentsFee>
              <TotalUnits>10</TotalUnits>
              <FeePerUnit>
                <CurrencyCode>USD</CurrencyCode>
                <Value>0.10</Value>
              </FeePerUnit>
              <TotalFee>
                <CurrencyCode>USD</CurrencyCode>
                <Value>10.0</Value>
              </TotalFee>
            </EstimatedBoxContentsFee>
            <Items>
              <member>
                <FulfillmentNetworkSKU>FNSKU00001</FulfillmentNetworkSKU>
                <Quantity>1</Quantity>
                <SellerSKU>SKU00001</SellerSKU>
                <PrepDetailsList>
                  <PrepDetails>
                    <PrepInstruction>Taping</PrepInstruction>
                    <PrepOwner>AMAZON</PrepOwner>
                  </PrepDetails>
                </PrepDetailsList>
              </member>
              <member>
                ...
              </member>
            </Items>
            <ShipmentId>FBA0000001</ShipmentId>
          </member>
          <member>
            ...
          </member>
        </InboundShipmentPlans>
      </CreateInboundShipmentPlanResult>
      <ResponseMetadata>
        <RequestId>babd156d-8b2f-40b1-a770-d117f9ccafef</RequestId>
      </ResponseMetadata>
    </CreateInboundShipmentPlanResponse>

Based on this example, we can see that each plan is represented by a ``InboundShipmentPlans.member`` node.
Multiple copies of the ``<member>`` XML element may be present, indicating more than one shipment is planned.
We'll take advantage of ``DotDict``'s :ref:`native iteration <dotdict_native_iteration>` to safely access these
multiple plan members, like so:

.. code-block:: python

    for plan in resp.parsed.InboundShipmentPlans.member:
        print(plan.DestinationFulfillmentCenterId)
        print(plan.LabelPrepType)
        print(plan.ShipToAddress.AddressLine1)
        # ...etc.

Each ``plan`` will also contain one or more Items, which (per the XML example) take the form ``plan.Items.member``.
We can again iterate on these item members to gather information on each of them:

.. code-block:: python

    for plan in resp.parsed.InboundShipmentPlans.member:
        ...
        for item in plan.Items.member:
            print(item.FulfillmentNetworkSKU)
            print(item.Quantity)
            # ...etc.

As mentioned, Amazon may
