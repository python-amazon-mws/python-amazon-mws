.. _page_parsed_attr:

Using Parsed XML Responses
##########################

Most responses to MWS requests take the form of XML documents `encoded using ISO 8859-1
<http://docs.developer.amazonservices.com/en_US/dev_guide/DG_ISO8859.html>`_. You can access the raw XML document
directly using the property ``response.original``.

Python-Amazon-MWS also performs some XML parsing automatically, turning the document tree into nested Python objects
that resemble dictionaries. This parsed version can be accessed from the response object, using ``response.parsed``.

Below, we'll go into more detail on how to use ``response.parsed`` in your application to get the most from MWS.

Dict Keys as Dotted Attrs
=========================

``response.parsed`` returns an instance of ``mws.utils.parsers.DotDict``, a dict-like object with some
added features. Each node in the XML tree is automatically converted into one of these ``DotDict``, so child nodes
share the same features.

Most notably, keys in a ``DotDict`` can be accessed like dotted attrs on a class object, in addition to accessing
like dict keys:

.. code-block:: python

    # The following are all equivalent:
    response.parsed['foo']['bar']['baz']
    response.parsed.foo.bar.baz
    response.parsed.foo.bar.get('baz')

    # And any combination therein:
    response.parsed.get('foo').bar['baz']

.. tip:: Using dotted attrs is highly recommended to make your code more concise, with the exception of cases where
   ``.get(key, default)`` may be useful (nodes that may be missing, providing defaults, etc.).

General parsing rules
=====================

The following general rules are followed for this parsing method:

- For convenience, ``response.parsed`` will start from the ``{operation}Result`` node of the XML document,
  where ``{operation}`` is the name of the MWS operation used to make the request. This makes it a little
  easier to get to the heart of the response content.

  For example, when requesting the **ListMatchingProducts** operation (in the **Products** API),
  the response XML will look something like:

  .. code-block:: xml

      <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <ListMatchingProductsResult>
          <Product>foo</Product>
        </ListMatchingProductsResult>
      </ListMatchingProductsResponse>

  After the response is processed, ``.parsed`` will be set with ``<ListMatchingProductsResult>`` as its root.
  To access the contents of the ``<Product>`` tag beneath it, use ``response.parsed.Product`` (returning ``"foo"``).

  - If no root node is provided - such as when working with the ``DictWrapper`` utility class directly and providing
    raw XML content) - ``.parsed`` will default to the document root node. In the above example, this
    would be ``<ListMatchingProductsResponse>``; and you would access the ``<Product>`` tag using
    ``response.parsed.ListMatchingProductsResult.Product``.

- Tags that contain a value with no tag attributes and no child tags will return that value directly when accessed:

  .. code-block:: python

      response = example_api.example_request()

      # with XML response of:
      # <Response>
      #   <SomeTag>foo</SomeTag>
      # </Response>

      print(response.parsed.SomeTag)
      # 'foo'

- Tags that contain at least one attribute will return a dict-like object containing that value and all attributes.
  The value of the tag can be accessed by a ``value`` key.

  .. code-block:: python

      # with XML response of:
      # <Response>
      #   <SomeTag Name="bar">foo</SomeTag>
      # </Response>

      print(response.parsed.SomeTag)
      # {'value': 'foo', 'Name': {'value': 'bar'}}

  .. note:: The parsed ``Name`` attribute in the example also returns a dict-like object with a single key, ``value``.
      Internally, all leaf nodes

  - ``xmlns`` namespace attributes are stripped ahead of time, and will not appear in parsed output.

- Sibling nodes with the same name will be grouped into a list accessible by that sibling tag's name.

  For example, the ``<Item>`` tags below are siblings, under the ``SomeItems`` parent tag:

  .. code-block:: xml

      <SomeItems>
        <Item>
          <Name>foo</Name>
        </Item>
        <Item>
          <Name>bar</Name>
        </Item>
      </SomeItems>

  These will be collected into a list under ``.parsed.SomeItems.Item``. You can access the child
  items of these nodes either by list index:

  .. code-block:: python

      print(response.parsed.SomeItems.Item[0].Name)
      # foo

      print(response.parsed.SomeItems.Item[1].Name)
      # bar

  ...or by iterating on the node itself:

  .. code-block:: python

      for item in response.parsed.SomeItems.Item:
          print(item.Name)

      # foo
      # bar

- The parser does not know ahead of time that a given node *may* contain a list of siblings.
  From the previous example, if only a single ``<Item>`` is returned, then
  ``response.parsed.SomeItems.Item`` will **not** be a list, and using list indices may result
  in an ``IndexError``.

  Fortunately, all nodes are iterable by default. If you expect a list of items, you may safely
  iterate on the node to access its contents, even if only one item is returned:

  .. code-block:: python

      # for the response:
      # <SomeItems>
      #   <Item>
      #     <Name>foo</Name>
      #   </Item>
      # </SomeItems>

      for items in response.parsed.SomeItems.Item:
          print(item.Name)

      # foo

- Self-terminated tags, i.e. ``<NothingIsHere/>``, can still be accessed, but will return an empty
  ``DotDict``, similar to an empty dict. Also similar to a dict, they will evaluate as ``False``
  when used as a conditional, so that you know to ignore them.

  .. warning:: Iterating on these "empty" nodes will produce one iteration, returning the single empty
     ``DotDict`` itself:

     .. code-block:: python

        for item in response.parsed.NothingIsHere:
            print(item)
            print(type(item))

        # {}
        # <class 'mws.utils.collections.DotDict'>

     A future dev version of the project will attempt to remove this inconsistency.

Example parsed response
=======================

Below is an example response from the Products API operation `ListMatchingProducts
<http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html>`_,
as provided in MWS documentation and modified for length:

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

``response.parsed`` will always start from the ``<operation>Result`` node as its "root":
in this case, ``ListMatchingProductsResult``.

To access, for instance, the ASINs of all Products returned by this request, we might
do the following:

.. code-block:: python

    products = response.parsed.Products.Product
    # Don't be afraid to re-assign sub-nodes for readability!

    asins = []
    for product in products:
        # Each `product` here begins from a `<Product>` tag in the XML
        this_asin = product.Identifiers.MarketplaceASIN.ASIN
        asins.append(this_asin)

    print(asins)
    # ['059035342X']

Going further, let's process some of the ``ItemAttributes`` available:

.. code-block:: python

    products = response.parsed.Products.Product
    for product in products:
        attributes = product.AttributeSets.ItemAttributes
        # This accesses the XML tag `<ns2:ItemAttributes>`
        # Note the `ns2:` prefix is stripped from this and all sub-nodes.

        creator_tag = attributes.Creator
        # `<ns2:Creator>` contains a "Role" attribute as well as a value.
        # Thus, the return value of `.Creator` is another `DotDict` containing both.

        role = creator_tag.Role
        # We access `Role` as though it were another child node.

        creator = creator_tag.value
        # The tag contents are stored in `.value`.

        print(role)
        # Illustrator

        print(creator)
        # GrandPrÃ©, Mary
