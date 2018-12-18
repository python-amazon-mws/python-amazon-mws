# -*- coding: utf-8 -*-
"""
Main module for python-amazon-mws package.
"""

from __future__ import absolute_import

import base64
import datetime
import hashlib
import hmac
import re
import warnings

import chardet
import requests
from requests.exceptions import HTTPError
from xml.parsers.expat import ExpatError
import xmltodict
from enum import Enum


from . import utils

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

__version__ = '1.0.0dev11'


class Marketplaces(Enum):
    """
    Format: Country code: endpoint, marketplace_id.
    """
    AU = ('https://mws.amazonservices.com.au', 'A39IBJ37TRP1C6')
    BR = ('https://mws.amazonservices.com', 'A2Q3Y263D00KWC')
    CA = ('https://mws.amazonservices.ca', 'A2EUQ1WTGCTBG2')
    CN = ('https://mws.amazonservices.com.cn', 'AAHKV2X7AFYLW')
    DE = ('https://mws-eu.amazonservices.com', 'A1PA6795UKMFR9')
    ES = ('https://mws-eu.amazonservices.com', 'A1RKKUPIHCS9HS')
    FR = ('https://mws-eu.amazonservices.com', 'A13V1IB3VIYZZH')
    IN = ('https://mws.amazonservices.in', 'A21TJRUUN4KGV')
    IT = ('https://mws-eu.amazonservices.com', 'APJ6JRA9NG5V4')
    JP = ('https://mws.amazonservices.jp', 'A1VC38T7YXB528')
    MX = ('https://mws.amazonservices.com.mx', 'A1AM78C64UM0Y8')
    UK = ('https://mws-eu.amazonservices.com', 'A1F83G8C2ARO7P')
    US = ('https://mws.amazonservices.com', 'ATVPDKIKX0DER')

    def __init__(self, endpoint, marketplace_id):
        """Easy dot access like: Marketplaces.endpoint ."""
        self.endpoint = endpoint
        self.marketplace_id = marketplace_id


class MWSError(Exception):
    """
    Main MWS Exception class
    """
    # Allows quick access to the response object.
    # Do not rely on this attribute, always check if its not None.
    response = None


def calc_request_description(params):
    """
    Returns a flatted string with the request description, built from the params dict.

    Keys should appear in alphabetical order in the result string.
    Example:
      params = {'foo': 1, 'bar': 4, 'baz': 'potato'}
    Returns:
      "bar=4&baz=potato&foo=1"
    """
    description_items = [
        '{}={}'.format(item, params[item]) for item in sorted(params.keys())]
    return '&'.join(description_items)


def clean_params(params):
    """
    Cleanup, html-escape and prevent a lot of common input mistakes for all parameter.
    """
    # silently remove parameter where values are empty
    params = {k: v for k, v in params.items() if v}

    params_enc = dict()
    for key, value in params.items():
        if isinstance(value, (dict, list, set, tuple)):
            message = 'expected string or datetime datatype, got {},'\
                'for key {} and value {}'.format(
                    type(value), key, str(value))
            raise MWSError(message)
        if isinstance(value, (datetime.datetime, datetime.date)):
            value = value.isoformat()
        if isinstance(value, bool):
            value = str(value).lower()
        value = str(value)

        params_enc[key] = quote(value, safe='-_.~')
    return params_enc


def validate_hash(response):
    """
    Input is a requests.response object, see the test class FakeResponse.
    """
    hash_ = utils.calc_md5(response.content)
    if response.headers['content-md5'].encode() != hash_:
        raise MWSError("Wrong Content length, maybe amazon error...")


class DataWrapper(object):
    """
    For all responses this is the rich object, you find all attributes here.

    We highly recommend to use the property apiresponse.parsed
    it works for all responses.

    You can also manually choose different recommended attributes
    for xml and textfiles.

    The recommended objects should be enough for all users.
    Additional details:
    The decoding we used you can find in apiresponse.original.encoding.

    The request.Response object is central, now its only a fallback:
    docs: http://docs.python-requests.org/en/master/api/#requests.Response
    apiresponse.original
    """

    def __init__(self, data, rootkey=None, force_cdata=False):
        """
        Besides the recommended apiresponse.parsed property, we offer a couple
        of useful attributes here.
        """
        # Fallback, raw and meta attributes for xml and textfiles
        self.original = data  # requests.request response object, link above
        self.headers = self.original.headers  # just easier to access

        # Recommended attributes only for xml
        self.pydict = None  # alternative to xml parsed or dot_dict
        self.dot_dict = None  # fallback for xml parsed

        # Recommended attribute only for textdata
        self.textdata = None

        # parsing
        self._rootkey = rootkey
        self._force_cdata = force_cdata
        self._main()

    def _main(self):
        """
        Try different parsing strategies.
        """
        # a better guess for the correct encoding
        self.original.encoding = self.guess_encoding()
        textdata = self.original.text
        # We don't trust the amazon content marker.
        try:  # try to parse as xml
            self._xml2dict(textdata)
        except ExpatError:  # if it's not xml its a plain textfile, like a csv
            self.textdata = textdata

    def guess_encoding(self):
        """
        Detecting encoding incrementally with a hotfix.
        """
        # fix for one none ascii character
        chardet.utf8prober.UTF8Prober.ONE_CHAR_PROB = 0.26
        bytelist = self.original.content.splitlines()
        detector = chardet.UniversalDetector()
        for line in bytelist:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
        return detector.result['encoding']

    def _xml2dict(self, rawdata):
        """
        Parse XML with xmltodict to a python dictionary.
        """
        namespaces = self._extract_namespaces(rawdata)
        self._mydict = xmltodict.parse(rawdata, dict_constructor=dict,
                                       process_namespaces=True,
                                       namespaces=namespaces,
                                       force_cdata=self._force_cdata)
        # unpack if possible, important for accessing the rootkey
        self.pydict = self._mydict.get(list(self._mydict.keys())[0],
                                       self._mydict)
        self.dot_dict = utils.DotDict(self.pydict)

    def _extract_namespaces(self, rawdata):
        """
        Parse all namespaces.
        """
        pattern = re.compile(r'xmlns[:ns2]*="\S+"')
        raw_namespaces = pattern.findall(rawdata)
        return {x.split('"')[1]: None for x in raw_namespaces}

    @property
    def parsed(self):
        """
        Recieve a nice formatted response, this can be your default.
        """
        if self.dot_dict is not None:
            # When we have succesful parsed a xml response.
            if self._rootkey != 'ignore':
                return self.dot_dict.get(self._rootkey, None)
            else:
                # ignore flag we use for xmlreports, not all have the same root
                return self.dot_dict
        else:
            return self.textdata


class MWS(object):
    """
    Base Amazon API class
    """
    # This is used to post/get to the different uris used by amazon per api
    # ie. /Orders/2011-01-01
    # All subclasses must define their own URI only if needed
    URI = "/"

    # The API version varies in most amazon APIs
    VERSION = "2009-01-01"

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

    def __init__(self, access_key, secret_key, account_id,
                 region='US', uri='', version='', auth_token='', proxy=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.auth_token = auth_token
        self.version = version or self.VERSION
        self.uri = uri or self.URI
        self.proxy = proxy

        # * TESTING FLAGS * #
        self._test_request_params = False

        if region in Marketplaces.__members__:
            self.domain = Marketplaces[region].endpoint
        else:
            error_msg = 'Incorrect region supplied: {region}. ' \
                'Must be one of the following: {regions}'.format(
                    region=region,
                    regions=', '.join(Marketplaces.__members__.keys()),
                )
            raise MWSError(error_msg)

    def get_default_params(self):
        """
        Get the parameters required in all MWS requests
        """
        params = {
            'AWSAccessKeyId': self.access_key,
            self.ACCOUNT_TYPE: self.account_id,
            'SignatureVersion': '2',
            'Timestamp': utils.get_utc_timestamp(),
            'Version': self.version,
            'SignatureMethod': 'HmacSHA256',
        }
        if self.auth_token:
            params['MWSAuthToken'] = self.auth_token
        # TODO current tests only check for auth_token being set.
        # need a branch test to check for auth_token being skipped (no key present)
        return params

    def make_request(self, extra_data, method="GET", **kwargs):
        """
        Make request to Amazon MWS API with these parameters
        """
        params = self.get_default_params()
        proxies = self.get_proxies()
        params.update(extra_data)
        params = clean_params(params)
        # rootkey is always the Action parameter from your request function,
        # except for get_feed_submission_result
        rootkey = kwargs.get('rootkey', extra_data.get("Action") + "Result")

        if self._test_request_params:
            # Testing method: return the params from this request before the request is made.
            return params
        # TODO: All current testing stops here. More branches needed.

        request_description = calc_request_description(params)
        signature = self.calc_signature(method, request_description)
        url = "{domain}{uri}?{description}&Signature={signature}".format(
            domain=self.domain,
            uri=self.uri,
            description=request_description,
            signature=quote(signature),
        )
        headers = {'User-Agent': 'python-amazon-mws/{} (Language=Python)'.format(__version__)}
        headers.update(kwargs.get('extra_headers', {}))

        try:
            # The parameters are included in the url string.
            response = requests.request(method, url, data=kwargs.get(
                'body', ''), headers=headers, proxies=proxies)
            response.raise_for_status()

            if 'content-md5' in response.headers:
                validate_hash(response)
            parsed_response = DataWrapper(response, rootkey)

        except HTTPError as exc:
            error = MWSError(str(exc.response.text))
            error.response = exc.response
            raise error

        return parsed_response

    def get_proxies(self):
        proxies = {"http": None, "https": None}
        if self.proxy:
            # TODO need test to enter here
            proxies = {
                "http": "http://{}".format(self.proxy),
                "https": "https://{}".format(self.proxy),
            }
        return proxies

    def get_service_status(self):
        """
        Returns a GREEN, GREEN_I, YELLOW or RED status.
        Depending on the status/availability of the API its being called from.
        """
        return self.make_request(extra_data=dict(Action='GetServiceStatus'))

    def action_by_next_token(self, action, next_token):
        """
        Run a '...ByNextToken' action for the given action.
        If the action is not listed in self.NEXT_TOKEN_OPERATIONS, MWSError is raised.
        Action is expected NOT to include 'ByNextToken'
        at the end of its name for this call: function will add that by itself.
        """
        if action not in self.NEXT_TOKEN_OPERATIONS:
            # TODO Would like a test entering here.
            # Requires a dummy API class to be written that will trigger it.
            raise MWSError((
                "{} action not listed in this API's NEXT_TOKEN_OPERATIONS. "
                "Please refer to documentation."
            ).format(action))

        action = '{}ByNextToken'.format(action)

        data = {
            'Action': action,
            'NextToken': next_token,
        }
        return self.make_request(data, method="POST")

    def calc_signature(self, method, request_description):
        """
        Calculate MWS signature to interface with Amazon
        Args:
            method (str)
            request_description (str)
        """
        sig_data = '\n'.join([
            method,
            self.domain.replace('https://', '').lower(),
            self.uri,
            request_description
        ])
        return base64.b64encode(hmac.new(self.secret_key.encode(), sig_data.encode(), hashlib.sha256).digest())

    def enumerate_param(self, param, values):
        """
        DEPRECATED.
        Please use `utils.enumerate_param` for one param, or
        `utils.enumerate_params` for multiple params.
        """
        # TODO remove in 1.0 release.
        # No tests needed.
        warnings.warn((
            "Please use `utils.enumerate_param` for one param, or "
            "`utils.enumerate_params` for multiple params."
        ), DeprecationWarning)
        return utils.enumerate_param(param, values)
