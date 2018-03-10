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

    # For using proxy you need to init this class with one more parameter proxies. It must look like 'ip_address:port'
    # if proxy without auth and 'login:password@ip_address:port' if proxy with auth

    ACCOUNT_TYPE = "SellerId"

    def __init__(self, access_key, secret_key, account_id,
                 region='US', domain='', uri="",
                 version="", auth_token="", proxy=None):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.auth_token = auth_token
        self.version = version or self.VERSION
        self.uri = uri or self.URI
        self.proxy = proxy

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
        proxies = self.get_proxies()
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
            response = request(method, url, data=kwargs.get('body', ''), headers=headers, proxies=proxies)
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

    def get_proxies(self):
        proxies = {"http": None, "https": None}
        if self.proxy:
            proxies = {"http": "http://{}".format(self.proxy),
                       "https": "https://{}".format(self.proxy)}
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

    def get_inbound_guidance_for_sku(self, sku_list, marketplace_id):
        if not isinstance(sku_list, (list, tuple, set)):
            sku_list = [sku_list]
        data = dict(
            Action='GetInboundGuidanceForSKU',
            MarketplaceId=marketplace_id,
        )
        data.update(utils.enumerate_param('SellerSKUList.Id', sku_list))
        return self.make_request(data)

    def get_inbound_guidance_for_asin(self, asin_list, marketplace_id):
        if not isinstance(asin_list, (list, tuple, set)):
            asin_list = [asin_list]
        data = dict(
            Action='GetInboundGuidanceForASIN',
            MarketplaceId=marketplace_id,
        )
        data.update(utils.enumerate_param('ASINList.Id', asin_list))
        return self.make_request(data)

    def get_pallet_labels(self, shipment_id, page_type, num_pallets):
        """
        Returns pallet labels.
        `shipment_id` must match a valid, current shipment.
        `page_type` expected to be string matching one of following (not checked, in case Amazon requirements change):
            PackageLabel_Letter_2
            PackageLabel_Letter_6
            PackageLabel_A4_2
            PackageLabel_A4_4
            PackageLabel_Plain_Pape
        `num_pallets` is integer, number of labels to create.

        Documentation:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPalletLabels.html
        """
        data = dict(
            Action='GetPalletLabels',
            ShipmentId=shipment_id,
            PageType=page_type,
            NumberOfPallets=num_pallets,
        )
        return self.make_request(data)

    def get_unique_package_labels(self, shipment_id, page_type, package_ids):
        """
        Returns unique package labels for faster and more accurate shipment processing at the Amazon fulfillment center.

        `shipment_id` must match a valid, current shipment.
        `page_type` expected to be string matching one of following (not checked, in case Amazon requirements change):
            PackageLabel_Letter_2
            PackageLabel_Letter_6
            PackageLabel_A4_2
            PackageLabel_A4_4
            PackageLabel_Plain_Pape
        `package_ids` a single package identifier, or a list/tuple/set of identifiers, specifying for which package(s)
            you want package labels printed.

        Documentation:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetUniquePackageLabels.html
        """
        data = dict(
            Action='GetUniquePackageLabels',
            ShipmentId=shipment_id,
            PageType=page_type,
        )
        if not isinstance(package_ids, (list, tuple, set)):
            package_ids = [package_ids]
        data.update(utils.enumerate_param('PackageLabelsToPrint.member.', package_ids))
        return self.make_request(data)

    def confirm_transport_request(self, shipment_id):
        """
        Confirms that you accept the Amazon-partnered shipping estimate and you request that the
        Amazon-partnered carrier ship your inbound shipment.

        Documentation:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmTransportRequest.html
        """
        data = dict(
            Action='ConfirmTransportRequest',
            ShipmentId=shipment_id,
        )
        return self.make_request(data)

    # TODO this method is incomplete: it should be able to account for all TransportDetailInput types
    # docs: http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#TransportDetailInput
    # def put_transport_content(self, shipment_id, is_partnered, shipment_type, carrier_name, tracking_id):
    #     data = dict(
    #         Action='PutTransportContent',
    #         ShipmentId=shipment_id,
    #         IsPartnered=is_partnered,
    #         ShipmentType=shipment_type,
    #     )
    #     data['TransportDetails.NonPartneredSmallParcelData.CarrierName'] = carrier_name
    #     if isinstance(tracking_id, tuple):
    #         count = 0
    #         for track in tracking_id:
    #             data[
    #                 'TransportDetails.NonPartneredSmallParcelData.PackageList.member.{}.TrackingId'.format(count + 1)
    #             ] = track
    #     return self.make_request(data)

    def confirm_preorder(self, shipment_id, need_by_date):
        data = dict(
            Action='ConfirmPreorder',
            ShipmentId=shipment_id,
            NeedByDate=need_by_date,
        )
        return self.make_request(data)

    def get_preorder_info(self, shipment_id):
        data = dict(
            Action='GetPreorderInfo',
            ShipmentId=shipment_id,
        )
        return self.make_request(data)


        """
        http://docs.developer.amazonservices.com/en_UK/merch_fulfill/MerchFulfill_GetEligibleShippingServices.html

        :param amazon_order_id: Required
        :param seller_orderid:
        :param item_list: Required
        :param ship_from_address: Required
        :param package_dimensions: Required
        :param weight: Required
        :param must_arrive_by_date:
        :param ship_date:
        :param shipping_service_options: Required
        :param label_customization:
        :return:
        """

        if ship_from_address is None:
            ship_from_address = {}
        if package_dimensions is None:
            package_dimensions = {}
        if weight is None:
            weight = {}
        if item_list is None:
            item_list = []
        if shipping_service_options is None:
            shipping_service_options = {}
        if label_customization is None:
            label_customization = {}
        """
        http://docs.developer.amazonservices.com/en_UK/merch_fulfill/MerchFulfill_CreateShipment.html

        :param amazon_order_id: Required
        :param seller_orderid:
        :param item_list: Required
        :param ship_from_address: Required
        :param package_dimensions: Required
        :param weight: Required
        :param must_arrive_by_date:
        :param ship_date:
        :param shipping_service_options:
        :param label_customization:
        :param shipping_service_id: Required
        :param shipping_service_offer_id:
        :param hazmat_type:
        :return:
        """

        if item_list is None:
            item_list = []
        if ship_from_address is None:
            ship_from_address = {}
        if package_dimensions is None:
            package_dimensions = {}
        if weight is None:
            weight = {}
        if shipping_service_options is None:
            shipping_service_options = {}
        if label_customization is None:
            label_customization = {}