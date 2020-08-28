.. _page_getting_started:

Getting started
###############

.. note:: We assume you have an Amazon Professional Seller account and developer access
   to be able to use MWS. If not, please see :ref:`page_prerequisites`.

Entering credentials
====================

To begin, use your MWS Credentials to instantiate one of the API classes.
We will use the ``Products`` API for this example.

Where you store these credentials is up to you, but we recommend pulling them
from environment variables:

.. code-block:: python

    import mws

    products_api = mws.Products(
        access_key=os.environ["MWS_ACCESS_KEY"],
        secret_key=os.environ["MWS_SECRET_KEY"],
        account_id=os.environ["MWS_ACCOUNT_ID"],
        auth_token=os.environ["MWS_AUTH_TOKEN"],
    )
    # auth_token is optional, depending on how you have your MWS access set up.

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

    response = products_api.list_matching_products(
        marketplace_id=mws.Marketplaces.US.marketplace_id,
        query="python",
    )
    # mws.Marketplaces is an enum we can use to fill in the `marketplace_id` value,
    # instead of needing to manually enter, i.e., "ATVPDKIKX0DER"

The request is sent automatically when ``list_matching_products`` is called, and a
``response`` is returned. MWS typically returns an XML document encoded in ISO-8859-1
(per `Amazon's standards <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_ISO8859.html>`_),
which python-amazon-mws attempts to decode automatically.

For most responses (including our example ``list_matching_products``), the ``response`` will be a
``DictWrapper`` object containing:

- ``response.original``, the original XML document;
- ``response.response``, the HTTP response code of the request (200, 400, etc.); and
- ``response.parsed``, a parsed version of the XML tree. (See :ref:`page_parsed_xml_responses`).

Certain responses (such as the `GetReport
<http://docs.developer.amazonservices.com/en_US/reports/Reports_GetReport.html>`_ operation, under
the Reports API) may return other content types, such as PDFs, tab-delimited flat files, ZIP files,
and so on. Non-XML responses will be wrapped in a ``DataWrapper`` object with similar attributes
as ``DictWrapper``, with the raw document stored in ``.original``, and ``.parsed`` simply returning
``.original`` for convenience.
