"""Data structure utilities."""

from collections.abc import Mapping, Iterable


def unique_list_order_preserved(seq):
    """Returns a unique list of items from the sequence
    while preserving original ordering.
    The first occurrence of an item is returned in the new sequence:
    any subsequent occurrences of the same item are ignored.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class DotDict(dict):
    """Read-only dict-like object class that wraps a mapping object."""

    def __init__(self, mapping=None, **kwargs):
        """Recursively builds values in the passed mapping
        through our build classmethod.

        - Each nested mapping object will be converted to a DotDict.
        - Each non-string, non-dict iterable will have elements built as well.
        - All other objects in the data are left unchanged.
        """
        if mapping is None:
            mapping = {}
        mapping = {key: self.__class__.build(val) for key, val in mapping.items()}
        dict.__init__(self, mapping)
        self.update(**kwargs)

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, super().__repr__())

    def __getattr__(self, name):
        """Simply attempts to grab a key `name`.

        Has some fallback logic for keys starting with '@' and '#',
        which are output by xmltodict when a tag has attributes included.

        In that case, will attempt to find a key starting with '@' or '#',
        or will raise the original KeyError exception.
        """
        try:
            return self[name]
        except KeyError:
            # No key by that name? Let's try being helpful.
            if "@{}".format(name) in self:
                # Does this same name occur starting with ``@``?
                return self["@{}".format(name)]
            if "#{}".format(name) in self:
                # Does this same name occur starting with ``#``?
                return self["#{}".format(name)]
            # Otherwise, raise the original exception
            raise

    def __setattr__(self, name, val):
        """Allows assigning new values to a DotDict, which will automatically build
        nested mapping objects into DotDicts, as well.

        Passes responsibility to ``__setitem__`` for consistency.
        """
        self.__setitem__(name, val)

    def __delattr__(self, name):
        """Passes attr deletion to __delitem__."""
        self.__delitem__(name)

    def __setitem__(self, key, val):
        """Allows assigning new values to a DotDict, which will automatically build
        nested mapping objects into DotDicts, as well.
        """
        val = self.__class__.build(val)
        dict.__setitem__(self, key, val)

    def __iter__(self):
        """Nodes must be iterable by default.

        This is slightly different from standard behavior, where iterating a ``dict``
        will return its keys. Here, instead, we assume that the user is iterating
        a node which may either contain a single subnode or a list of subnodes.

        Example:

        .. code-block:: python

            # For an xml response of:
            # <Products>
            #   <Product>
            #     <Name>foo</Name>
            #   </Product>
            # </Products>

            # The parsed DotDict will look like so:
            xml_example1 = DotDict({
                "Products": {
                    "Product": {"Name": "foo"}
                }
            })

            for product in xml_example1.Products.Product:
                print(product.Name)
            # foo

        Here, ``product`` returns the child DotDict ``{'Name': 'foo'}``,
        so ``product`` can be used to access child elements within the loop.

        This mirrors how a similar response with multiple ``Product`` sibling tags
        will return a list in the resulting ``DotDict`` instance:

        .. code-block:: python

            # For another response returning two Products:
            # <Products>
            #   <Product>
            #     <Name>bar</Name>
            #   </Product>
            #   <Product>
            #     <Name>baz</Name>
            #   </Product>
            # </Products>

            # will parse as:
            xml_example2 = DotDict({
                "Products": {
                    "Product": [
                        {"Name": "bar"},
                        {"Name": "baz"}
                    ]
                }
            })

            for product in xml_example2.Products.Product:
                print(product.Name)
            # bar
            # baz

        With this simple adjustment, both examples can be accessed by the same code,
        with no need to test if the node is an iterable first.
        """
        return iter([self])

    def update(self, **kwargs):
        """Build each value of our kwargs when doing an update."""
        built = {key: self.__class__.build(val) for key, val in kwargs.items()}
        dict.update(self, **built)

    @classmethod
    def build(cls, obj):
        """Builds objects to work as recursive versions of this object.

        - Mappings are converted to a DotDict object.
        - For iterables, each element in the sequence is run through the build method recursively.
        - All other objects are returned unchanged.
        """
        if isinstance(obj, Mapping):
            # Return a new DotDict object wrapping `obj`.
            return cls(obj)
        if not isinstance(obj, str) and isinstance(obj, Iterable):
            # Build each item in the `obj` sequence,
            # then construct a new sequence matching `obj`'s type.
            # Must be careful not to pass strings here, even though they are iterable!
            return obj.__class__(cls.build(x) for x in obj)
        # In all other cases, return `obj` unchanged.
        return obj
