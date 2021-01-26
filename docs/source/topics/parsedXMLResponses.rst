Using Parsed XML Responses
##########################

.. versionadded:: 1.0dev15
   ``MWSResponse`` and ``DotDict`` added.

.. include:: /newFeaturesTopNote100dev15.rst

For most MWS operations, the returned response is an XML documents `encoded using ISO 8859-1
<http://docs.developer.amazonservices.com/en_US/dev_guide/DG_ISO8859.html>`_. python-amazon-mws will wrap all responses
in an instance of :py:class:`MWSResponse <mws.response.MWSResponse>`, which then parses these responses automatically
using the ``xmltodict`` package. This parsed content is then available from the
:py:attr:`MWSResponse.parsed <mws.response.MWSResponse.parsed>` property.

Below, we'll go into more detail on how to use ``MWSResponse.parsed`` in your application to get the most from
these XML responses.

How XML responses are parsed in python-amazon-mws
=================================================

XML responses from MWS typically look like the following example (adapted from an example in MWS documentation):

.. code-block:: xml

    <?xml version="1.0"?>
    <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
      <ListMatchingProductsResult>
        <Products xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01" xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
          <Product>
            <Identifiers>
              <MarketplaceASIN>
                <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
                <ASIN>059035342X</ASIN>
              </MarketplaceASIN>
            </Identifiers>
            <AttributeSets>
              <ns2:ItemAttributes xml:lang="en-US">
                <ns2:Binding>Paperback</ns2:Binding>
                <ns2:Brand>Scholastic Press</ns2:Brand>
                <ns2:Creator Role="Illustrator">GrandPrÃ©, Mary</ns2:Creator>
              </ns2:ItemAttributes>
            </AttributeSets>
            <Relationships/>
          </Product>
        </Products>
      </ListMatchingProductsResult>
      <ResponseMetadata>
        <RequestId>3b805a12-689a-4367-ba86-EXAMPLE91c0b</RequestId>
      </ResponseMetadata>
    </ListMatchingProductsResponse>

Parsing of this document goes through the following steps in python-amazon-mws:

1. All requests are sent through the ``requests`` package, and responses are returned as
   |requests_response_instance_link|_.

   The ``Response`` object is then wrapped by :py:class:`MWSResponse <mws.response.MWSResponse>`, and stored internally
   as :py:attr:`MWSResponse.original <mws.response.MWSResponse.original>`.

   .. |requests_response_instance_link| replace:: a ``requests.Response`` instance
   .. _requests_response_instance_link: https://2.python-requests.org/en/master/api/#requests.Response

2. If the response did not specify an encoding in its headers, ``MWSResponse`` will call on
   ``requests.Response.apparent_encoding`` explicitly to force character set detection.
   For most use cases, this will allow the :py:attr:`MWSResponse.text <mws.response.MWSResponse.text>` property
   to decode the response content properly.

   .. note:: if a different encoding is required, you can alter
      :py:attr:`MWSResponse.encoding <mws.response.MWSResponse.encoding>` before accessing
      ``MWSResponse.text``, or work with the raw :py:attr:`MWSResponse.content <mws.response.MWSResponse.content>`.

      You can also initialize an API class instance with a ``force_response_encoding='my-encoding'`` argument.
      This will override the encoding used to decode all responses from that API's requests. This is useful when you
      are confident that responses are being encoded differently, such as when responses are actually encoded in UTF-8
      (despite Amazon's documentation to the contrary).

3. :py:meth:`MWSResponse.parse_response() <mws.response.MWSResponse.parse_response>` is called, which:

   1. Produces a "clean" copy of the XML document to use for parsing (see :ref:`xml_cleaning_before_parsing`).
      (The original response content is left unchanged: only a copy is used for parsing.)

   2. Runs ``MWSResponse.text`` through the utility ``mws.utils.xml.mws_xml_to_dict``. This uses ``xmltodict.parse()``
      to convert the XML to a standard Python dictionary, which is returned and stored as ``MWSResponse._dict``.

   3. Wraps the parsed Python dict in a :py:class:`DotDict <mws.utils.collections.DotDict>`, which can be accessed from
      :py:attr:`MWSResponse.parsed <mws.response.MWSResponse.parsed>`.

      If the response contains a ``<ResponseMetadata>`` tag, this method also builds a ``DotDict`` instance of this
      key only, storing it as :py:attr:`MWSResponse.metadata <mws.response.MWSResponse.metadata>`. Typically this tag
      only contains the ``<RequestId>`` element, so the property
      :py:attr:`MWSResponse.request_id <mws.response.MWSResponse.request_id>` can also be used to access this value.

Once parsing is complete, the :py:class:`MWSResponse <mws.response.MWSResponse>` instance is returned. From this
instance, we can access the :py:class:`DotDict <mws.utils.collections.DotDict>` that is returned from its
:py:attr:`.parsed <mws.response.MWSResponse.parsed>` property to comb through the returned data.

For more details on how to make the best use of this parsed data, please see
:doc:`../reference/DotDict`.

Result keys and metadata
========================

Most MWS requests returning XML documents take the following overall shape:

.. code-block:: xml

    <?xml version="1.0"?>
    <OperationResponse>
      <OperationResult>
        ...
      </OperationResult>
      <ResponseMetadata>
        <RequestId>...</RequestId>
      </ResponseMetadata>
    </OperationResponse>

The parsed document initially returns a ``dict`` with just two keys. For the above example, that would look like so:

.. code-block:: python

    {
        'OperationResult': ...,
        'ResponseMetadata': ...,
    }

.. note:: ``Operation`` in all above examples would be replaced by the name of the MWS operation that was called.
   For the ``ListInboundShipments`` operation, for example, the document's root will be
   ``ListInboundShipmentsResponse``, and the result key will be ``ListInboundShipmentsResult``.

Both the ``...Result`` key and ``ResponseMetadata`` are accessible from
:py:class:`MWSResponse <mws.response.MWSResponse>` through separate properties:

- The ``...Result`` key is used as the root for :py:attr:`MWSResponse.parsed <mws.response.MWSResponse.parsed>`,
  so accessing ``.parsed`` should only return parsed content found inside the ``<...Result>`` tag.
- ``ResponseMetadata`` is accessible from :py:attr:`MWSResponse.metadata <mws.response.MWSResponse.metadata>`.
  You can access the ``RequestId`` stored there either as ``MWSResponse.metadata.RequestId`` or through the shortcut
  property, :py:attr:`MWSResponse.request_id <mws.response.MWSResponse.request_id>`.

.. tip:: `Amazon recommends <https://docs.developer.amazonservices.com/en_US/dev_guide/DG_ResponseFormat.html>`_
   logging ``RequestId`` as well as the request timestamp (found in
   :py:attr:`MWSResponse.timestamp <mws.response.MWSResponse.timestamp>`) to aid in troubleshooting when contacting
   their support channels.

.. _xml_cleaning_before_parsing:

XML "cleaning" before parsing
=============================

MWS XML responses may be returned with a variety of data that does not fit well into Python data structures
During parsing of these responses, python-amazon-mws either removes or finesses some of this data into a "cleaner"
format.

Consider the example response from earlier:

.. code-block:: xml
   :linenos:

   <?xml version="1.0"?>
   <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
     <ListMatchingProductsResult>
       <Products xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01" xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
         <Product>
           <Identifiers>
             <MarketplaceASIN>
               <MarketplaceId>ATVPDKIKX0DER</MarketplaceId>
               <ASIN>059035342X</ASIN>
             </MarketplaceASIN>
           </Identifiers>
           <AttributeSets>
             <ns2:ItemAttributes xml:lang="en-US">
               <ns2:Binding>Paperback</ns2:Binding>
               <ns2:Brand>Scholastic Press</ns2:Brand>
               <ns2:Creator Role="Illustrator">GrandPrÃ©, Mary</ns2:Creator>
             </ns2:ItemAttributes>
           </AttributeSets>
           <Relationships/>
         </Product>
       </Products>
     </ListMatchingProductsResult>
     <ResponseMetadata>
       <RequestId>3b805a12-689a-4367-ba86-EXAMPLE91c0b</RequestId>
     </ResponseMetadata>
   </ListMatchingProductsResponse>

This document will be "cleaned" as follows:

- The document's root tag - in this case ``<ListMatchingProductsResponse>`` - will be ignored. The parsed Python dict
  will take the shape of:

  .. code-block:: python

     {
         'ListMatchingProductsResult': ...,
         'ResponseMetadata': ...
     }

- `Namespaces <https://en.wikipedia.org/wiki/XML_namespace>`_ are removed. For instance, the ``<Products>`` tag
  (line 4) will have both namespaces stripped, leaving only the bare tag name.
- Prefixes - such as ``ns2:`` or ``xml:``, seen on lines 13 through 17 - are removed from tag names and attributes.
  The tag ``<ns2:ItemAttributes xml:lang="en-US">`` on line 13 will be stripped down to just
  ``<ItemAttributes lang="en-US">`` prior to being parsed.
