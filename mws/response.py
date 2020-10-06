"""Contains the MWSResponse object and related utilities."""

from xml.parsers.expat import ExpatError

from mws.utils.xml import mws_xml_to_dict
from mws.errors import MWSError
from mws.utils.collections import DotDict
from mws.utils.crypto import calc_md5


__all__ = ["MWSResponse"]


class ResponseWrapperBase:
    """Wraps a ``requests.Response`` object, storing the object internally
    and providing access to its public attributes as read-only properties.

    Mainly serves as a base class for ``MWSResponse``, so as to separate this code.
    """

    def __init__(self, response):
        self.original = response

    @property
    def text(self):
        """Shortcut to ``.original.text``, which is unicode."""
        return self.original.text

    @property
    def content(self):
        """Shortcut to ``.original.content``, which is bytes."""
        return self.original.content

    @property
    def status_code(self):
        """Shortcut to ``.original.status_code``."""
        return self.original.status_code

    @property
    def headers(self):
        """Shortcut to ``.original.headers``."""
        return self.original.headers

    @property
    def encoding(self):
        """Shortcut to ``.original.encoding``.
        Can also be used as a setter, changing the encoding of the response.
        This then changes how content is decoded when using :py:meth:`.text <.text>`.
        """
        return self.original.encoding

    @encoding.setter
    def encoding(self, val):
        self.original.encoding = val

    @property
    def reason(self):
        """Shortcut to ``.original.reason``."""
        return self.original.reason

    @property
    def cookies(self):
        """Shortcut to ``.original.cookies``."""
        return self.original.cookies

    @property
    def elapsed(self):
        """Shortcut to ``.original.elapsed``."""
        return self.original.elapsed

    @property
    def request(self):
        """Shortcut to ``.original.request``."""
        return self.original.request


class MWSResponse(ResponseWrapperBase):
    """Wraps a ``requests.Response`` object and extracts some known data.

    Particularly for XML responses, parsed contents can be found in the ``.parsed``
    property as a ``DotDict`` instance.

    Find metadata in ``.metadata``, mainly for accessing ``.metadata.RequestId``;
    or simply use the ``.request_id`` shortcut attr.

    :param request.Response response: Response object returned by a request sent
     to MWS.
    :param str result_key: Key to use as the root for ``.parsed``.
     Typically a tag in the root of the response's XML document whose name ends
     in ``Result``. Defaults to ``None``, in which case the full document is
     presented when using ``.parsed``.
    :param bool force_cdata: Passed to ``xmltodict.parse()`` when parsing
     the response's XML document. Defaults to ``False``.
    """

    __attrs__ = [
        "original",
        "content",
        "text",
        "status_code",
        "headers",
        "encoding",
        "reason",
        "cookies",
        "elapsed",
        "request",
        "parse_response",
        "parsed",
        "metadata",
        "request_id",
    ]

    def __init__(self, response, result_key=None, encoding=None, force_cdata=False):
        super().__init__(response)
        self.timestamp = None
        self._result_key = result_key

        if not self.encoding:
            # If the response did not specify its encoding,
            # we use either A) an encoding specified by the user,
            # or B) the ``apparent_encoding`` of the ``requests.Response`` object,
            # which uses ``chardet`` to guess the encoding of the response content.
            # Either way, we need an encoding saved in order to parse the content
            # from XML into DotDicts.
            self.encoding = encoding or response.apparent_encoding

        self._dict = None
        self._dotdict = None
        self._metadata = None
        self.parse_response(force_cdata=force_cdata)

    def __repr__(self):
        return "<{} [{}]>".format(self.__class__.__name__, self.original.status_code)

    def parse_response(self, force_cdata=False):
        """Runs :py:meth:`.text <.text>` through ``xmltodict.parse()``, storing the
        returned Python dictionary as ``._dict``.

        If no XML errors occur during that process, constructs
        :py:class:`DotDict <mws.collections.DotDict>` instances
        from the parsed XML data, making them available from
        :py:meth:`.parsed <.parsed>` and :py:meth:`.metadata <.metadata>`.

        For non-XML responses, does nothing.

        :param bool force_cdata: Passed to ``xml_to_dict.parse()`` when
         parsing XML content. Defaults to ``False``. Ignored for non-XML responses.
        """
        try:
            # Attempt to convert text content to an
            self._dict = mws_xml_to_dict(
                self.content, encoding=self.encoding, force_cdata=force_cdata
            )
        except ExpatError:
            # Probably not XML content: just ignore it.
            pass
        else:
            # No exception? Cool
            self._build_dotdicts()

    def _build_dotdicts(self):
        self._dotdict = DotDict(self._dict)

        # Extract ResponseMetadata as a separate DotDict, if provided
        if "ResponseMetadata" in self._dict:
            self._metadata = DotDict(self._dict["ResponseMetadata"])

    @property
    def parsed(self):
        """Returns a parsed version of the response.

        For XML documents, returns a :py:class:`DotDict <mws.collections.DotDict>`
        of the parsed XML content, starting from ``._result_key``.

        For all other types of responses, returns :py:meth:`.text <.text>` instead.
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
        """Returns a :py:class:`DotDict <mws.collections.DotDict>` instance from the
        response's ``ResponseMetadata`` key, if present.
        Typically the only key of note here is ``.metadata.RequestId``,
        which can also be accessed with :py:meth:`.request_id <.request_id>`.
        """
        return self._metadata

    @property
    def request_id(self):
        """Returns the value of a ``RequestId`` from :py:meth:`.metadata <.metadata>`,
        if present, otherwise ``None``.
        """
        if self.metadata is not None:
            return self.metadata.get("RequestId")
        return None
