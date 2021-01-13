Managing Fulfillment Inbound (FBA) Shipments
############################################

.. include:: /newFeaturesTopNote100dev16.rst
.. note:: Examples in this document use :doc:`MWSResponse preview features <../reference/MWSResponse>`.

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

In any case, supplying a ``from_address`` argument to one of these methods will be used as an override, regardless of
the address stored within the API instance.

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

Other arguments you can provide include:

- ``country_code`` *or* ``subdivision_code``, the country or country subdivision you are planning to send a shipment to.
  ``country_code`` defaults to ``"US"``; ``subdivision_code`` (which refers to a subdivision of India specifically)
  defaults to ``None``.

  - According to `MWS documentation
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipmentPlan.html>`_,
    providing both options will return an error.

- ``label_preference``, a preference for label preparation. Defaults to ``None``, which MWS may interpret
  as "SELLER_LABEL" internally.

And note that the ``from_address`` argument is optional if the address has been
`stored on the API instance <#optional-store-your-ship-from-address-on-the-api-instance>`_.

Processing shipment plans
=========================

If our request to create shipment plans was successful, MWS will respond with an XML document containing plan details.
python-amazon-mws will :doc:`automatically parse this response <parsedXMLResponses>`, giving us access to the
Python representation of the response in ``resp.parsed``.

For reference, we will use the following example XML response from ``create_inbound_shipment_plan``. You can access
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

Gathering shipment details
--------------------------

To begin, we can access each shipment plan in the parsed response like so:

.. code-block:: python

    # Using the `resp` object from our previous examples
    for plan in resp.parsed.InboundShipmentPlans.member:
        ...

Each ``plan`` contains metadata required for creating a new shipment. These include:

- ``plan.ShipmentId``, the FBA shipment ID Amazon generates for the new shipment plan.
- ``plan.DestinationFulfillmentCenterId``, the short code for a Fulfillment Center planning to receive this shipment.
- ``plan.LabelPrepType``, the label preparation type for this shipment.

In addition to these data points, you should consider gathering the following data as arguments for the
``create_inbound_shipment`` request method:

- ``shipment_name`` (required), a human-readable name to help identify your shipment without relying on shipment IDs.
- ``shipment_status``, the initial status of the shipment. Defaults to "WORKING", indicating the shipment will remain
  "open" so that items and quantities can still be changed before it is shipped.

  The following constants can be used for this argument:

  - ``InboundShipments.STATUS_WORKING``
  - ``InboundShipments.STATUS_SHIPPED``
  - ``InboundShipments.STATUS_CANCELLED``
  - ``InboundShipments.STATUS_CANCELED`` (alias for ``STATUS_CANCELLED``)

- ``case_required``, a boolean indicating that items in the shipment are either *all case-packed* (if ``True``) or
  *all loose items* (if ``False``). Defaults to ``False``.
- ``box_contents_source``, a string indicating a source of box content data for packages within the shipment, or
  ``None`` indicating no box contents source. Defaults to ``None``.

  The following constants can be used for this argument:

  - ``InboundShipments.BOX_CONTENTS_FEED``, indicating contents will be provided in a :doc:`Feed <../apis/Feeds>` of type
    ``_POST_FBA_INBOUND_CARTON_CONTENTS_``.
  - ``InboundShipments.BOX_CONTENTS_2D_BARCODE``, indicating contents will be provided using 2D barcodes present
    on the cartons of the shipment.

We will illustrate how to use these data points later in this doc.

Converting plan items to shipment items
---------------------------------------

While the request to ``create_inbound_shipment_plan`` makes use of the
:py:class:`InboundShipmentPlanRequestItem <mws.models.inbound_shipments.InboundShipmentPlanRequestItem>` model to
transmit item data, this model is not sufficient for passing data to ``create_inbound_shipment`` and
``update_inbound_shipment`` requests, as they require slightly different parameters. We will need to use the
:py:class:`InboundShipmentItem <mws.models.inbound_shipments.InboundShipmentItem>` model, instead.

We can pass data to this model in one of three ways:

1. Manually processing item data from the response:

   .. code-block:: python

      from mws.models.inbound_shipments import InboundShipmentItem

      for plan in resp.parsed.InboundShipmentPlans.member:
          shipment_items = []
          for item in plan.Items.member:
              new_item = InboundShipmentItem(
                  sku=item.SellerSKU,
                  quantity=item.Quantity,
              )
              shipment_items.append(new_item)

2. Using :py:meth:`InboundShipmentItem.from_plan_item <mws.models.inbound_shipments.InboundShipmentItem.from_plan_item>`
   to construct an item automatically from each item in the response:

   .. code-block:: python

      from mws.models.inbound_shipments import InboundShipmentItem

      for plan in resp.parsed.InboundShipmentPlans.member:
          shipment_items = []
          for item in plan.Items.member:
              new_item = InboundShipmentItem.from_plan_item(item)
              shipment_items.append(new_item)

3. Using helper method :py:func:`shipment_items_from_plan <mws.models.inbound_shipments.shipment_items_from_plan>`
   to return a list of items from the entire plan automatically:

   .. code-block:: python

      from mws.models.inbound_shipments import shipment_items_from_plan

      for plan in resp.parsed.InboundShipmentPlans.member:
          shipment_items = shipment_items_from_plan(plan)

.. note:: Using ``InboundShipmentItem.from_plan_item`` or ``shipment_items_from_plan``, each item will automatically
   store the ``fnsku`` of each planned item. This data is ignored in calls to ``create_inbound_shipment`` and
   ``update_inbound_shipment``, but can be useful for tracking items internally.

Using either of these methods, the list of ``shipment_items`` can be used as the ``items`` argument to either the
``create_inbound_shipment`` or ``update_inbound_shipment`` request method.

.. rubric:: Adding ``quantity_in_case`` and ``release_date`` values

Item data provided by a ``plan`` is sufficient for most data required for items, but some data points must be
added manually:

- Case-pack information, specifically the ``quantity_in_case`` argument, is not supplied by the response from
  ``create_inbound_shipment_plan``, even if this information was provided in the request itself.
- Pre-order items must provide an additional ``release_date`` data point.

In the first two examples `above <#converting-plan-items-to-shipment-items>`_, these data points can be added as
arguments when constructing the new item:

.. code-block:: python
    :emphasize-lines: 5-6,12-13

    # using InboundShipmentItem(...):
    new_item = InboundShipmentItem(
        sku=item.SellerSKU,
        quantity=item.Quantity,
        quantity_in_case=...,
        release_date=...,
    )

    # using InboundShipmentItem.from_plan_item(...):
    new_item = InboundShipmentItem.from_plan_item(
      item,
      quantity_in_case=...,
      release_date=...,
    )

    # Confirm this data has been added:
    print(new_item.quantity_in_case, new_item.release_date)

In either case, when working with multiple items per shipment plan, you will need to determine which SKU these data
refer to. You should be able to rely on ``item.SellerSKU`` to identify those SKUs.

.. rubric:: Adding extra data when processing items in bulk

When processing a planned shipment's items in bulk, adding ``quantity_in_case`` and/or ``release_date`` values to
each item can be done using the ``overrides`` argument to ``shipment_items_from_plan``.

``overrides`` expects a dictionary with SellerSKUs as its keys. The values of this dict can be either:

- A dict containing keys ``quantity_in_case`` and/or ``release_date`` (all other keys are ignored):

  .. code-block:: python

      overrides = {
          'mySku1': {
              'quantity_in_case': 12,
              'release_date': datetime.datetime(2020-12-25),
          },
      }

- An instance of :py:class:`ExtraItemData <mws.models.inbound_shipments.ExtraItemData>`:

  .. code-block:: python

      from mws.models.inbound_shipments import ExtraItemData

      overrides = {
          'mySku2': ExtraItemData(
              quantity_in_case=12,
              release_date=datetime.datetime(2020-12-25),
          ),
      }

You should construct this set of overrides for all SKUs sent in your original request to
``create_inbound_shipment_plan``. You can then use the same set of overrides on any planned shipment resulting
from that request:

.. code-block:: python

    overrides = {...}

    for plan in resp.parsed.InboundShipmentPlans.member:
        shipment_items = shipment_items_from_plan(plan, overrides=overrides)

Creating shipments
==================

Putting everything together up to this point, we can create a new FBA shipment using the
:py:meth:`create_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.create_inbound_shipment>`
method:

.. code-block:: python

    from mws.models.inbound_shipments import ExtraItemData, shipment_items_from_plan

    # with optional overrides
    overrides = {
        'mySku1': ExtraItemData(...),
        'mySku2': ExtraItemData(...),
    }

    for plan in resp.parsed.InboundShipmentPlans.member:
        # Gather our items for the planned shipment
        shipment_items = shipment_items_from_plan(plan, overrides=overrides)

        # Send the request to create a new shipment
        new_shipment_resp = inbound_api.create_inbound_shipment(
            shipment_id=plan.ShipmentId,
            shipment_name="My Shiny New FBA Shipment",
            destination=plan.DestinationFulfillmentCenterId,
            items=shipment_items,
            label_preference=plan.LabelPrepType,
        )

For help with additional arguments - such as ``shipment_status``, ``case_required``, ``box_contents_source``,
or ``from_address`` - see `Gathering shipment details`_.

Updating shipments
==================

Creating a shipment is not the end of the story, of course. It is sometimes necessary to make changes to an
already-created shipment. For this, we use
:py:meth:`update_inbound_shipment <mws.apis.inbound_shipments.InboundShipments.update_inbound_shipment>`.

``update_inbound_shipment``'s arguments are identical to those of ``create_inbound_shipment``, with the exception that
all arguments besides ``shipment_id`` are optional. Generally, supplying a value to one of those arguments will
overwrite that value of the given shipment, such as:

- Setting ``shipment_status=InboundShipments.STATUS_CANCELLED`` to cancel a shipment;
- Changing the ``from_address``;
- etc.

Changing item quantities
------------------------

Item quantities on a shipment can be changed by providing a list of ``InboundShipmentItem`` instances for the ``items``
argument of ``update_inbound_shipment``. The details of the submitted items will overwrite details of those items in the
existing shipment based on matching SellerSKUs.

Amazon will expect the *total* quantity for an item: there is no mechanism for adding or subtracting a quantity from
the existing total. For example, if a shipment contains **24** units of an item and you want to add **12** of that item,
you will need to submit a total quantity of **36** in the update request:

.. code-block:: python

    resp = inbound_api.update_inbound_shipment(
        shipment_id="FBAMYSHIPMENT",
        items=[InboundShipmentItem(sku="MySku1", quantity=36)]
    )

It is up to you how you keep track of these quantity changes in your process. One way might be to cache these details
in some local database. Another might be querying the current total quantity using a request to
:py:meth:`list_inbound_shipment_items <mws.apis.inbound_shipments.InboundShipments.list_inbound_shipment_items>`, then
calculating the new total:

.. code-block:: python

    my_shipment = "FBAMYSHIPMENT"
    # Set our change quantities as "deltas", with SKU as key and the change as value
    quantity_deltas = {
        'mySku1': 12,  # add 12
        'mySku2': -6,  # remove 6
    }

    update_items = []

    list_resp = inbound_api.list_inbound_shipment_items(shipment_id=my_shipment)
    for item in list_resp.parsed.ItemData.member:
        if item.SellerSKU in quantity_deltas:
            new_quantity = item.QuantityShipped + quantity_deltas[item.SellerSKU]

            # Negative quantities not permitted, so set 0 as a minimum using `max`:
            new_quantity = max([new_quantity, 0])

            # Add items to a list for updates:
            update_items.append(
                InboundShipmentItem(item.SellerSKU, new_quantity)
            )

    if update_items:
        update_resp = inbound_api.update_inbound_shipment(
            shipment_id=my_shipment,
            items=update_items,
        )

Adding items from a new shipment plan
-------------------------------------

Under certain conditions, items from a new shipment plan can be added to one of your existing shipments in WORKING
status. In this way, you can keep a shipment "open" in your own facility, adding new items to the same shipment before
"closing" it and sending it to Amazon's fulfillment network.

Follow the same steps as `Requesting a shipment plan`_, then inspect the contents of the planned shipments (see
`Processing shipment plans`_).

Generally, you *may* be able to add newly-planned items to an existing shipment if the
following details match in the target "WORKING" shipment:

- ``DestinationFulfillmentCenterId``
- ``LabelPrepType``
- Whether both shipments are designated for **hazmat** items.

  .. note:: In the author's experience, this detail may not be apparent through MWS ahead of time: you may simply
     need to attempt to add the item and handle whatever error occurs afterward.

     Forgiveness instead of permission, as they say.

- Whether the two shipments require **case packs** or not.

This list is not exhaustive, so use best judgment and follow Amazon's guidance where necessary.

If you determine that a planned item *can* be added to one of your existing shipments, add that item to an
``update_inbound_shipment`` request for the given shipment ID.

As mentioned in `Changing item quantities`_, remember to use the **total** quantity of an item being updated, not
the change in quantity, if the item is already present in the given shipment. If you are not tracking these quantities
in your own application, you may wish to send a request to
:py:meth:`list_inbound_shipment_items <mws.apis.inbound_shipments.InboundShipments.list_inbound_shipment_items>` to
obtain the current quantity of a matching item *before* sending the update request.
