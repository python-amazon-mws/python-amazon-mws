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
   confused with |requests_response_link|_.

   However, ``MWSResponse`` wraps a ``requests.Response`` instance and provides access to its contents through several
   shortcut properties, such as ``headers``, ``status_code``, etc. That original ``requests.Response`` instance
   can be found as either ``MWSResponse.response`` or ``MWSResponse.original``, and you can further access content of
   the original response using, for instance, ``MWSResponse.original.content`` or ``MWSResponse.original.text``.

   ``MWSResponse`` also provides shortcut methods to the same, i.e. ``MWSResponse.headers``,
   ``MWSResponse.status_code``, ``MWSResponse.context``, and ``MWSResponse.text``.

   **So**, if you wish to process the raw XML document yourself, you can work with any of the above methods to
   get to the original response's ``.content`` (for bytes) or ``.text`` (for Unicode).

.. |requests_response_link| replace:: an instance of ``requests.Response`` from the ``requests`` package
.. _requests_response_link: https://2.python-requests.org/en/master/user/advanced/#request-and-response-objects

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

Sibling XML tags with the same tag name represent sequences of similar objects. When parsed to a Python dict,
they are collected into a list of dicts accessible from a key by the same name as the sibling tags.

For the following (simplified) XML document:

.. code-block:: xml

    <Response>
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

Each ``<Product>`` tag's child nodes are parsed into a separate dict, and all dicts are joined in a list,
which you will find at ``response.parsed.Products.Product``. Typically, you will want to access these ``Product``
objects by iterating the ``Product`` node:

.. code-block:: python

    names = []
    for product in response.parsed.Products.Product:
        names.append(product.Name)

    print(names)
    # ['spam', 'ham', 'eggs']

If the same request returns only one ``<Product>`` tag, the ``Product`` key in the parsed response will return only
a single ``DotDict``, similar to any other node in the XML tree. Trying to access the ``Product`` node in this case
as though it were a list - such as using indices (``.Product[0]``) - will result in errors.

However, when a ``DotDict`` is iterated, it will wrap itself in a list in order to provide the same interface as before.

So, for an XML response like so:

.. code-block:: xml

    <Response>
      <Products>
        <Product>
          <Name>foo</Name>
        </Product>
      </Products>
    </Response>

...the same Python code can be used to access "all" ``Product`` keys:

.. code-block:: python

    names = []
    for product in response.parsed.Products.Product:
        names.append(product.Name)

    print(names)
    # ['foo']

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

``DotDict`` also allows accessing these keys using a fallback method. Simply provide the key name without
``@`` or ``#`` in front, and it will attempt to find a matching key:

.. code-block:: python

    print(dotdict.Products.Product.Name)
    # 'spam'

    print(dotdict.Products.Product.WhatHaveYou.text)
    # 'eggs'

.. note:: In case of a conflicting key name, a key matching the attribute will be returned first:

   .. code-block:: python

       dotdict = DotDict({'foo': 'spam', '@foo': 'ham'})
       print(dotdict.foo)
       # 'spam'
       print(dotdict['@foo'])
       # 'ham'

   This conflict is a rare occurrence for most XML documents, however, as they are not likely to return a tag attribute
   with the same name as an immediate child tag.

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
