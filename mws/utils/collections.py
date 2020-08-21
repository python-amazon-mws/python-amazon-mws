"""Data structure utilties."""

from collections.abc import Mapping, Iterable
import pprint


def unique_list_order_preserved(seq):
    """Returns a unique list of items from the sequence
    while preserving original ordering.
    The first occurence of an item is returned in the new sequence:
    any subsequent occurrences of the same item are ignored.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


class DotDict(dict):
    """Read-only dict-like object class that wraps a mapping object.

    Provides access to dict keys as dotted attrs. For example:

        dd = DotDict({'hello': 'world'})
        dd.hello
        # 'world'
        dd['hello']
        # 'world'
        dd.get('hello')
        # 'world'

    Nested mappings are converted to nested DotDicts, as well:

        dd = DotDict({'ham': {'spam': {'eggs': {'foo': 'bar'}}}})
        dd.ham.spam.eggs.foo
        # 'bar'
    """

    def __init__(self, mapping):
        self._data = mapping

    def __getattr__(self, name):
        """Simply returns an attr if the object has one by that name.

        If not, assumes `name` is a key of the underlying dict data,
        passing the call to `__getitem__`.
        """
        if hasattr(self._data, name):
            # Use an attribute present on the original
            return getattr(self._data, name)

        # it's not an attribute, so use it as a key for the data
        return self.__getitem__(name)

    def __getitem__(self, key):
        """Return a child item as another DotDict instance."""
        return self.__class__.build(self._data[key])

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__["_data"],)

    def __str__(self):
        """Print contents using pprint."""
        return pprint.pformat(self.__dict__["_data"])

    def __iter__(self):
        """Nodes must be iterable by default."""
        # If the parser finds multiple sibling nodes by the same name
        # (under the same parent node), that node will return a list of DotDicts.
        # However, if the same node is returned with only one child in other responses,
        # downstream code may expect the list, but iterating the single node will
        # throw an error.
        # So, when iteration is required, we return single nodes as an iterator
        # wrapping that single instance.
        return iter([self])

    def get(self, key, default=None):
        """Access a node like `dict.get`, including default values."""
        try:
            return self.__getitem__(key)
        except KeyError:
            return default

    @classmethod
    def build(cls, obj):
        """Converts a nested mappings and mutable sequences to DotDicts and
        lists of DotDicts, respectively.
        All other objects are returned unchanged.
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
