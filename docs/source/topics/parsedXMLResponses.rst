.. _page_parsed_attr:

Using Parsed XML Responses
##########################

For most MWS operations, the returned response is an XML documents `encoded using ISO 8859-1
<http://docs.developer.amazonservices.com/en_US/dev_guide/DG_ISO8859.html>`_. Python-Amazon-MWS will wrap all responses
in a ``mws.response.MWSResponse`` object, which then parses these responses automatically using the ``xmltodict``
package. This parsed content is then available as ``response.parsed``.

Below, we'll go into more detail on how to use ``response.parsed`` in your application to get the most from
these XML responses.

.. note:: Throughout these docs, we refer to an instance of ``MWSResponse`` as ``response``. This should not be
   confused with a ``requests.Response`` instance, which is returned from all requests sent through the ``requests``
   package.

   However, as ``MWSResponse`` wraps a ``requests.Response`` instance, it also provides direct access to its contents
   through several shortcut properties (``headers``, ``status_code``, etc.). Thus, you can work with the original XML
   document returned from the request using ``MWSResponse.content`` (bytes) and ``MWSResponse.text`` (Unicode string).

Dictionary keys as attributes
=============================

``response.parsed`` returns an instance of ``mws.utils.collections.DotDict``, a subclass of ``dict`` that allows
its keys to be accessed as attributes as well as standard ``dict`` keys:

.. code-block:: python

    from mws.utils.collections import DotDict

    foo = DotDict({'bar': {'baz': 'spam'}})
    print(foo.bar.baz)
    # 'spam'

This is useful for MWS responses and parsed XML documents in particular, which may have tags with long names
and deeply-nested structures.

Consider the following (truncated and edited) example response from the MWS operation ``ListMatchingProducts``:

.. code-block:: xml

    <?xml version="1.0"?>
    <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
      <ListMatchingProductsResult>
        <Products>
          <Product>
            <Identifiers>
              <MarketplaceASIN>
                <MarketplaceId>ACBDEFGH</MarketplaceId>
                <ASIN>B0987654</ASIN>
              </MarketplaceASIN>
            </Identifiers>
            <AttributeSets>
              ...
            </AttributeSets>
          </Product>
          <Product>
            ...
          </Product>
        </Products>
      </ListMatchingProductsResult>
    </ListMatchingProductsResponse>

When this document is parsed to a standard ``dict``, accessing the ASIN of the first Product requires code like:

.. code-block:: python

    asin = parsed_dict['Products']['Product'][0]['Identifiers']['MarketplaceASIN']['ASIN']

Using a ``DotDict``, the same content can be accessed by specifying attributes by the same names as the keys:

.. code-block:: python

    asin = response.parsed.Products.Product[0].Identifiers.MarketplaceASIN.ASIN

Of course, using keys is still possible with ``response.parsed``. Further, as the keys, attrs, and ``dict.get()``
method all return the same content, these methods can all be mixed as needed:

.. code-block:: python

    asin = response.parsed['Products'].get('Product')[0].Identifiers['MarketplaceASIN'].get('ASIN')

While these still produce lengthy code lines, we can always assign chunks of the parsed document to a new variable:

.. code-block:: python

    product = response.parsed.Products.Product[0]
    asin = product.Identifiers.MarketplaceASIN.ASIN

Using the above pattern, breaking the document down in chunks, comes in handy as we get into additional features
of the parsed response below.

Iteration by default
====================

In the previous XML example, note there are two ``<Product>`` tags that are children of ``<Products>``. This is
typical in XML documents, with multiple sibling tags of the same name indicating a sequence of similar objects.

When this document is parsed by ``xmltodict``, sibling tags are collected into a list of dicts, accessible from
a key by the same name as the sibling tag.

.. note:: To demonstrate, we can use utility function ``mws_xml_to_dict`` to convert a simple XML document to a
   standard ``dict``, or ``mws_xml_to_dotdict`` to produce a ``DotDict`` instance. In the following example,
   we will use the latter method.

   In this example, ``dotdict`` produces the same content as a full response accessed through ``response.parsed``.

.. code-block:: python

    from mws.utils.xml import mws_xml_to_dotdict

    content = """<Response>
      <Products>
        <Product>
          <Name>spam</Name>
        </Product>
        <Product>
          <Name>ham</Name>
        </Product>
        <Product>
          <Name>eggs</Name>
        </Product>
      </Products>
    </Response>
    """

    dotdict = mws_xml_to_dotdict(content)
    print(dotdict)
    # DotDict({'Products': DotDict({'Product': [DotDict({'Name': 'spam'}), DotDict({'Name': 'ham'}), DotDict({'Name': 'eggs'})]})})

    # iterate on .Product key to access the <Product> tags from the response:
    for product in dotdict.Products.Product:
        print(product.Name)

    # 'spam'
    # 'ham'
    # 'eggs'

Suppose the same request occasionally returns only one ``<Product>`` tag. The XML parser does not know that this may
sometimes be a list, so it produces a single dict entry instead of a list of dicts.

``DotDict`` will wrap itself in an iterator when needed, such that iterating on a single node provides the same
interface as iterating on a list of nodes:

.. code-block:: python

    from mws.utils.xml import mws_xml_to_dotdict

    # XML response with a single <Product> tag
    content = """<Response>
      <Products>
        <Product>
          <Name>spam</Name>
        </Product>
      </Products>
    </Response>
    """

    # This produces a single DotDict entry, instead of a list of DotDicts as before:
    dotdict = mws_xml_to_dotdict(content)
    print(dotdict)
    # DotDict({'Products': DotDict({'Product': DotDict({'Name': 'spam'})})})

    # Iterating on the .Product key still works that same way:
    for product in dotdict.Products.Product:
        print(product.Name)

    # 'spam'

.. note:: While ``DotDict`` is a subclass of ``dict``, this behavior is different from that of the standard ``dict``,
   where iterating directly on the ``dict`` object is equivalent to iterating on ``dict.keys()``. We have chosen to
   implement the above behavior to more closely match most users' intended usage when working with parsed XML,
   even though ``DotDict`` *can* be used much like a standard ``dict`` for (most) general purposes.

Working with tag attributes
===========================

XML content can contain attributes on tags, as well. These attributes are parsed as dict keys beginning
with ``@``, accessible as child nodes of the tag they appear on.

Further, tags that contain an attribute and text content will store the text on a special key, ``#text``.

Example:

.. code-block:: python

    from mws.utils.xml import mws_xml_to_dotdict

    content = """<Response>
      <Products>
        <Product Name="spam">
          <SomethingElse>ham</SomethingElse>
          <WhatHaveYou anotherAttr="foo">eggs</WhatHaveYou>
        </Product>
      </Products>
    </Response>
    """

    dotdict = mws_xml_to_dotdict(content)

    print(dotdict)
    # DotDict({'Products': DotDict({'Product': DotDict({'@Name': 'spam', 'SomethingElse': 'ham', 'WhatHaveYou': DotDict({'@anotherAttr': 'foo', '#text': 'eggs'})})})})

These ``@`` and ``#text`` keys cannot be accessed directly as attributes due to Python syntax, which reserves the
``@`` and ``#`` characters. You can still use standard dict keys to access this content:

.. code-block:: python

    print(dotdict.Products.Product['@Name'])
    # 'spam'

    print(dotdict.Products.Product.WhatHaveYou['#text'])
    # 'eggs'

``DotDict`` also allows accessing these keys using a fallback method. Simply provide the key name *without*
``@`` or ``#`` in front, and it will attempt to find the match:

.. code-block:: python

    print(dotdict.Products.Product.Name)
    # 'spam'

    print(dotdict.Products.Product.WhatHaveYou.text)
    # 'eggs'



*TODO*

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
