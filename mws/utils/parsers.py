"""Utilities for parsing content from MWS responses.

XML to Dict code Borrowed from https://github.com/timotheus/ebaysdk-python
"""

from io import BytesIO
from zipfile import ZipFile
import re
import xml.etree.ElementTree as ET

from mws.errors import MWSError
from mws.utils.crypto import calc_md5


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


def remove_xml_namespace(xml):
    """Strips the namespace from XML document contained in a string.
    Returns the stripped string.
    """
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub("", xml)


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


# DEPRECATION: these are old names for these objects, which have been updated
# to more idiomatic naming convention. Leaving these names in place in case
# anyone is using the old object names.
# TODO: remove in 1.0.0
object_dict = ObjectDict
xml2dict = XML2Dict


class DictWrapper(object):
    """Converts XML data to a parsed response object as a tree of `ObjectDict`s.

    Use `.parsed` for direct access to those contents, and `.original` for
    the original XML document string.
    """

    # TODO create a base class for DictWrapper and DataWrapper with all the keys we expect in responses.
    # This will make it easier to use either class in place of each other.
    # Either this, or pile everything into DataWrapper and make it able to handle all cases.

    def __init__(self, xml, rootkey=None):
        if isinstance(xml, bytes):
            try:
                xml = xml.decode(encoding="iso-8859-1")
            except UnicodeDecodeError as exc:
                # In the very rare occurence of a decode error, attach the original xml to the .response of the MWSError
                error = MWSError(str(exc.response.text))
                error.response = xml
                raise error

        self.response = None
        self._rootkey = rootkey
        self._mydict = XML2Dict().fromstring(remove_xml_namespace(xml))
        self._response_dict = self._mydict.get(
            list(self._mydict.keys())[0], self._mydict
        )

    @property
    def parsed(self):
        """Returns parsed XML contents as a tree of `ObjectDict`s."""
        if self._rootkey:
            return self._response_dict.get(self._rootkey, self._response_dict)
        return self._response_dict


class DataWrapper(object):
    """Text wrapper in charge of validating the hash sent by Amazon."""

    def __init__(self, data, headers):
        self.original = data
        self.response = None
        self.headers = headers
        if "content-md5" in self.headers:
            hash_ = calc_md5(self.original)
            if self.headers["content-md5"].encode() != hash_:
                raise MWSError("Wrong Content length, maybe amazon error...")

    @property
    def parsed(self):
        """Returns original content.

        Used to provide an identical interface as `DictWrapper`, even if
        content could not be parsed as XML.
        """
        return self.original

    @property
    def unzipped(self):
        """Returns a `ZipFile` of file contents if response contains zip file bytes.

        Otherwise, returns None.
        """
        if self.headers["content-type"] == "application/zip":
            try:
                with ZipFile(BytesIO(self.original)) as unzipped_fileobj:
                    # unzipped the zip file contents
                    unzipped_fileobj.extractall()
                    # return original zip file object to the user
                    return unzipped_fileobj
            except Exception as exc:
                raise MWSError(str(exc))
        return None  # 'The response is not a zipped file.'
