Generic Requests
################

.. versionadded:: 1.0dev15
   Generic request support added.

While most MWS operations are well-covered by python-amazon-mws with dedicated and purpose-built request methods,
Amazon may occasionally update MWS to include new parameters that we do not yet provide access to. Either that, or
you just want lower-level access to input your own request, without going through the rest of python-amazon-mws
to do so.

For these situations, you can use :py:meth:`APIClass.generic_request() <mws.mws.MWS.generic_request>`, available
in all API classes that inherit from the base ``MWS`` class.

Back to basics
==============

To use ``.generic_request()``, you must first instantiate the API class that contains the operation you want to send.
Using the correct API class is required, as the base URI used the build the request is different for each API section.
For instance, to use the ``ListOrders`` operation in the ``Orders`` API, you would create an
:py:class:`Orders <mws.apis.orders.Orders>` instance.

With the class instantiated, specify the operation to call as the ``action`` arg to ``.generic_request()``;
then provide a dict of parameters for your request as ``params``:

.. code-block:: python

    import datetime

    from mws import Orders, Marketplaces

    my_marketplace_ids = [
        Marketplaces.US.marketplace_id,
        Marketplaces.UK.marketplace_id,
    ]

    orders_api = Orders(MY_ACCESS_KEY, MY_SECRET_KEY, MY_ACCOUNT_ID)

    response = orders_api.generic_request(
        action="ListOrders",
        params={
            "MarketplaceId.Id": my_marketplace_ids,
            "CreatedAfter": datetime.datetime(2020, 8, 28),
        }
    )

The above is equivalent to calling
:py:meth:`Orders.list_orders <mws.apis.orders.Orders.list_orders>` with:

.. code-block:: python

    response = orders_api.list_orders(
        marketplace_ids=my_marketplace_ids,
        created_after=datetime.datetime(2020, 8, 28),
    )

Key differences between a generic request and the "pythonic" version include:

- The ``action`` must be specified for each call, using the case-sensitive name of the MWS operation
  (usually in CapCase with no underscores).
- ``params`` must include case-sensitive keys matching the parameters required for the MWS operation, according to
  Amazon documentation.
- The ``params`` dict is :ref:`flattened <param_flat_dict_ref>`, such that nested lists and dicts in ``params`` are
  keyed and enumerated into appropriate request parameter keys.

.. _param_flat_dict_ref:

Parameter dict flattening
=========================

Generic requests make use of :py:func:`flat_param_dict() <mws.utils.params.flat_param_dict>` to convert nested
Mappings and Iterables into a "flat" set of key-value pairs.

.. rubric:: Rules

- Nested mapping objects (``dict``, ``DotDict``, etc.) are recursively flattened, joining the keys of the child
  mapping to the parent key with ``.``.
- Nested iterables (``list``, ``tuple``, ``set``, etc.) are enumerated with a 1-based index, with each index
  joined to the parent key with ``.``.
- All nested mappings and iterables are processed recursively, flattening other mappings and iterables along the way.

.. rubric:: Example

.. code-block:: python

    value = {
        "a": 1,
        "b": "hello",
        "c": [
            "foo",
            "bar",
            {
                "spam": "ham",
                "eggs": [
                    5,
                    6,
                    7,
                ],
            },
        ],
    }

The above, when passed through ``flat_param_dict()``, produces:

.. code-block:: python

    {
        "a": 1,
        "b": "hello",
        "c.1": "foo",
        "c.2": "bar",
        "c.3.spam": "ham",
        "c.3.eggs.1": 5,
        "c.3.eggs.2": 6,
        "c.3.eggs.3": 7,
    }

- "a" and "b" keys point to non-dict, non-sequence values (not including strings),
  so they return their original values.
- "c" contains an iterable (list), which is enumerated with a 1-based index.
  Each index is concatenated to "c" with ".", creating keys "c.1" and "c.2".
- At "c.3", another nested object was found. This is processed recursively,
  and each key of the resulting dict is concatenated to the parent "c.3"
  to create multiple keys in the final output.
- The same occurs for "c.3.eggs", where an iterable is found and is enumerated.
- The final output should always be a flat dictionary with key-value pairs.

.. rubric:: Using a prefix

``flat_param_dict`` accepts a ``prefix`` argument, used mainly when flattening nested objects recursively.
When provided, all keys in the resulting output will begin with ``prefix + '.'``:

.. code-block:: python

    # Using the same `value` as before:
    flat_param_dict(value, prefix="example")

    # Produces:
    {
        "example.a": 1,
        "example.b": "hello",
        "example.c.1": "foo",
        "example.c.2": "bar",
        "example.c.3.spam": "ham",
        "example.c.3.eggs.1": 5,
        "example.c.3.eggs.2": 6,
        "example.c.3.eggs.3": 7,
    }

Generic request component methods
=================================

.. automethod:: mws.mws.MWS.generic_request

.. autofunction:: mws.utils.params.flat_param_dict
