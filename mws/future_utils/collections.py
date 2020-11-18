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

    def __init__(self, *args, **kwargs):
        dict.__init__(self)
        self.update(*args, **kwargs)

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
        """Nodes are natively iterable, returning an iterator wrapping this instance.

        This is slightly different from standard behavior: iterating a ``dict`` will
        return its keys. Instead, we assume that the user is iterating an XML node
        which they expect sometimes returns a list of nodes, and other times returns
        a single instance of ``DotDict``. If the latter is true, we end up here.

        So, we wrap this instance in an iterator, so that iterating on it will return
        the ``DotDict`` itself, rather than its keys.
        """
        return iter([self])

    def update(self, *args, **kwargs):
        """Recursively builds values in any nested objects, such that any mapping
        object in the nested structure is converted to a ``DotDict``.

        - Each nested mapping object will be converted to ``DotDict``.
        - Each non-string, non-dict iterable will have elements built, as well.
        - All other objects in the data are left unchanged.
        """
        for key, val in dict(*args, **kwargs).items():
            self[key] = self.__class__.build(val)

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
