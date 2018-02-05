==========================================
Getting Started with ``python-amazon-mws``
==========================================

Prerequisites
=============

Use of this module requires access to `Amazon Marketplace Web
Services <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_IfNew.html>`__,
also called simply **MWS**. You will need to sign up with the service to
get your own set of credentials. The specific credentials you will need
are:

-  Access Key
-  Secret Key
-  Account ID
-  Auth Token (optional)

If credentials are missing or incorrect when calling the different
request methods, MWS will deny access, responding with an error.

Further, while this module provides assistance with building requests to
and parsing responses from MWS, you will need some familiarity with MWS
itself to use the data effectively. Refer to MWS Documentation (linked
above) for details.

From here on, we assume you are familiar with MWS, know which requests
to send, and know how to parse the response data in a meaningful way.
Our documentation is specific to how ``python-amazon-mws`` builds
requests and handles response, and what types of helper methods we
provide.

Key Points
==========

-  MWS is separated into a number of **APIs**, each of which contain
   many **operations**. ``python-amazon-mws`` defines each API as a
   separate class, subclassed from the base class ``MWS``. An API’s
   operations are defined as methods of that class.
-  Each MWS operation is covered here by a request method (in its
   appropriate API class) of the identical name. Note that while MWS
   operations are named using ``CamelCase`` style, request methods in
   ``python-amazon-mws`` are named using ``lowercase_with_underscores``
   style.

   -  Example: the operation
      `GetPrepInstructionsForSKU <http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForSKU.html>`__
      is covered by method ``get_prep_instructions_for_sku`` (in the
      ``InboundShipments`` class).
   -  Note that our code sometimes refers to operations as “actions”.
      This term is interchangeable.

-  We have **one exception** to the above rule: operations ending in
   “ByNextToken” may not be covered with an explicit
   ``by_next_token``-style method. Instead, we offer a ``next_token``
   keyword argument (kwarg) in the original method. If this kwarg is
   given to the method call, the appropriate “ByNextToken” operation
   will be called.

   -  Note that some ``by_next_token`` methods *are* defined in the
      current package. This is a deprecated style: these methods may be
      removed or aliased by the time of a 1.0 release.

API Class Names
===============

Each MWS API is covered by a separate class, all of which are subclasses
of the base ``MWS`` class. These APIsA select few APIs are covered by
classes of slightly different names. See here for all MWS APIs and the
classes that cover them:

+-------------------------------+---------------------------+
| MWS API                       | Class Name                |
+===============================+===========================+
| Feeds                         | ``Feeds``                 |
+-------------------------------+---------------------------+
| Finances                      | ``Finances``              |
+-------------------------------+---------------------------+
| Fulfillment Inbound Shipment  | ``InboundShipments``\ \*  |
+-------------------------------+---------------------------+
| Fulfillment Inventory         | ``Inventory``\ \*         |
+-------------------------------+---------------------------+
| Fulfillment Outbound Shipment | ``OutboundShipments``\ \* |
+-------------------------------+---------------------------+
| Merchant Fulfillment          | *not yet implemented*     |
+-------------------------------+---------------------------+
| Orders                        | ``Orders``                |
+-------------------------------+---------------------------+
| Products                      | ``Products``              |
+-------------------------------+---------------------------+
| Recommendations               | ``Recommendations``       |
+-------------------------------+---------------------------+
| Reports                       | ``Reports``               |
+-------------------------------+---------------------------+
| Sellers                       | ``Sellers``               |
+-------------------------------+---------------------------+
| Subscriptions                 | *not yet implemented*     |
+-------------------------------+---------------------------+

\* *Name of class not a perfect match for API name.*

Simple Example: ``get_service_status``
======================================

Each MWS API has a ``GetServiceStatus`` operation, which returns either
a GREEN, YELLOW, or RED status for that particular API.
``python-amazon-mws`` makes this accessible through a common
``get_service_status`` method.

For example, let us check the status of the Orders API:

.. code:: python

    import mws, os

    # set up our API instance using MWS credentials (as environment variables)
    orders_api = mws.Orders(
        access_key=os.environ['MWS_ACCESS_KEY'],
        secret_key=os.environ['MWS_SECRET_KEY'],
        account_id=os.environ['MWS_ACCOUNT_ID'],
        auth_token=os.environ['MWS_AUTH_TOKEN'], # optional
    )

    # make the call
    response = orders_api.get_service_status()

*Note*: Technically, ``get_service_status`` calls will pass without
checking credentials.

The output for all request methods is either a ``DictWrapper`` (for XML
content) or ``DataWrapper`` (for all others). The majority of our
responses will be ``DictWrapper``\ s containing a few main attributes:

-  ``response.original``: original response content stored as a string.
-  ``response.response``: HTTP response code for the request (usually
   200).
-  ``response.parsed``: an ``mws.utils.ObjectDict`` (a subclass of the
   built-in ``dict``) containing the parsed data from the response for
   easier access.

Using ``.parsed``
-----------------

The content of ``.parsed`` reads like a dict:

.. code:: python

    >>> response.parsed
    {'Status': {'value': 'GREEN'}, 'Timestamp': {'value': '2017-06-14T16:39:12.765Z'}}

Any of the keys of that dict can be accessed as an attribute:

.. code:: python

    >>> response.parsed.Status
    'GREEN'
    >>> response.parsed.Timestamp
    '2017-06-14T16:39:12.765Z'

All XML nodes from the parsed data are accessed in the same way.
Accessing a node with nothing but a value will return that value, while
accessing a node that has child nodes will return a new ObjectDict.

Optional: Accessing Values As Dict Keys
---------------------------------------

Optionally, you can access a node like a dict using key index syntax. Be
warned, while accessing a node as an attibute (i.e.
``parsed.Attribute``) will automatically return a value, using dict keys
or ``.get()`` will provide the ObjectDict instead:

.. code:: python

    >>> response.parsed['Status']
    {'value': 'GREEN'}
    >>> response.parsed.get('Status')
    {'value': 'GREEN'}
    >>> type(response.parsed['Status'])
    <class 'mws.utils.ObjectDict'>

To account for this, if you access a node with data using a dict key or
``.get()``, you must access its ``value`` attribute manually:

.. code:: python

    >>> response.parsed['Status'].value
    'GREEN'
    >>> response.parsed['Status']['value']
    'GREEN'

To cover all use cases, when testing if a node exists and to provide a
default, use a “double-get” like so:

.. code:: python

    response.parsed.get('Status', {}).get('value')

*This is, admittedly, not very intuitive. This will be adjusted in the
near future.*

Longer Example: ``Orders.list_order_items``
===========================================

Let’s get a little fancier (but only slightly). Suppose you are a
seller, a customer has placed an order, and you have their order ID in
hand. You may have gotten this ID from the response from
``Orders.list_orders()``, or someone emailed you out of the blue with
the order ID asking for assistance.

Getting order metadata - person’s name, shipping address, payment
method, etc. - is one thing, obtained from the ListOrders or GetOrder
calls; but these do not list out the items contained in an order. To get
that list, you need to call the
`ListOrderItems <http://docs.developer.amazonservices.com/en_US/orders-2013-09-01/Orders_ListOrderItems.html>`__
operation.

In ``python-amazon-mws``, this is called by using
``Orders.list_order_items()``:

.. code:: python

    orders_api = mws.Orders(...) # credentials go in here
    order_id = "902-3159896-1390916"
    response = orders_api.list_order_items(order_id)

Based on the MWS documentation (linked above) for this call, your
``reponse.parsed`` may look like so (formatted here for easier reading):

.. code:: python

    >>> response.parsed
    {
        'NextToken': {'value': 'MRgZW55IGNhcm5hbCBwbGVhc3VyZS6='},
        'AmazonOrderId': {'value': '058-1233752-8214740'},
        'OrderItems': {
            'OrderItem': [
                {
                    'ASIN': {'value': 'BT0093TELA'},
                    'OrderItemId': {'value': '68828574383266'},
                    'BuyerCustomizedInfo': {
                        'CustomizedURL': {'value': 'https://...'}
                    },
                    'SellerSKU': {'value': 'CBA_OTF_1'},
                    'Title': {'value': 'Example item name'},
                    'QuantityOrdered': {'value': '1'},
                    'QuantityShipped': {'value': '1'},
                    'ProductInfo': {
                        'NumberOfItems': {'value': '12'}
                    },
                    'PointsGranted': {
                        'PointsNumber': {'value': '10'},
                        'PointsMonetaryValue': {
                            'CurrencyCode': {'value': 'JPY'},
                            'Amount': {'value': '10.00'}
                        }
                    },
                    'ItemPrice': {
                        'CurrencyCode': {'value': 'JPY'},
                        'Amount': {'value': '25.99'}
                    },
                    'ShippingPrice': {
                        'CurrencyCode': {'value': 'JPY'},
                        'Amount': {'value': '1.26'}
                    },
                    'ScheduledDeliveryEndDate': {'value': '2013-09-09T01:30:00.000-06:00 '},
                    'ScheduledDeliveryStartDate': {'value': '2013-09-071T02:00:00.000-06:00 '},
                    'CODFee': {
                        'CurrencyCode': {'value': 'JPY'},
                        'Amount': {'value': '10.00'}
                    },
                    'CODFeeDiscount': {
                        'CurrencyCode': {'value': 'JPY'},
                        'Amount': {'value': '1.00'}
                    },
                    'GiftMessageText': {'value': 'For you!'},
                    'GiftWrapPrice': {
                        'CurrencyCode': {'value': 'JPY'},
                        'Amount': {'value': '1.99'}
                    },
                    'GiftWrapLevel': {'value': 'Classic'},
                    'PriceDesignation': {'value': 'BusinessPrice'}
                },
                ... # more OrderItem objects
            ]
        }
    }

Some notes first:

-  **List Location**: The XML for this example contains many
   **<OrderItem>** tags within the **<OrderItems>** tag, which is
   expected: this is the set of OrderItem objects to work on. In our
   parsed response, when many tags of the same name are all children of
   the same parent node, they will be made into a list of ObjectDicts
   that can be accessed from the same key they all share. In the
   example, ``OrderItems.OrderItem`` is that list.

   -  It may seem more intuitive to have a structure like
      ``{'OrderItems': [...]}`` instead of
      ``{'OrderItems': {'OrderItem': [...]}]}``, but that would mean
      removing an expected key from the parsed response data. Further,
      some responses may have other keys at the same node level, so we
      must ensure that each is captured correctly.
   -  **Single-Item Responses**: Some responses of this type may only
      contain a single “item”. We don’t (yet) have intelligent behavior
      for this scenario, so instead of a list with a single element, you
      will just find a single ObjectDict at that node. The simplest way
      to work around this at the moment is to test the node with
      ``isinstance(response.parsed.OrderItems.OrderItem, list)`` and
      handle it accordingly. (*in the future, we may allow every node to
      be iterable so that this check is not necessary.*)

-  The actual output may show various ``'value'`` keys with empty string
   values, or strings containing only spaces or newline characters.
   These can be safely ignored.

Given this example, suppose you want to get the **ItemPrice** for the
first item in this order. MWS typically returns prices with two
attributes, **Amount** and **CurrencyCode**, so that you can process the
price in whatever currency you need.

So, to get these two values, we might do this:

.. code:: python

    >>> response.parsed.OrderItems.OrderItem[0].ItemPrice.Amount
    '25.99'
    >>> response.parsed.OrderItems.OrderItem[0].ItemPrice.CurrencyCode
    'JPY'

Note that all data is returned as a string. To parse this, you may want
to pass **ItemPrice.Amount** through ``float``,
`decimal.Decimal <https://docs.python.org/3.5/library/decimal.html>`__,
or
`fractions.Fraction <https://docs.python.org/3.5/library/fractions.html>`__,
as you see fit.

Also note how long these calls can be. A good practice is to work on
parts of the response at a time by assigning them to a new variable or
passing them to your own parsing method, depending on your needs:

.. code:: python

    >>> items = response.parsed.OrderItems.OrderItem
    >>> item = items[0]
    >>> item.ItemPrice.Amount
    '25.99'
    >>> item.ItemPrice.CurrencyCode
    'JPY'

Moving Forward
==============

We cannot guarantee the output of any particular call made to MWS, or that
any given call will result in the same output each time. Use of this module will
necessarily require some trial and error, using the Python interactive shell
to make test calls to MWS and parsing the output on your own until you have
some patterns useful enough to put into a production setting.

Be warned that there is no safe testing environment for MWS requests: any valid request
has the potential to disrupt the production environment of that seller account. Please
be cautious as to which requests are being sent, scrutinize and clean your input as
best as possible, and know the potential outcomes for the requests being made.