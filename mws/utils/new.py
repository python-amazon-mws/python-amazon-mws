import re
from xml.parsers.expat import ExpatError
import pprint
from collections.abc import Mapping, MutableSequence

import chardet
import xmltodict

# from mws.utils import DotDict


class MWSResponse(object):
    """Wraps a requests.Response object and extracts some known data points.

    Particularly for XML responses, parsed contents can be found in the `.parsed`
    property as DotDicts; and metadata in `.meta` (mainly for `.meta.RequestId`).

    Also gives quick access to `.headers`, the `.original` response object,
    and the raw `.textdata` from the response.
    """

    def __init__(self, response, rootkey=None, force_cdata=False):
        # Fallback, raw and meta attributes for xml and textfiles
        # requests.request response object, link above
        self.original = response
        self.headers = self.original.headers

        # Recommended attributes only for xml
        self.pydict = None  # alternative to xml parsed or dot_dict
        self.dot_dict = None  # fallback for xml parsed
        self._meta = None

        # Recommended attribute only for textdata
        self.textdata = None

        # parsing
        self._rootkey = rootkey
        self._force_cdata = force_cdata
        self._parse_content()

    def _parse_content(self):
        """Attempt to process and parse the response content."""
        # a better guess for the correct encoding
        self.original.encoding = self.guess_encoding()
        textdata = self.original.text
        try:
            # try to parse as xml
            self._xml2dict(textdata)
        except ExpatError:
            # if it's not xml its a plain textfile, like a csv
            self.textdata = textdata

    def guess_encoding(self):
        """Returns the possible encoding for the response using chardet."""
        # fix for one none ascii character
        chardet.utf8prober.UTF8Prober.ONE_CHAR_PROB = 0.26
        bytelist = self.original.content.splitlines()
        detector = chardet.UniversalDetector()
        for line in bytelist:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result["encoding"]

    def _xml2dict(self, rawdata):
        """Convert XML response content to a Python dictionary using `xmltodict`."""
        namespaces = self._extract_namespaces(rawdata)
        self._mydict = xmltodict.parse(
            rawdata,
            dict_constructor=dict,
            process_namespaces=True,
            namespaces=namespaces,
            force_cdata=self._force_cdata,
        )
        # unpack if possible, important for accessing the rootkey
        self.pydict = self._mydict.get(list(self._mydict.keys())[0], self._mydict)
        self.dot_dict = DotDict(self.pydict)
        if "ResponseMetaData" in self.pydict:
            # Create a DotDict for the meta data on `self.meta`
            self._meta = DotDict(self.pydict["ResponseMetaData"])

    def _extract_namespaces(self, rawdata):
        """Return namespaces found in the XML data."""
        pattern = re.compile(r'xmlns[:ns2]*="\S+"')
        raw_namespaces = pattern.findall(rawdata)
        return {x.split('"')[1]: None for x in raw_namespaces}

    @property
    def parsed(self):
        """Return a parsed version of the response.
        For XML documents, returns a nested DotDict of the parsed XML content,
        starting from `_rootkey`.
        """
        if self.dot_dict is not None:
            if self._rootkey == "ignore":
                # With a special "ignore" flag, return the dot_dict
                # without attempting to use _rootkey
                return self.dot_dict
            return self.dot_dict.get(self._rootkey, None)
        # If no parsed content exists, return the raw textdata, instead.
        return self.textdata

    @property
    def meta(self):
        """Returns a metadata DotDict from the response content.

        Typically the only key of note here is `reponse.meta.RequestId`.
        """
        return self._meta


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
        self.__data = mapping

    def __getattr__(self, name):
        """Simply returns an attr if the object has one by that name.

        If not, assumes `name` is a key of the underlying dict data,
        passing the call to `__getitem__`.
        """
        if hasattr(self.__data, name):
            # Use an attribute present on the original
            return getattr(self.__data, name)

        # it's not an attribute, so use it as a key for the data
        return self.__getitem__(name)

    def __getitem__(self, key):
        """Return a child item as another DotDict instance."""
        return self.__class__.build(self.__data[key])

    def __repr__(self):
        return "{}({})".format(
            self.__class__.__name__, self.__dict__["_DotDict__data"],
        )

    def __str__(self):
        """Print contents using pprint."""
        return pprint.pformat(self.__dict__["_DotDict__data"])

    def __iter__(self):
        """Nodes are iterable be default, even with just one child node.

        Returns non-list nodes wrapped in an iterator, so they can be iterated
        and return the child node.
        """
        # If the parser finds multiple sibling nodes by the same name
        # (under the same parent node), that node will return a list of DotDicts.
        # However, if the same node is returned with only one child in other responses,
        # downstream code may expect the list, but iterating the single node will
        # throw an error.
        # So, when iteration is required, we return single nodes as an iterator
        # wrapping that single instance.
        if not isinstance(self, MutableSequence):
            return iter([self])
        return self

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
        if isinstance(obj, MutableSequence):
            # Build each item in the `obj` sequence, and return a list containing them.
            return [cls.build(item) for item in obj]
        # In all other cases, return `obj` unchanged.
        return obj
