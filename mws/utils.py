# -*- coding: utf-8 -*-
"""A bunch of cruddy utilities.

XML to Dict code Borrowed from https://github.com/timotheus/ebaysdk-python
"""
# TODO break utils module into a utils package,
# with separate modules for different concerns
import re
import base64
import datetime
import hashlib
import xml.etree.ElementTree as ET


class ObjectDict(dict):
    """Extension of dict to allow accessing keys as attributes.

    Example:
    >>> a = ObjectDict()
    >>> a.fish = 'fish'
    >>> a['fish']
    'fish'
    >>> a['water'] = 'water'
    >>> a.water
    'water'
    """

    def __init__(self, initd=None):
        if initd is None:
            initd = {}
        dict.__init__(self, initd)

    def __getattr__(self, item):
        node = self.__getitem__(item)

        if isinstance(node, dict) and "value" in node and len(node) == 1:
            return node["value"]
        return node

    # if value is the only key in object, you can omit it
    def __setstate__(self, item):
        return False

    def __setattr__(self, item, value):
        self.__setitem__(item, value)

    def __iter__(self):
        """A fix for instances where we expect a list, but get a single item.

        If the parser finds multiple keys by the same name under the same parent node,
        the node will create a list of ObjectDicts to that key. However, if we expect a list
        in downstream code when only a single item is returned, we will find a single ObjectDict.
        Attempting to iterate over that object will iterate through dict keys,
        which is not what we want.

        This override will send back an iterator of a list with a single element if necessary
        to allow iteration of any node with a single element. If accessing directly, we will
        still get a list or ObjectDict, as originally expected.
        """
        if not isinstance(self, list):
            return iter([self])
        return self

    def getvalue(self, item, value=None):
        """Old Python 2-compatible getter method for default value."""
        return self.get(item, {}).get("value", value)


class XML2Dict(object):
    def __init__(self):
        pass

    def _parse_node(self, node):
        node_tree = ObjectDict()
        # Save attrs and text, hope there will not be a child with same name
        if node.text:
            node_tree.value = node.text
        for key, val in node.attrib.items():
            key, val = self._namespace_split(key, ObjectDict({"value": val}))
            node_tree[key] = val
        # Save childrens
        for child in node:
            tag, tree = self._namespace_split(child.tag, self._parse_node(child))
            if tag not in node_tree:  # the first time, so store it in dict
                node_tree[tag] = tree
                continue
            old = node_tree[tag]
            if not isinstance(old, list):
                node_tree.pop(tag)
                node_tree[tag] = [old]  # multi times, so change old dict to a list
            node_tree[tag].append(tree)  # add the new one

        return node_tree

    def _namespace_split(self, tag, value):
        """Split the tag '{http://cs.sfsu.edu/csc867/myscheduler}patients'
        ns = http://cs.sfsu.edu/csc867/myscheduler
        name = patients
        """
        result = re.compile(r"\{(.*)\}(.*)").search(tag)
        if result:
            value.namespace, tag = result.groups()

        return (tag, value)

    def parse(self, filename):
        """Parse XML file to a dict."""
        file_ = open(filename, "r")
        return self.fromstring(file_.read())

    def fromstring(self, str_):
        """Convert XML-formatted string to an ObjectDict."""
        text = ET.fromstring(str_)
        root_tag, root_tree = self._namespace_split(text.tag, self._parse_node(text))
        return ObjectDict({root_tag: root_tree})


def calc_md5(string):
    """Generates base64-encoded MD5 hash of `string`."""
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b"\n")


def unique_list_order_preserved(seq):
    """Returns a unique list of items from the sequence
    while preserving original ordering.
    The first occurence of an item is returned in the new sequence:
    any subsequent occurrences of the same item are ignored.
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_utc_timestamp():
    """Returns the current UTC timestamp in ISO-8601 format."""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()


# DEPRECATION: these are old names for these objects, which have been updated
# to more idiomatic naming convention. Leaving these names in place in case
# anyone is using the old object names.
# TODO: remove in 1.0.0
object_dict = ObjectDict
xml2dict = XML2Dict
