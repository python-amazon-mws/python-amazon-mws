DotDict
#######

.. versionadded:: 1.0dev15
   ``DotDict`` added.

.. include:: /newFeaturesTopNote100dev15.rst

The :py:class:`DotDict <mws.utils.collections.DotDict>` class is a subclass of a standard Python dict that provides
access to its keys as attributes. This object is used mainly for parsed XML content returned by
:py:attr:`MWSResponse.parsed <mws.response.MWSResponse.parsed>` and
:py:attr:`MWSResponse.metadata <mws.response.MWSResponse.metadata>`, but ``DotDict`` can also be used as a
general-purpose ``dict`` replacement (with some caveats, as shown below).

Keys as attributes
==================

While keys of a ``DotDict`` can be accessed the same as keys in a standard ``dict``, they can also be accessed
as attributes:

.. code-block:: python

    from mws.utils.collections import DotDict

    foo = DotDict({'spam': 'ham'})

    print(foo['spam'])
    # 'ham'
    print(foo.spam)
    # 'ham'
    print(foo.get('spam'))
    # 'ham'

This is useful for traversing the nested structures created by parsing XML documents, where several keys are required
in order to access a leaf node.

Consider the following (truncated and edited) example response from the MWS operation ``ListMatchingProducts``:

.. code-block:: xml
   :linenos:

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
          </Product>
        </Products>
      </ListMatchingProductsResult>
    </ListMatchingProductsResponse>

When this document is parsed, accessing the ``<ASIN>`` on line 9 using dict keys looks like the following:

.. code-block:: python

    # assuming `response` is an instance of `MWSResponse`
    asin = response.parsed['Products']['Product']['Identifiers']['MarketplaceASIN']['ASIN']

Using attribute access, the above call turns into:

.. code-block:: python

    asin = response.parsed.Products.Product.Identifiers.MarketplaceASIN.ASIN

And, of course, a mix of the different methods is possible:

.. code-block:: python

    asin = response.parsed['Products'].get('Product').Identifiers['MarketplaceASIN'].get('ASIN')

.. tip:: Accessing specific data in an MWS response will often produce lengthy code lines, as the above samples show.
   We recommend following best practices for Python programs in general, breaking up these longer lines by assigning
   chunks of data to intermediary variables:

   .. code-block:: python

      product = response.parsed.Products.Product
      asin = product.Identifiers.MarketplaceASIN.ASIN

.. _native_iteration:

Native iteration
================

XML represents sequences of similar objects by having sibling tags with the same tag name. Consider the following
toy example with three ``<Product>`` tags:

.. code-block:: xml
   :emphasize-lines: 3,6,9

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

When parsed, these are collected into a list of ``DotDict`` instances:

.. code-block:: python
   :emphasize-lines: 3-7

    DotDict({
        'Products': DotDict({
            'Product': [
                DotDict({'Name': 'spam'}),
                DotDict({'Name': 'ham'}),
                DotDict({'Name': 'eggs'}),
            ]
        })
    })

.. note:: The list of objects will always be found under the same key name as the duplicate tags, i.e. ``Product``;
   *not* under their parent key, ``Products``. This may seem counterintuitive, but the parser is simply preserving all
   tag names present in the XML document.

   Further, if a tag attribute is present on the parent ``<Products>`` tag, you would be able to access it as a
   separate key at the same level as ``Product``. This would not be possible if ``Products`` returned a list.

To gather the names of all products in this response, we can simply iterate over this list:

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

Recursive conversion of dict objects
====================================

``DotDict`` instances expect to hold nested data, as seen in the examples throughout this document. As such, any
``dict`` assigned as a value to a ``DotDict`` is automatically converted to a ``DotDict``, as well. The values
of the assigned ``dict`` are then recursively built the same way, such that every ``dict`` (or other mapping type)
instance in the structure is also converted to ``DotDict``.

This holds true in a variety of scenarios:

- Wrapping a nested ``dict`` in ``DotDict``:

  .. code-block:: python

      example1 = DotDict({'spam': {'ham': {'eggs': 'juice'}}})
      print(example1)
      # DotDict({'spam': DotDict({'ham': DotDict({'eggs': 'juice'})})})

- Using kwargs to build ``DotDict``, with a ``dict`` as one of the values:

  .. code-block:: python

      example2 = DotDict(spam={'muffin': {'cereal': 'milk'}})
      print(example2)
      DotDict({'spam': DotDict({'muffin': DotDict({'cereal': 'milk'})})})

- Assigning a ``dict`` to a key of an existing ``DotDict``, including creating new keys:

  .. code-block:: python

      example3 = DotDict()
      example3.pancakes = {'maple': 'syrup'}
      print(example3)
      # DotDict({'pancakes': DotDict({'maple': 'syrup'})})

      example3.pancakes.toast = {'strawberry': 'jam'}
      print(example3)
      # DotDict({'pancakes': DotDict({'maple': 'syrup', 'toast': DotDict({'strawberry': 'jam'})})})

- Using ``DotDict.update`` in a similar manner as ``dict.update``:

  .. code-block:: python

      example4 = DotDict()
      example4.update({'chicken': {'waffles': 'honey'}})
      print(example4)
      # DotDict({'chicken': DotDict({'waffles': 'honey'})})

      # Including a mix of a plain dict and kwargs
      example5 = DotDict()
      example5.update({'running': {'out': 'of'}}, food='examples', to={'use': 'here'})
      print(example5)
      # DotDict({'running': DotDict({'out': 'of'}), 'food': 'examples', 'to': DotDict({'use': 'here'})})

.. _tag_attributes:

Working with XML tag attributes
================================

``DotDict`` is used in python-amazon-mws primarily for parsed XML content. As such, some features of the class are
specialized for working with that content.

XML tags can contain attributes with additional data points. When parsed, these attributes are assigned to their own
dict keys starting with ``@``, differentiating them from normal tag names.

Further, tags that contain an attribute and text content will store the text on a special key, ``#text``.

For example, with the following XML document:

.. code-block:: xml
   :emphasize-lines: 3,5

    <Response>
      <Products>
        <Product Name="spam">
          <SomethingElse>ham</SomethingElse>
          <WhatHaveYou anotherAttr="foo">eggs</WhatHaveYou>
        </Product>
      </Products>
    </Response>

The parsed response would look like:

.. code-block:: python
   :emphasize-lines: 4,7,8

    DotDict({
        'Products': DotDict({
            'Product': DotDict({
                '@Name': 'spam',
                'SomethingElse': 'ham',
                'WhatHaveYou': DotDict({
                    '@anotherAttr': 'foo',
                    '#text': 'eggs'
                })
            })
        })
    })

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

DotDict API
===========

.. versionadded:: 1.0dev15
.. autoclass:: mws.utils.collections.DotDict
   :members:
