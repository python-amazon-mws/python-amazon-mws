"""Contains the MWSResponse object and related utilities."""

from xml.parsers.expat import ExpatError

from mws.utils.xml import mws_xml_to_dict, MWS_ENCODING
from mws.errors import MWSError
from mws.utils.collections import DotDict
from mws.utils.crypto import calc_md5


class ResponseWrapperBase:
    """Wraps a ``requests.Response`` object, storing the object internally
    and providing access to its public attributes as read-only properties.

    Mainly serves as a base class for ``MWSResponse``, so as to separate this code.
    """

    def __init__(self, response):
        self._response = response

    @property
    def response(self):
        """Read-only shortcut to ``._response.``"""
        return self._response

    @property
    def original(self):
        """Alias for ``.response``."""
        return self.response

    @property
    def text(self):
        """Returns the requests.Response object ``text`` attr,
        which returns unicode.
        """
        return self.response.text

    @property
    def content(self):
        """Returns the requests.Response object ``content`` attr,
        which returns bytes.
        """
        return self.response.content

    @property
    def status_code(self):
        """Returns the requests.Response object ``status_code`` attr."""
        return self.response.status_code

    @property
    def headers(self):
        """Returns the requests.Response object ``headers`` attr."""
        return self.response.headers

    @property
    def encoding(self):
        """Returns the requests.Response object ``encoding`` attr."""
        return self.response.encoding

    @property
    def reason(self):
        """Returns the requests.Response object ``reason`` attr."""
        return self.response.reason

    @property
    def cookies(self):
        """Returns the requests.Response object ``cookies`` attr."""
        return self.response.cookies

    @property
    def elapsed(self):
        """Returns the requests.Response object ``elapsed`` attr."""
        return self.response.elapsed

    @property
    def request(self):
        """Returns the requests.Response object ``request`` attr."""
        return self.response.request


class MWSResponse(ResponseWrapperBase):
    """Wraps a requests.Response object and extracts some known data.

    Particularly for XML responses, parsed contents can be found in the ``.parsed``
    property as a ``DotDict`` instance.

    Find metadata in ``.metadata``, mainly for accessing ``.metadata.RequestId``;
    or simply use the ``.request_id`` shortcut attr.
    """

    def __init__(
        self, response, request_timestamp=None, result_key=None, force_cdata=False
    ):
        super().__init__(response)
        if not self._response.encoding:
            # If the response did not specify its encoding,
            # we will assume Amazon's choice of encoding stands.
            # Otherwise, the chardet detection may end up as Windows-1252
            # or something else close, yet incorrect.
            self._response.encoding = MWS_ENCODING

        if self._response.headers and "content-md5" in self._response.headers:
            hash_ = calc_md5(self._response.content)
            if self._response.headers["content-md5"].encode() != hash_:
                raise MWSError("Wrong Content length, maybe amazon error...")

        # Attrs for collecting parsed XML data
        self._dict = None
        self._dotdict = None
        self._metadata = None

        # parsing
        self._request_timestamp = request_timestamp
        self._result_key = result_key

        try:
            # Attempt to convert text content to an
            self._dict = mws_xml_to_dict(self._response.text, force_cdata=force_cdata)
        except ExpatError:
            # Probably not XML content: just ignore it.
            pass
        else:
            # No exception? Cool
            self._build_dotdict_data()

    def __repr__(self):
        return "<{} [{}]>".format(self.__class__.__name__, self._response.status_code)

    def _build_dotdict_data(self):
        """Convert XML response content to a Python dictionary using `xmltodict`."""
        self._dotdict = DotDict(self._dict)

        # Extract ResponseMetadata as a separate DotDict, if provided
        if "ResponseMetadata" in self._dict:
            self._metadata = DotDict(self._dict["ResponseMetadata"])

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
        """Shortcut to ResponseMetadata.RequestId if present.
        Returns None if not found.
        """
        if self.metadata is not None:
            return self.metadata.get("RequestId")
        return None

    @property
    def timestamp(self):
        """Returns the timestamp when the request was sent."""
        return self._request_timestamp
