# -*- coding: utf-8 -*-
"""Main module for python-amazon-mws package."""

from enum import Enum
from urllib.parse import quote
import base64
import hashlib
import hmac
import warnings

from requests import request
from requests.exceptions import HTTPError

from mws.errors import MWSError
from mws.response import MWSResponse
from mws.utils.crypto import response_md5_is_valid
from mws.utils.params import (
    clean_params_dict,
    enumerate_param,
    flat_param_dict,
    remove_empty_param_keys,
)
from mws.utils.timezone import mws_utc_now


__version__ = "1.0dev16"
PAM_USER_AGENT = "python-amazon-mws/{} (Language=Python)".format(__version__)
"""See recommended user agent string format:
https://docs.developer.amazonservices.com/en_US/dev_guide/DG_UserAgentHeader.html
"""

PAM_DEFAULT_TIMEOUT = 300

__all__ = [
    "calc_request_description",
    "Marketplaces",
    "MWS",
]


class Marketplaces(Enum):
    """Enumeration for MWS marketplaces, containing endpoints and marketplace IDs.

    Example, endpoint and ID for UK marketplace:
        endpoint = Marketplaces.UK.endpoint
        marketplace_id = Marketplaces.UK.marketplace_id
    """

    AE = ("https://mws.amazonservices.ae", "A2VIGQ35RCS4UG")
    AU = ("https://mws.amazonservices.com.au", "A39IBJ37TRP1C6")
    BR = ("https://mws.amazonservices.com", "A2Q3Y263D00KWC")
    CA = ("https://mws.amazonservices.ca", "A2EUQ1WTGCTBG2")
    DE = ("https://mws-eu.amazonservices.com", "A1PA6795UKMFR9")
    EG = ("https://mws-eu.amazonservices.com", "ARBP9OOSHTCHU")
    ES = ("https://mws-eu.amazonservices.com", "A1RKKUPIHCS9HS")
    FR = ("https://mws-eu.amazonservices.com", "A13V1IB3VIYZZH")
    GB = ("https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P")
    IN = ("https://mws.amazonservices.in", "A21TJRUUN4KGV")
    IT = ("https://mws-eu.amazonservices.com", "APJ6JRA9NG5V4")
    JP = ("https://mws.amazonservices.jp", "A1VC38T7YXB528")
    MX = ("https://mws.amazonservices.com.mx", "A1AM78C64UM0Y8")
    NL = ("https://mws-eu.amazonservices.com", "A1805IZSGTT6HS")
    SA = ("https://mws-eu.amazonservices.com", "A17E79C6D8DWNP")
    SE = ("https://mws-eu.amazonservices.com", "A2NODRKZP88ZB9")
    SG = ("https://mws-fe.amazonservices.com", "A19VAU5U5O7RUS")
    TR = ("https://mws-eu.amazonservices.com", "A33AVAJ2PDY3EV")
    UK = ("https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P")  # alias for GB
    US = ("https://mws.amazonservices.com", "ATVPDKIKX0DER")

    def __init__(self, endpoint, marketplace_id):
        """Easy dot access like: Marketplaces.endpoint ."""
        self.endpoint = endpoint
        self.marketplace_id = marketplace_id

    @property
    def value(self):
        return self.marketplace_id


## TODO DEPRECATE THIS ##
def calc_request_description(params):
    """Builds the request description as a single string from the set of params.

    Each key-value pair takes the form "key=value"
    Sets of "key=value" pairs are joined by "&".
    Keys should appear in alphabetical order in the result string.

    Example:
      params = {'foo': 1, 'bar': 4, 'baz': 'potato'}
    Returns:
      "bar=4&baz=potato&foo=1"
    """
    description_items = []
    for item in sorted(params.keys()):
        encoded_val = params[item]
        description_items.append("{}={}".format(item, encoded_val))
    return "&".join(description_items)


class MWS(object):
    """Base Amazon API class.

    NOTICE FOR 1.0 RELEASE TESTING
    ------------------------------

    A new parser, ``mws.utils.parsers.MWSResponse``, can be used to process requests
    made to MWS. To test the new parser:

    .. code-block:: python

        # instantiate your API class as usual
        api = Products(access_key, secret_key, account_id, ...)
        # Then set the `_use_feature_mwsresponse` flag on the instance.
        api._use_feature_mwsresponse = True

    Now all requests you make with this instance of the API class
    will run through ``MWSResponse``.
    """

    # This is used to post/get to the different uris used by amazon per api
    # ie. /Orders/2011-01-01
    # All subclasses must define their own URI only if needed
    URI = "/"

    # The API version varies in most amazon APIs
    VERSION = "2009-01-01"

    # There seem to be some xml namespace issues. therefore every api subclass
    # is recommended to define its namespace, so that it can be referenced
    # like so AmazonAPISubclass.NAMESPACE.
    # For more information see https://stackoverflow.com/a/8719461/389453
    NAMESPACE = ""

    # In here we name each of the operations available to the subclass
    # that have 'ByNextToken' operations associated with them.
    # If the Operation is not listed here, self.action_by_next_token
    # will raise an error.
    NEXT_TOKEN_OPERATIONS = []

    # Some APIs are available only to either a "Merchant" or "Seller"
    # the type of account needs to be sent in every call to the amazon MWS.
    # This constant defines the exact name of the parameter Amazon expects
    # for the specific API being used.
    # All subclasses need to define this if they require another account type
    # like "Merchant" in which case you define it like so.
    # ACCOUNT_TYPE = "Merchant"
    # Which is the name of the parameter for that specific account type.

    # For using proxy you need to init this class with one more parameter proxies. It must look like 'ip_address:port'
    # if proxy without auth and 'login:password@ip_address:port' if proxy with auth

    ACCOUNT_TYPE = "SellerId"

    def __init__(
        self,
        access_key,
        secret_key,
        account_id,
        region="US",
        uri="",
        version="",
        auth_token="",
        proxy=None,
        user_agent_str="",
        headers=None,
        force_response_encoding=None,
    ):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.auth_token = auth_token
        self.version = version or self.VERSION
        self.uri = uri or self.URI
        self.proxy = proxy
        self.user_agent_str = user_agent_str or PAM_USER_AGENT
        self.extra_headers = headers or {}
        self.force_response_encoding = force_response_encoding

        # * TESTING FLAGS * #
        self._test_request_params = False
        self._use_feature_mwsresponse = False

        if region in Marketplaces.__members__:
            self.domain = Marketplaces[region].endpoint
        else:
            error_msg = (
                "Incorrect region supplied: {region}. "
                "Must be one of the following: {regions}".format(
                    region=region,
                    regions=", ".join(Marketplaces.__members__.keys()),
                )
            )
            raise MWSError(error_msg)

    def get_default_params(self, action, timestamp):
        """Get the params required in all MWS requests."""
        params = {
            "Action": action,
            "AWSAccessKeyId": self.access_key,
            self.ACCOUNT_TYPE: self.account_id,
            "SignatureVersion": "2",
            "Timestamp": timestamp,
            "Version": self.version,
            "SignatureMethod": "HmacSHA256",
        }
        if self.auth_token:
            params["MWSAuthToken"] = self.auth_token
        # TODO current tests only check for auth_token being set.
        # need a branch test to check for auth_token being skipped (no key present)
        return params

    def make_request(
        self, action, params=None, method="GET", timeout=PAM_DEFAULT_TIMEOUT, **kwargs
    ):
        """Make request to Amazon MWS API with these params.

        `action` is a string matching the name of the request action
        (i.e. "ListOrders").

        `params` is a flat dict containing params to pass to the operation.

        `method` is a string, matching an HTTP verb ("GET", "POST", etc.),
        which sets the method for a `requests.request` call.

        `timeout` passes to `requests.request`, setting the timeout for this request.

        `kwargs` may include:

        - `result_key`, providing a custom key to use as the root for results
          returned by `response.parsed`.
        - `body`, primarily used in Feeds requests to send a data file in the request.
        """
        params = params or {}

        request_timestamp = mws_utc_now()
        request_params = self.get_default_params(action, request_timestamp)
        proxies = self.get_proxies()
        request_params.update(params)

        # Remove empty keys and clean values before transmitting
        request_params = remove_empty_param_keys(request_params)
        request_params = clean_params_dict(request_params)

        if self._test_request_params:
            # Testing method: return the params from this request before the request is made.
            return request_params
        # TODO: All current testing stops here. More branches needed.

        request_description = calc_request_description(request_params)
        signature = self.calc_signature(method, request_description)
        url = "{domain}{uri}?{description}&Signature={signature}".format(
            domain=self.domain,
            uri=self.uri,
            description=request_description,
            signature=quote(signature),
        )
        headers = {"User-Agent": self.user_agent_str}
        headers.update(self.extra_headers)
        headers.update(kwargs.get("extra_headers", {}))

        result_key = kwargs.get("result_key", "{}Result".format(action))

        try:
            # Some might wonder as to why i don't pass the params dict as the params argument to request.
            # My answer is, here i have to get the url parsed string of params in order to sign it, so
            # if i pass the params dict as params to request, request will repeat that step because it will need
            # to convert the dict to a url parsed string, so why do it twice if i can just pass the full url :).

            # TODO ^^ Because that's not how a POST request works, man!
            # We're gonna fix this!
            response = request(
                method,
                url,
                data=kwargs.get("body", ""),
                headers=headers,
                proxies=proxies,
                timeout=timeout,
            )
            response.raise_for_status()
            # When retrieving data from the response object,
            # be aware that response.content returns the content in bytes while response.text calls
            # response.content and converts it to unicode.

            if self._use_feature_mwsresponse:
                # Turn on the new response parser and DotDict parsed output
                # (will be made standard in v1.0)
                if not response_md5_is_valid(response):
                    raise MWSError(
                        "MD5 hash validation failed: wrong content length for response"
                    )

                parsed_response = MWSResponse(
                    response,
                    result_key=result_key,
                    encoding=self.force_response_encoding,
                )
                parsed_response.timestamp = request_timestamp
            else:
                ### DEPRECATED ###
                # Remove in v1.0
                from xml.etree.ElementTree import ParseError as XMLError
                from mws.utils.parsers import DictWrapper, DataWrapper

                data = response.content
                try:
                    try:
                        parsed_response = DictWrapper(data, result_key)
                    except TypeError:
                        # When we got CSV as result, we will got error on this
                        parsed_response = DictWrapper(response.text, result_key)

                except XMLError:
                    parsed_response = DataWrapper(data, response.headers)
                parsed_response.response = response

        except HTTPError as exc:
            error = MWSError(str(exc.response.text))
            error.response = exc.response
            raise error

        # Store the response object in the parsed_response for quick access
        return parsed_response

    def get_proxies(self):
        """Return a dict of http and https proxies, as defined by `self.proxy`."""
        proxies = {"http": None, "https": None}
        if self.proxy:
            # TODO need test to enter here
            proxies = {
                "http": "http://{}".format(self.proxy),
                "https": "https://{}".format(self.proxy),
            }
        return proxies

    def get_service_status(self):
        """Returns MWS service status.

        Typical return values (embedded within `response.parsed`) are:

        - GREEN
        - GREEN_I
        - YELLOW
        - RED

        The same request can be used for any MWS API subclass, and MWS may respond
        differently for each endpoint. Best to use this method from the same API
        subclass you intend to use for other requests!

        Docs (from Orders API example):
        https://docs.developer.amazonservices.com/en_US/orders-2013-09-01/MWS_GetServiceStatus.html
        """
        return self.make_request("GetServiceStatus")

    def action_by_next_token(self, action, next_token):
        """Run a '...ByNextToken' action for the given action.

        If the action is not listed in self.NEXT_TOKEN_OPERATIONS, MWSError is raised.
        Action is expected NOT to include 'ByNextToken'
        at the end of its name for this call: function will add that by itself.
        """
        if action not in self.NEXT_TOKEN_OPERATIONS:
            # TODO Would like a test entering here.
            # Requires a dummy API class to be written that will trigger it.
            raise MWSError(
                (
                    "{} action not listed in this API's NEXT_TOKEN_OPERATIONS. "
                    "Please refer to documentation."
                ).format(action)
            )

        action = "{}ByNextToken".format(action)

        return self.make_request(action, {"NextToken": next_token}, method="POST")

    def calc_signature(self, method, request_description):
        """Calculate MWS signature to interface with Amazon

        Args:
            method (str)
            request_description (str)
        """
        sig_data = "\n".join(
            [
                method,
                self.domain.replace("https://", "").lower(),
                self.uri,
                request_description,
            ]
        )
        return base64.b64encode(
            hmac.new(
                self.secret_key.encode(), sig_data.encode(), hashlib.sha256
            ).digest()
        )

    def enumerate_param(self, param, values):
        """DEPRECATED, alias for `utils.params.enumerate_param`."""
        from mws.utils.deprecation import RemovedInPAM10Warning

        warnings.warn(
            (
                "MWS.enumerate_param is deprecated. "
                "Please use methods in 'mws.utils.params', instead."
            ),
            RemovedInPAM10Warning,
        )
        return enumerate_param(param, values)

    def generic_request(
        self, action, params=None, method="GET", timeout=PAM_DEFAULT_TIMEOUT, **kwargs
    ):
        """Builds a generic request with arbitrary parameter arguments.
        This method should be called from an API subclass (``Orders``, ``Feeds``, etc.),
        else the ``uri`` attribute of the class instance must be set manually.

        This method's signature matches that of ``.make_request``, as the two methods
        are similar. However, ``params`` is expected to be either the default ``None``
        or a nested dictionary, that is then passed to
        :py:func:`flat_param_dict() <mws.utils.params.flat_param_dict>`.
        """
        # NOTE you may be asking why this method exists. Why not simply put the logic
        # of `flat_param_dict` into `make_request`, and let every request method
        # pass nested objects freely?
        # Well, I tried that. Turns out giving up that kind of control has some
        # unintended consequences.
        # For instance, say you know that a given parameter for your request only takes
        # one value, such as `ReportType=_SOME_REPORT_TYPE_`.
        # If the user passes a list wrapping that string, `flat_param_dict` will
        # happily enumerate that value: `ReportType.1=_SOME_REPORT_TYPE_`.
        # For that particular request, we would know this to be an error: MWS will
        # not accept that entry. Surfacing that error to the end user would be quite
        # difficult, and trying to prevent it would introduce the hassle of verifying
        # argument types in every request method.
        # It is better to allow that list object to pass through the params to
        # `make_request`, where it can raise an error in our code, rather than have
        # the request get sent to MWS.
        if not self.uri or self.uri == "/":
            raise ValueError(
                (
                    "Cannot send generic request to URI '%s'. "
                    "Please use one of the API classes "
                    "(`mws.apis.Reports`, `mws.apis.Feeds`, etc.) "
                    "to initiate this request."
                )
                % self.uri
            )
        if not isinstance(params, dict):
            raise ValueError("`params` must be a dict.")
        data = flat_param_dict(params)
        return self.make_request(
            action=action, params=data, method=method, timeout=timeout, **kwargs
        )
