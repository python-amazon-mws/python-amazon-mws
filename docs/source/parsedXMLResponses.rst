.. _page_parsed_attr:

Parsed XML Responses
####################

Most responses from MWS take the form of ISO-8859-1 encoded XML documents. Python-Amazon-MWS
wraps these responses in a ``DictWrapper`` object for convenient access to its meta attributes.

Of particular interest is the ``.parsed`` property, which provides access to nodes in the
XML tree using either dict keys - ``reponse.parsed["key1"]["key2"]`` - or dotted attrs
- ``response.parsed.key1.key2``.

.. tip:: Accessing contents of the parsed XML using dotted attrs is highly recommended,
   and will be used throughout the following examples.

Parsing rules
=============

The following general rules are followed for this parsing method:

1. Attributes found on a tag, such as ``<TagName attr1="foo">``, will be converted to their
   own nodes:

   .. code-block:: python

      print(response.parsed.TagName.attr1)
      # foo

   - ``xmlns`` namespace attributes are stripped ahead of time, and will not appear in parsed output.

2. Sibling nodes with the same name will be grouped into a list accessible by that sibling tag's name.

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

3. The parser does not know ahead of time that a given node *may* contain a list of siblings.
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

4. Self-terminated tags, i.e. ``<NothingIsHere/>``, can still be accessed, but will return an empty
   ``ObjectDict``, similar to an empty dict. Also similar to a dict, they will evaluate as ``False``
   when used as a conditional, so that you know to ignore them.

   .. warning:: Iterating on these "empty" nodes will produce one iteration, returing the single empty
      ``ObjectDict`` itself:

      .. code-block:: python

          for item in response.parsed.NothingIsHere:
              print(item)
              print(type(item))

          # {}
          # <class 'mws.utils.collections.ObjectDict'>

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
        # Thus, the return value of `.Creator` is another `ObjectDict` containing both.

        role = creator_tag.Role
        # We access `Role` as though it were another child node.

        creator = creator_tag.value
        # The tag contents are stored in `.value`.

        print(role)
        # Illustrator

        print(creator)
        # GrandPrÃ©, Mary
