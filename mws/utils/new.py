import re
from xml.parsers.expat import ExpatError
import pprint
from collections.abc import Mapping, MutableSequence

# import chardet
import xmltodict

# from mws.utils import DotDict
MWS_ENCODING = "iso-8859-1"
"""Amazon documents this as the encoding to expect in responses.
If it doesn't work, :shrug:, we'll have to wing it.
"""


def extract_xml_namespaces(data):
    """Return namespaces found in the XML data."""
    pattern = re.compile(r'xmlns[:ns2]*="\S+"')
    raw_namespaces = pattern.findall(data)
    return {x.split('"')[1]: None for x in raw_namespaces}


def mws_xml_to_dict(data, encoding=MWS_ENCODING, force_cdata=False, **kwargs):
    """Convert XML expected from MWS to a Python dict.
    Extracts namespaces and passes data into `xmltodict.parse`
    with some useful defaults:
        force_cdata
    """
    # Extracted namespaces
    namespaces = extract_xml_namespaces(data)
    # Run the parser
    xmldict = xmltodict.parse(
        data,
        encoding=encoding,
        process_namespaces=True,
        dict_constructor=dict,
        namespaces=namespaces,
        force_cdata=force_cdata,
    )
    # Return the results of the first key (?), otherwise the original
    finaldict = xmldict.get(list(xmldict.keys())[0], xmldict)
    return finaldict


def mws_xml_to_dotdict(data, result_key=None, force_cdata=False):
    """Convert XML expected from MWS to a DotDict object.
    first using `mws_xml_to_dict` for our default args to `xmltodict.parse`
    and then sending the res
    """
    xmldict = mws_xml_to_dict(data, force_cdata=force_cdata)
    if result_key:
        xmldict = xmldict.get(result_key, xmldict)
    return DotDict(xmldict)


class MWSResponse:
    """Wraps a requests.Response object and extracts some known data points.

    Particularly for XML responses, parsed contents can be found in the `.parsed`
    property as DotDicts; and metadata in `.metadata` (mainly for `.metadata.RequestId`).
    """

    def __init__(self, response_obj, result_key=None, force_cdata=False):
        # Fallback, raw and meta attributes for xml and textfiles
        # requests.request response object, link above
        self.original = response_obj

        # Attrs for collecting parsed XML data
        self._dict = None
        self._dotdict = None
        self._metadata = None

        # parsing
        self._result_key = result_key

        try:
            # Attempt to convert text content to an
            self._dict = mws_xml_to_dict(self.original.text, force_cdata=force_cdata)
        except ExpatError:
            # Probably not XML content: just ignore it.
            pass
        else:
            # No exception? Cool
            self._build_dotdict_data()

    ### NOTE encoding guessing was used in a prior version of this code before merge,
    ### but it's unclear if we'd ever need to guess it.
    # def guess_encoding(self):
    #     """Returns the possible encoding for the response using chardet."""
    #     # fix for one none ascii character
    #     chardet.utf8prober.UTF8Prober.ONE_CHAR_PROB = 0.26
    #     bytelist = self.original.content.splitlines()
    #     detector = chardet.UniversalDetector()
    #     for line in bytelist:
    #         detector.feed(line)
    #         if detector.done:
    #             break
    #     detector.close()
    #     return detector.result["encoding"]

    def _build_dotdict_data(self):
        """Convert XML response content to a Python dictionary using `xmltodict`."""
        self._dotdict = DotDict(self._dict)

        # Extract ResponseMetaData as a separate DotDict, if provided
        if "ResponseMetaData" in self._dict:
            self._metadata = DotDict(self._dict["ResponseMetaData"])

    @property
    def text(self):
        """Shortcut to `.original.text`."""
        return self.original.text

    @property
    def parsed(self):
        """Return a parsed version of the response.
        For XML documents, returns a nested DotDict of the parsed XML content,
        starting from `_result_key`.
        """
        if self._dotdict is not None:
            if self._result_key is None:
                # Use the full DotDict without going to a root key first
                return self._dotdict
            return self._dotdict.get(self._result_key, None)
        # If no parsed content exists, return the raw text, instead.
        return self.text

    @property
    def metadata(self):
        """Returns a metadata DotDict from the response content.
        Typically the only key of note here is `reponse.metadata.RequestId`
        (which can also be accessed from the shortcut `response.request_id`).
        """
        return self._metadata

    @property
    def request_id(self):
        """Shortcut to ResponseMetaData.RequestId if present.
        Returns None if not found.
        """
        if self.metadata is not None:
            return self.metadata.get("RequestId")
        return None


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
