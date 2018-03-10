# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import datetime
import hashlib
import hmac
import re
import warnings

from requests import request
from requests.exceptions import HTTPError

from . import utils

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote
try:
    from xml.etree.ElementTree import ParseError as XMLError
except ImportError:
    from xml.parsers.expat import ExpatError as XMLError


__version__ = '1.0.0'
    'MerchantFulfillment',

# See https://images-na.ssl-images-amazon.com/images/G/01/mwsportal/doc/en_US/bde/MWSDeveloperGuide._V357736853_.pdf
# page 8
# for a list of the end points and marketplace IDs

MARKETPLACES = {
    "CA": "https://mws.amazonservices.ca",  # A2EUQ1WTGCTBG2
    "US": "https://mws.amazonservices.com",  # ATVPDKIKX0DER",
    "DE": "https://mws-eu.amazonservices.com",  # A1PA6795UKMFR9
    "ES": "https://mws-eu.amazonservices.com",  # A1RKKUPIHCS9HS
    "FR": "https://mws-eu.amazonservices.com",  # A13V1IB3VIYZZH
    "IN": "https://mws.amazonservices.in",  # A21TJRUUN4KGV
    "IT": "https://mws-eu.amazonservices.com",  # APJ6JRA9NG5V4
    "UK": "https://mws-eu.amazonservices.com",  # A1F83G8C2ARO7P
    "JP": "https://mws.amazonservices.jp",  # A1VC38T7YXB528
    "CN": "https://mws.amazonservices.com.cn",  # AAHKV2X7AFYLW
    "MX": "https://mws.amazonservices.com.mx",  # A1AM78C64UM0Y8
}


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
    Entries are escaped with urllib quote method, formatted as "key=value", and joined with "&".
    """
    request_description = ''
    for key in sorted(params):
        encoded_value = quote(params[key], safe='-_.~')
        request_description += '&{}={}'.format(key, encoded_value)
    return request_description[1:]  # don't include leading ampersand


def remove_empty(dict_):
    """
    Returns dict_ with all empty values removed.
    """
    return {k: v for k, v in dict_.items() if v}


def remove_namespace(xml):
    """
    Strips the namespace from XML document contained in a string.
    Returns the stripped string.
    """
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub('', xml)


class DictWrapper(object):
    def __init__(self, xml, rootkey=None):
        self.original = xml
        self.response = None
        self._rootkey = rootkey
        self._mydict = utils.XML2Dict().fromstring(remove_namespace(xml))
        self._response_dict = self._mydict.get(list(self._mydict.keys())[0], self._mydict)

    @property
    def parsed(self):
        if self._rootkey:
            return self._response_dict.get(self._rootkey)
        return self._response_dict


class DataWrapper(object):
    """
    Text wrapper in charge of validating the hash sent by Amazon.
    """
    def __init__(self, data, header):
        self.original = data
        self.response = None
        if 'content-md5' in header:
            hash_ = utils.calc_md5(self.original)
            if header['content-md5'].encode() != hash_:
                raise MWSError("Wrong Contentlength, maybe amazon error...")

    @property
    def parsed(self):
        return self.original


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

    # There seem to be some xml namespace issues. therefore every api subclass
    # is recommended to define its namespace, so that it can be referenced
    # like so AmazonAPISubclass.NAMESPACE.
    # For more information see http://stackoverflow.com/a/8719461/389453
    NAMESPACE = ''

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
    ACCOUNT_TYPE = "SellerId"

    def __init__(self, access_key, secret_key, account_id,
                 region='US', domain='', uri="",
                 version="", auth_token=""):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.auth_token = auth_token
        self.version = version or self.VERSION
        self.uri = uri or self.URI

        if domain:
            self.domain = domain
        elif region in MARKETPLACES:
            self.domain = MARKETPLACES[region]
        else:
            error_msg = "Incorrect region supplied ('%(region)s'). Must be one of the following: %(marketplaces)s" % {
                "marketplaces": ', '.join(MARKETPLACES.keys()),
                "region": region,
            }
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
        return params

    def make_request(self, extra_data, method="GET", **kwargs):
        """
        Make request to Amazon MWS API with these parameters
        """

        # Remove all keys with an empty value because
        # Amazon's MWS does not allow such a thing.
        extra_data = remove_empty(extra_data)

        # convert all Python date/time objects to isoformat
        for key, value in extra_data.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                extra_data[key] = value.isoformat()

        params = self.get_default_params()
        params.update(extra_data)
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
            # Some might wonder as to why i don't pass the params dict as the params argument to request.
            # My answer is, here i have to get the url parsed string of params in order to sign it, so
            # if i pass the params dict as params to request, request will repeat that step because it will need
            # to convert the dict to a url parsed string, so why do it twice if i can just pass the full url :).
            response = request(method, url, data=kwargs.get('body', ''), headers=headers)
            response.raise_for_status()
            # When retrieving data from the response object,
            # be aware that response.content returns the content in bytes while response.text calls
            # response.content and converts it to unicode.

            data = response.content
            # I do not check the headers to decide which content structure to server simply because sometimes
            # Amazon's MWS API returns XML error responses with "text/plain" as the Content-Type.
            rootkey = kwargs.get('rootkey', extra_data.get("Action") + "Result")
            try:
                try:
                    parsed_response = DictWrapper(data, rootkey)
                except TypeError:  # raised when using Python 3 and trying to remove_namespace()
                    # When we got CSV as result, we will got error on this
                    parsed_response = DictWrapper(response.text, rootkey)

            except XMLError:
                parsed_response = DataWrapper(data, response.headers)

        except HTTPError as exc:
            error = MWSError(str(exc.response.text))
            error.response = exc.response
            raise error

        # Store the response object in the parsed_response for quick access
        parsed_response.response = response
        return parsed_response

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
            raise MWSError((
                "{} action not listed in this API's NEXT_TOKEN_OPERATIONS. "
                "Please refer to documentation."
            ).format(action))

        action = '{}ByNextToken'.format(action)

        data = dict(
            Action=action,
            NextToken=next_token
        )
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
        warnings.warn((
            "Please use `utils.enumerate_param` for one param, or "
            "`utils.enumerate_params` for multiple params."
        ), DeprecationWarning)
        return utils.enumerate_param(param, values)



# * Merchant Fulfillment API * #
class MerchantFulfillment(MWS):
    """
    Amazon MWS Merchant Fulfillment API
    """
    URI = "/MerchantFulfillment/2015-06-01"
    VERSION = "2015-06-01"
    NS = '{https://mws.amazonservices.com/MerchantFulfillment/2015-06-01}'

    def get_eligible_shipping_services(self, amazon_order_id=None, seller_orderid=None, item_list=[],
                                       ship_from_address={}, package_dimensions={}, weight={},
                                       must_arrive_by_date=None, ship_date=None,
                                       shipping_service_options={}, label_customization={}):

        data = {
            "Action": "GetEligibleShippingServices",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_orderid,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", item_list))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def create_shipment(self, amazon_order_id=None, seller_orderid=None, item_list=[], ship_from_address={},
                        package_dimensions={}, weight={}, must_arrive_by_date=None, ship_date=None,
                        shipping_service_options={}, label_customization={}, shipping_service_id=None,
                        shipping_service_offer_id=None, hazmat_type=None):

        data = {
            "Action": "CreateShipment",
            "ShipmentRequestDetails.AmazonOrderId": amazon_order_id,
            "ShipmentRequestDetails.SellerOrderId": seller_orderid,
            "ShipmentRequestDetails.MustArriveByDate": must_arrive_by_date,
            "ShipmentRequestDetails.ShipDate": ship_date,
            "ShippingServiceId": shipping_service_id,
            "ShippingServiceOfferId": shipping_service_offer_id,
            "HazmatType": hazmat_type
        }
        data.update(utils.enumerate_keyed_param("ShipmentRequestDetails.ItemList.Item", item_list))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShipFromAddress", ship_from_address))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.PackageDimensions", package_dimensions))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.Weight", weight))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.ShippingServiceOptions", shipping_service_options))
        data.update(utils.dict_keyed_param("ShipmentRequestDetails.LabelCustomization", label_customization))
        return self.make_request(data)

    def get_shipment(self, shipment_id=None):
        data = dict(Action="GetShipment", ShipmentId=shipment_id)
        return self.make_request(data)

    def cancel_shipment(self, shipment_id=None):
        data = dict(Action="CancelShipment", ShipmentId=shipment_id)
        return self.make_request(data)