"""Testing for objects in ``mws.utils.collections``."""

import pytest

from mws.utils.collections import DotDict


class TestDotDictObject:
    """Test cases for the ``DotDict`` object."""

    def test_dotdict_assignment(self):
        """Tests for constructors of DotDict, attr assignment, and updating."""
        dot_dict = DotDict()

        assert bool(dot_dict) is False

        dot_dict.a = "a"
        assert dot_dict["a"] == "a"
        dot_dict["a"] = "b"
        assert dot_dict.a == "b"

        # Assignment of a standard dict should return nested DotDicts,
        # so sub-keys should be accessible with attrs
        dot_dict.b = {"c": {"d": "e"}}
        assert dot_dict.b.c.d == "e"

        # Assigning an empty dict will also convert to a DotDict
        dot_dict.c = {}
        assert isinstance(dot_dict.c, DotDict)
        # by the way, is also an instance of dict
        assert isinstance(dot_dict.c, dict)

    def test_dotdict_constructor(self):
        """The constructor for a ``DotDict`` object."""
        # Update method should work similar to the above
        dot_dict = DotDict(a=3, b=4, c={"d": "e"}, d=DotDict(a=3))
        assert dot_dict.a == 3
        assert dot_dict.b == 4
        assert isinstance(dot_dict.c, DotDict)
        assert isinstance(dot_dict.c, dict)
        assert dot_dict.c.d == "e"
        assert isinstance(dot_dict.d, DotDict)
        assert isinstance(dot_dict.d, dict)
        assert dot_dict.d.a == 3

    def test_dotdict_mapping_constructor(self):
        dot_dict = DotDict({"a": 3, "b": 4, "c": {"d": "e"}, "d": DotDict(a=3)})
        assert dot_dict.a == 3
        assert dot_dict.b == 4
        assert isinstance(dot_dict.c, DotDict)
        assert isinstance(dot_dict.c, dict)
        assert dot_dict.c.d == "e"
        assert isinstance(dot_dict.d, DotDict)
        assert isinstance(dot_dict.d, dict)
        assert dot_dict.d.a == 3

    def test_dotdict_item_deletion(self):
        """Testing of the delattr method in particular."""
        dot_dict = DotDict(a=3)
        assert dot_dict.a == 3
        del dot_dict.a
        assert "a" not in dot_dict

        dot_dict["b"] = 4
        assert dot_dict["b"] == 4
        del dot_dict["b"]
        assert "b" not in dot_dict

        with pytest.raises(KeyError):
            dot_dict.b

    def test_dotdict_repr(self):
        content = {"Content": {"Item1": "spam"}}

        dot_dict = DotDict(content)

        dot_dict_repr = repr(dot_dict)
        expected = "DotDict({'Content': DotDict({'Item1': 'spam'})})"

        assert expected == dot_dict_repr

    def test_dotdict_iteration(self):
        # Iteration of a single item:
        # fmt: off
        dot_dict1 = DotDict({
            "Products": {
                "Product": {"Name": "foo"}
            }
        })
        # fmt: on

        for product in dot_dict1.Products.Product:
            assert isinstance(product, DotDict)
            assert "Name" in product

        # The above should be an identical interface to the below,
        # in which ``Product`` is a list of DotDicts with the same
        # type of content.
        # This matches up with how ``xmltodict`` might process a response
        # that may have one or more sibling tags of the same names (``Product``).
        # fmt: off
        dot_dict2 = DotDict({
            "Products": {
                "Product": [
                    {"Name": "bar"},
                    {"Name": "baz"}
                ]
            }
        })
        # fmt: on

        for product in dot_dict2.Products.Product:
            assert isinstance(product, DotDict)
            assert "Name" in product

    def test_dotdict_update(self):
        """``DotDict.update`` method."""
        dot_dict = DotDict()
        dot_dict.update(a=3, b=4, c={"d": "e"}, d=DotDict(a=3))
        assert dot_dict.a == 3
        assert dot_dict.b == 4
        assert isinstance(dot_dict.c, DotDict)
        assert isinstance(dot_dict.c, dict)
        assert dot_dict.c.d == "e"
        assert isinstance(dot_dict.d, DotDict)
        assert isinstance(dot_dict.d, dict)
        assert dot_dict.d.a == 3

    def test_dotdict_update_plain_dict(self):
        """``DotDict.update`` method."""
        dot_dict = DotDict()
        dot_dict.update({"a": 3, "b": 4, "c": {"d": "e"}, "d": DotDict(a=3)})
        assert dot_dict.a == 3
        assert dot_dict.b == 4
        assert isinstance(dot_dict.c, DotDict)
        assert isinstance(dot_dict.c, dict)
        assert dot_dict.c.d == "e"
        assert isinstance(dot_dict.d, DotDict)
        assert isinstance(dot_dict.d, dict)
        assert dot_dict.d.a == 3

    def test_dotdict_update_mixed(self):
        """``DotDict.update`` method."""
        dot_dict = DotDict()
        dot_dict.update({"a": 3, "b": 4}, c={"d": "e"}, d=DotDict(a=3))
        assert dot_dict.a == 3
        assert dot_dict.b == 4
        assert isinstance(dot_dict.c, DotDict)
        assert isinstance(dot_dict.c, dict)
        assert dot_dict.c.d == "e"
        assert isinstance(dot_dict.d, DotDict)
        assert isinstance(dot_dict.d, dict)
        assert dot_dict.d.a == 3

    def test_dotdict_attr_key_access_methods(self):
        """Various methods for accessing contents of a parsed XML response
        should all return the same way.

        - dotted attribute access
        - using dict keys
        - using `DotDict.get` (an overwrite of `dict.get`)
        - `values` containing just newlines and spaces ('\n    ') should be stripped
        and not exist at all.
        """

        content = {
            "Content": {
                "Item1": "spam",
                "Item2": {"Details": "ham", "Inner": {"Something": "eggs"}},
            }
        }

        dot_dict = DotDict(content)

        # The `in` operator should work.
        assert "Content" in dot_dict
        # Access to the attr should be the same as access to the key
        assert dot_dict.Content is dot_dict.get("Content")
        assert dot_dict.Content is dot_dict["Content"]

        # The type of a child mapping should also be DotDict
        assert isinstance(dot_dict.Content.Item2, DotDict)

        # `.keys` should work similar to a standard dict
        assert isinstance(dot_dict.Content.keys(), type(dict().keys()))

        # as should `.values()`
        assert isinstance(dot_dict.Content.values(), type(dict().values()))

        # Contents of `.items()` should work similar to a standard dict
        for key, val in dot_dict.Content.items():
            assert dot_dict.Content[key] == getattr(dot_dict.Content, key)
            assert val == dot_dict.Content[key]
            # Values should be returned as the same type as accessing them from the dict
            assert isinstance(val, type(dot_dict.Content[key]))
            assert isinstance(val, type(getattr(dot_dict.Content, key)))

        # Accessing deeper contents should work just the same
        assert dot_dict.Content.Item1 == "spam"
        assert dot_dict.Content.get("Item1") == "spam"
        assert dot_dict.Content["Item1"] == "spam"

        # .get with a default should work the same as with a dict
        assert dot_dict.Content.Item2.get("NotHere") is None
        assert dot_dict.Content.Item2.get("NotHere", "what") == "what"

        # looking for an attr not existing will pass to getitem, so will raise KeyError
        with pytest.raises(KeyError):
            dot_dict.Content.Item2.NotHere

    def test_dotdict_attr_fallback_keys(self):
        """Checks our special case fallback methods for accessing keys in DotDict.

        ``xmltodict`` converts tag attributes to a key starting with ``@``.
        Further, tags with attributes and no child tags present their text content
        as a new key, ``#text``.

        These types of keys cannot be accessed directly as attrs due to Python syntax,
        so we provide a fallback that tries to access those key names without
        ``@`` or ``#`` included.
        """
        content = {
            "Something": {
                "@Attr1": "spam",
                "ChildTag": {"@Attr2": "ham", "#text": "eggs"},
                "Conflicting": "foo",
                "@Conflicting": "bar",
                "#Conflicting": "baz",
            }
        }

        dot_dict = DotDict(content)

        # The special key ``@Attr1`` should be accessible as an attribute without ``@``
        assert dot_dict.Something.Attr1 == "spam"
        assert dot_dict.Something["@Attr1"] == "spam"
        assert dot_dict.Something.get("@Attr1") == "spam"

        # Same for the child node's attr.
        assert dot_dict.Something.ChildTag.Attr2 == "ham"
        assert dot_dict.Something.ChildTag["@Attr2"] == "ham"
        assert dot_dict.Something.ChildTag.get("@Attr2") == "ham"

        # and for the child node's text content.
        assert dot_dict.Something.ChildTag.text == "eggs"
        assert dot_dict.Something.ChildTag["#text"] == "eggs"
        assert dot_dict.Something.ChildTag.get("#text") == "eggs"

        # In the case of a conflict, a key with no '@' or '#' takes precedence
        assert dot_dict.Something.Conflicting == "foo"
        assert dot_dict.Something["@Conflicting"] == "bar"
        assert dot_dict.Something["#Conflicting"] == "baz"

        # As expected without this fallback, a missing key raises KeyError
        with pytest.raises(KeyError):
            dot_dict.Something.NonExistent
