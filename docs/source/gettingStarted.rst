Getting started
###############

.. note:: We assume you have an Amazon Professional Seller account and developer access
   to be able to use MWS. If not, please see :doc:`prerequisites`.

Entering credentials
====================

To begin, use your MWS Credentials to instantiate one of the API classes.
We will use the ``Products`` API for this example.

Where you store these credentials is up to you, but we recommend using environment variables, like so:

.. code-block:: python

    import os
    from mws import Products

    products_api = Products(
        access_key=os.environ["MWS_ACCESS_KEY"],
        secret_key=os.environ["MWS_SECRET_KEY"],
        account_id=os.environ["MWS_ACCOUNT_ID"],
        auth_token=os.environ["MWS_AUTH_TOKEN"],
    )
    # `auth_token` is optional, depending on how you your MWS access is set up.

Making requests
===============

Each API class contains a number of **request methods**, which closely match the
Operations available to that API section in MWS. You should refer to MWS documentation
for the API class you intend to use and provide the data specified by that operation.

For our example, we will use the `Products API
<http://docs.developer.amazonservices.com/en_US/products/Products_Overview.html>`_
operation `ListMatchingProducts
<http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html>`_.
In python-amazon-mws, this is done using an instance of the ``Products`` API class and its method
``list_matching_products``:

.. code-block:: python

    from mws import Marketplaces

    # Marketplaces is an enum we can use to fill in the `marketplace_id` value,
    # instead of needing to manually enter, i.e., "ATVPDKIKX0DER"
    my_marketplace = Marketplaces.US.marketplace_id

    response = products_api.list_matching_products(
        marketplace_id=my_marketplace,
        query="python",
    )

The request is sent automatically when ``list_matching_products`` is called, and a
``response`` is returned. MWS typically returns an XML document encoded in ISO-8859-1
(per `Amazon's standards <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_ISO8859.html>`_),
which python-amazon-mws attempts to decode automatically.

For most responses (including our example ``list_matching_products``), the ``response`` will be a
``DictWrapper`` object containing:

- ``response.original``, the original XML document;
- ``response.response``, the HTTP response code of the request (200, 400, etc.); and
- ``response.parsed``, a parsed version of the XML tree. (See :doc:`topics/parsedXMLResponses`).

Certain responses (such as the `GetReport
<http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReport.html>`_ operation, under
the Reports API) may return other content types, such as PDFs, tab-delimited flat files, ZIP files,
and so on. Non-XML responses will be wrapped in a ``DataWrapper`` object with similar attributes
as ``DictWrapper``, with the raw document stored in ``.original``, and ``.parsed`` simply returning
``.original`` for convenience.

.. warning::
   .. versionadded:: 1.0dev15

   ``DictWrapper`` and ``DataWrapper`` are deprecated, and will be removed in v1.1. During development testing,
   these objects will still be returned from requests by default, and parsed content will still use ``ObjectDict``
   instances (also deprecated).

   To use newer features, such as the :py:class:`MWSResponse <mws.response.MWSResponse>` wrapper and
   parsed XML using :py:class:`DotDict <mws.utils.collections.DotDict>`, set flag ``_use_feature_mwsresponse`` to
   ``True`` on an API class instance *before* making any requests:

   .. code-block:: python

      # instantiate your class
      products_api = Products(...)

      # set the new feature flag
      products_api._use_feature_mwsresponse = True

      # run your requests as normal
      response = products_api.list_matching_products(...)

   For details on using these newer features, please see:

   - :doc:`topics/parsedXMLResponses`
   - :doc:`reference/MWSResponse`
   - :doc:`reference/DotDict`

   ``MWSResponse`` *and* ``DotDict`` *will become the default objects returned by requests in v1.0*.
