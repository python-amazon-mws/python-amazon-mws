# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import hashlib
import hmac
import re
from time import gmtime, strftime

import datetime
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


__all__ = [
    'Feeds',
    'Inventory',
    'MWSError',
    'Reports',
    'Orders',
    'Products',
    'Recommendations',
    'Sellers',
    'InboundShipments',
]

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


def calc_md5(string):
    """Calculates the MD5 encryption for the given string
    """
    md = hashlib.md5()
    md.update(string)
    return base64.b64encode(md.digest()).strip(b'\n')


def remove_empty(d):
    """Helper function that removes all keys from a dictionary (d), that have an empty value.

    Args:
        d (dict)

    Return:
        dict
    """
    return {k: v for k, v in d.items() if v}


def remove_namespace(xml):
    regex = re.compile(' xmlns(:ns2)?="[^"]+"|(ns2:)|(xml:)')
    return regex.sub('', xml)


class DictWrapper(object):
    def __init__(self, xml, rootkey=None):
        self.original = xml
        self._rootkey = rootkey
        self._mydict = utils.xml2dict().fromstring(remove_namespace(xml))
        self._response_dict = self._mydict.get(list(self._mydict.keys())[0],
                                               self._mydict)

    @property
    def parsed(self):
        if self._rootkey:
            return self._response_dict.get(self._rootkey)
        else:
            return self._response_dict


class DataWrapper(object):
    """
        Text wrapper in charge of validating the hash sent by Amazon.
    """
    def __init__(self, data, header):
        self.original = data
        if 'content-md5' in header:
            hash_ = calc_md5(self.original)
            if header['content-md5'].encode() != hash_:
                raise MWSError("Wrong Contentlength, maybe amazon error...")

    @property
    def parsed(self):
        return self.original


class MWS(object):
    """ Base Amazon API class """

    # This is used to post/get to the different uris used by amazon per api
    # ie. /Orders/2011-01-01
    # All subclasses must define their own URI only if needed
    URI = "/"

    # The API version varies in most amazon APIs
    VERSION = "2009-01-01"

    # There seem to be some xml namespace issues. therefore every api subclass
    # is recommended to define its namespace, so that it can be referenced
    # like so AmazonAPISubclass.NS.
    # For more information see http://stackoverflow.com/a/8719461/389453
    NS = ''

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

    def __init__(self, access_key, secret_key, account_id, region='US', domain='', uri="", version="", auth_token="",
                 proxy=None):
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

    def make_request(self, extra_data, method="GET", **kwargs):
        """Make request to Amazon MWS API with these parameters
        """

        # Remove all keys with an empty value because
        # Amazon's MWS does not allow such a thing.
        extra_data = remove_empty(extra_data)

        # convert all Python date/time objects to isoformat
        for key, value in extra_data.items():
            if isinstance(value, (datetime.datetime, datetime.date)):
                extra_data[key] = value.isoformat()

        params = {
            'AWSAccessKeyId': self.access_key,
            self.ACCOUNT_TYPE: self.account_id,
            'SignatureVersion': '2',
            'Timestamp': self.get_timestamp(),
            'Version': self.version,
            'SignatureMethod': 'HmacSHA256',
        }
        if self.auth_token:
            params['MWSAuthToken'] = self.auth_token
        proxies = self.get_proxies()
        params.update(extra_data)
        request_description = '&'.join(['%s=%s' % (k, quote(params[k], safe='-_.~')) for k in sorted(params)])
        signature = self.calc_signature(method, request_description)
        url = '%s%s?%s&Signature=%s' % (self.domain, self.uri, request_description, quote(signature))
        headers = {'User-Agent': 'python-amazon-mws/0.0.1 (Language=Python)'}
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

        except HTTPError as e:
            error = MWSError(str(e.response.text))
            error.response = e.response
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

    def calc_signature(self, method, request_description):
        """Calculate MWS signature to interface with Amazon

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

    def get_timestamp(self):
        """
            Returns the current timestamp in proper format.
        """
        return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

    def enumerate_param(self, param, values):
        """
            Builds a dictionary of an enumerated parameter.
            Takes any iterable and returns a dictionary.
            ie.
            enumerate_param('MarketplaceIdList.Id', (123, 345, 4343))
            returns
            {
                MarketplaceIdList.Id.1: 123,
                MarketplaceIdList.Id.2: 345,
                MarketplaceIdList.Id.3: 4343
            }
        """
        params = {}
        if values is not None:
            if not param.endswith('.'):
                param = "%s." % param
            for num, value in enumerate(values):
                params['%s%d' % (param, (num + 1))] = value
        return params


class Feeds(MWS):
    """ Amazon MWS Feeds API """

    ACCOUNT_TYPE = "Merchant"

    def submit_feed(self, feed, feed_type, marketplaceids=None,
                    content_type="text/xml", purge='false'):
        """
        Uploads a feed ( xml or .tsv ) to the seller's inventory.
        Can be used for creating/updating products on Amazon.
        """
        data = dict(Action='SubmitFeed',
                    FeedType=feed_type,
                    PurgeAndReplace=purge)
        data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        md = calc_md5(feed)
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md, 'Content-Type': content_type})

    def get_feed_submission_list(self, feedids=None, max_count=None, feedtypes=None,
                                 processingstatuses=None, fromdate=None, todate=None):
        """
        Returns a list of all feed submissions submitted in the previous 90 days.
        That match the query parameters.
        """

        data = dict(Action='GetFeedSubmissionList',
                    MaxCount=max_count,
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate,)
        data.update(self.enumerate_param('FeedSubmissionIdList.Id', feedids))
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(self.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_submission_list_by_next_token(self, token):
        data = dict(Action='GetFeedSubmissionListByNextToken', NextToken=token)
        return self.make_request(data)

    def get_feed_submission_count(self, feedtypes=None, processingstatuses=None, fromdate=None, todate=None):
        data = dict(Action='GetFeedSubmissionCount',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(self.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def cancel_feed_submissions(self, feedids=None, feedtypes=None, fromdate=None, todate=None):
        data = dict(Action='CancelFeedSubmissions',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(self.enumerate_param('FeedSubmissionIdList.Id.', feedids))
        data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        return self.make_request(data)

    def get_feed_submission_result(self, feedid):
        data = dict(Action='GetFeedSubmissionResult', FeedSubmissionId=feedid)
        return self.make_request(data, rootkey='Message')


class Reports(MWS):
    """ Amazon MWS Reports API """

    ACCOUNT_TYPE = "Merchant"

    # * REPORTS * #

    def get_report(self, report_id):
        data = dict(Action='GetReport', ReportId=report_id)
        return self.make_request(data)

    def get_report_count(self, report_types=(), acknowledged=None, fromdate=None, todate=None):
        data = dict(Action='GetReportCount',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate)
        data.update(self.enumerate_param('ReportTypeList.Type.', report_types))
        return self.make_request(data)

    def get_report_list(self, requestids=(), max_count=None, types=(), acknowledged=None,
                        fromdate=None, todate=None):
        data = dict(Action='GetReportList',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate,
                    MaxCount=max_count)
        data.update(self.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    def get_report_list_by_next_token(self, token):
        data = dict(Action='GetReportListByNextToken', NextToken=token)
        return self.make_request(data)

    def get_report_request_count(self, report_types=(), processingstatuses=(), fromdate=None, todate=None):
        data = dict(Action='GetReportRequestCount',
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(self.enumerate_param('ReportTypeList.Type.', report_types))
        data.update(self.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_report_request_list(self, requestids=(), types=(), processingstatuses=(),
                                max_count=None, fromdate=None, todate=None):
        data = dict(Action='GetReportRequestList',
                    MaxCount=max_count,
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(self.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        data.update(self.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_report_request_list_by_next_token(self, token):
        data = dict(Action='GetReportRequestListByNextToken', NextToken=token)
        return self.make_request(data)

    def request_report(self, report_type, start_date=None, end_date=None, marketplaceids=()):
        data = dict(Action='RequestReport',
                    ReportType=report_type,
                    StartDate=start_date,
                    EndDate=end_date)
        data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        return self.make_request(data)

    # * ReportSchedule * #

    def get_report_schedule_list(self, types=()):
        data = dict(Action='GetReportScheduleList')
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    def get_report_schedule_count(self, types=()):
        data = dict(Action='GetReportScheduleCount')
        data.update(self.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)


class Orders(MWS):
    """ Amazon Orders API """

    URI = "/Orders/2013-09-01"
    VERSION = "2013-09-01"
    NS = '{https://mws.amazonservices.com/Orders/2013-09-01}'

    def list_orders(self, marketplaceids, created_after=None, created_before=None, lastupdatedafter=None,
                    lastupdatedbefore=None, orderstatus=(), fulfillment_channels=(),
                    payment_methods=(), buyer_email=None, seller_orderid=None, max_results='100'):

        data = dict(Action='ListOrders',
                    CreatedAfter=created_after,
                    CreatedBefore=created_before,
                    LastUpdatedAfter=lastupdatedafter,
                    LastUpdatedBefore=lastupdatedbefore,
                    BuyerEmail=buyer_email,
                    SellerOrderId=seller_orderid,
                    MaxResultsPerPage=max_results,
                    )
        data.update(self.enumerate_param('OrderStatus.Status.', orderstatus))
        data.update(self.enumerate_param('MarketplaceId.Id.', marketplaceids))
        data.update(self.enumerate_param('FulfillmentChannel.Channel.', fulfillment_channels))
        data.update(self.enumerate_param('PaymentMethod.Method.', payment_methods))
        return self.make_request(data)

    def list_orders_by_next_token(self, token):
        data = dict(Action='ListOrdersByNextToken', NextToken=token)
        return self.make_request(data)

    def get_order(self, amazon_order_ids):
        data = dict(Action='GetOrder')
        data.update(self.enumerate_param('AmazonOrderId.Id.', amazon_order_ids))
        return self.make_request(data)

    def list_order_items(self, amazon_order_id):
        data = dict(Action='ListOrderItems', AmazonOrderId=amazon_order_id)
        return self.make_request(data)

    def list_order_items_by_next_token(self, token):
        data = dict(Action='ListOrderItemsByNextToken', NextToken=token)
        return self.make_request(data)


class Products(MWS):
    """ Amazon MWS Products API """

    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NS = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'

    def list_matching_products(self, marketplaceid, query, contextid=None):
        """ Returns a list of products and their attributes, ordered by
            relevancy, based on a search query that you specify.
            Your search query can be a phrase that describes the product
            or it can be a product identifier such as a UPC, EAN, ISBN, or JAN.
        """
        data = dict(Action='ListMatchingProducts',
                    MarketplaceId=marketplaceid,
                    Query=query,
                    QueryContextId=contextid)
        return self.make_request(data)

    def get_matching_product(self, marketplaceid, asins):
        """ Returns a list of products and their attributes, based on a list of
            ASIN values that you specify.
        """
        data = dict(Action='GetMatchingProduct', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_matching_product_for_id(self, marketplaceid, type, ids):
        """ Returns a list of products and their attributes, based on a list of
            product identifier values (ASIN, SellerSKU, UPC, EAN, ISBN, GCID  and JAN)
            The identifier type is case sensitive.
            Added in Fourth Release, API version 2011-10-01
        """
        data = dict(Action='GetMatchingProductForId',
                    MarketplaceId=marketplaceid,
                    IdType=type)
        data.update(self.enumerate_param('IdList.Id.', ids))
        return self.make_request(data)

    def get_competitive_pricing_for_sku(self, marketplaceid, skus):
        """ Returns the current competitive pricing of a product,
            based on the SellerSKU and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForSKU', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_competitive_pricing_for_asin(self, marketplaceid, asins):
        """ Returns the current competitive pricing of a product,
            based on the ASIN and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForASIN', MarketplaceId=marketplaceid)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_lowest_offer_listings_for_sku(self, marketplaceid, skus, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForSKU',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_lowest_offer_listings_for_asin(self, marketplaceid, asins, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_lowest_priced_offers_for_sku(self, marketplaceid, sku, condition="New", excludeme="False"):
        data = dict(Action='GetLowestPricedOffersForSKU',
                    MarketplaceId=marketplaceid,
                    SellerSKU=sku,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        return self.make_request(data)

    def get_lowest_priced_offers_for_asin(self, marketplaceid, asin, condition="New", excludeme="False"):
        data = dict(Action='GetLowestPricedOffersForASIN',
                    MarketplaceId=marketplaceid,
                    ASIN=asin,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        return self.make_request(data)

    def get_product_categories_for_sku(self, marketplaceid, sku):
        data = dict(Action='GetProductCategoriesForSKU',
                    MarketplaceId=marketplaceid,
                    SellerSKU=sku)
        return self.make_request(data)

    def get_product_categories_for_asin(self, marketplaceid, asin):
        data = dict(Action='GetProductCategoriesForASIN',
                    MarketplaceId=marketplaceid,
                    ASIN=asin)
        return self.make_request(data)

    def get_my_price_for_sku(self, marketplaceid, skus, condition=None):
        data = dict(Action='GetMyPriceForSKU',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition)
        data.update(self.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_my_price_for_asin(self, marketplaceid, asins, condition=None):
        data = dict(Action='GetMyPriceForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition)
        data.update(self.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)


class Sellers(MWS):
    """ Amazon MWS Sellers API """

    URI = '/Sellers/2011-07-01'
    VERSION = '2011-07-01'
    NS = '{http://mws.amazonservices.com/schema/Sellers/2011-07-01}'

    def list_marketplace_participations(self):
        """
            Returns a list of marketplaces a seller can participate in and
            a list of participations that include seller-specific information in that marketplace.
            The operation returns only those marketplaces where the seller's account is in an active state.
        """

        data = dict(Action='ListMarketplaceParticipations')
        return self.make_request(data)

    def list_marketplace_participations_by_next_token(self, token):
        """
            Takes a "NextToken" and returns the same information as "list_marketplace_participations".
            Based on the "NextToken".
        """
        data = dict(Action='ListMarketplaceParticipations', NextToken=token)
        return self.make_request(data)


# * Fulfillment APIs * #

class InboundShipments(MWS):
    """
    Amazon MWS FulfillmentInboundShipment API
    """
    URI = "/FulfillmentInboundShipment/2010-10-01"
    VERSION = '2010-10-01'
    NAMESPACE = '{http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/}'
    NEXT_TOKEN_OPERATIONS = [
        'ListInboundShipments',
        'ListInboundShipmentItems',
    ]
    SHIPMENT_STATUSES = ['WORKING', 'SHIPPED', 'CANCELLED']
    DEFAULT_SHIP_STATUS = 'WORKING'
    LABEL_PREFERENCES = ['SELLER_LABEL',
                         'AMAZON_LABEL_ONLY',
                         'AMAZON_LABEL_PREFERRED']

    def __init__(self, *args, **kwargs):
        """
        Allow the addition of a from_address dict during object initialization.
        kwarg "from_address" is caught and popped here,
        then calls set_ship_from_address.
        If empty or left out, empty dict is set by default.
        """
        self.from_address = {}
        addr = kwargs.pop('from_address', None)
        if addr is not None:
            self.from_address = self.set_ship_from_address(addr)
        super(InboundShipments, self).__init__(*args, **kwargs)

    def set_ship_from_address(self, address):
        """
        Verifies the structure of an address dictionary.
        Once verified against the KEY_CONFIG, saves a parsed version
        of that dictionary, ready to send to requests.
        """
        # Clear existing
        self.from_address = None

        if not address:
            raise MWSError('Missing required `address` dict.')
        if not isinstance(address, dict):
            raise MWSError("`address` must be a dict")

        key_config = [
            # Tuples composed of:
            # (input_key, output_key, is_required, default_value)
            ('name', 'Name', True, None),
            ('address_1', 'AddressLine1', True, None),
            ('address_2', 'AddressLine2', False, None),
            ('city', 'City', True, None),
            ('district_or_county', 'DistrictOrCounty', False, None),
            ('state_or_province', 'StateOrProvinceCode', False, None),
            ('postal_code', 'PostalCode', False, None),
            ('country', 'CountryCode', False, 'US'),
        ]

        # Check if all REQUIRED keys in address exist:
        if not all(k in address for k in
                   [c[0] for c in key_config if c[2]]):
            # Required parts of address missing
            raise MWSError((
                "`address` dict missing required keys: {required}."
                "\n- Optional keys: {optional}."
            ).format(
                required=", ".join([c[0] for c in key_config if c[2]]),
                optional=", ".join([c[0] for c in key_config if not c[2]]),
            ))

        # Passed tests. Assign values
        addr = {'ShipFromAddress.{}'.format(c[1]): address.get(c[0], c[3])
                for c in key_config}
        self.from_address = addr

    def _parse_item_args(self, item_args, operation):
        """
        Parses item arguments sent to create_inbound_shipment_plan, create_inbound_shipment,
        and update_inbound_shipment methods.

        `item_args` is expected as an iterable containing dicts.
        Each dict should have the following keys:
          For `create_inbound_shipment_plan`:
            REQUIRED: 'sku', 'quantity'
            OPTIONAL: 'quantity_in_case', 'asin', 'condition'
          Other operations:
            REQUIRED: 'sku', 'quantity'
            OPTIONAL: 'quantity_in_case'
        If a required key is missing, throws MWSError.
        All extra keys are ignored.

        Keys (above) are converted to the appropriate MWS key according to `key_config` (below)
        based on the particular operation required.
        """
        if not item_args:
            raise MWSError("One or more `item` dict arguments required.")

        if operation == 'CreateInboundShipmentPlan':
            # `key_config` composed of list of tuples, each tuple compose of:
            # (input_key, output_key, is_required, default_value)
            key_config = [
                ('sku', 'SellerSKU', True, None),
                ('quantity', 'Quantity', True, None),
                ('quantity_in_case', 'QuantityInCase', False, None),
                ('asin', 'ASIN', False, None),
                ('condition', 'Condition', False, None),
            ]
            # The expected MWS key for quantity is different for this operation.
            # This ensures we use the right key later on.
            quantity_key = 'Quantity'
        else:
            key_config = [
                ('sku', 'SellerSKU', True, None),
                ('quantity', 'QuantityShipped', True, None),
                ('quantity_in_case', 'QuantityInCase', False, None),
            ]
            quantity_key = 'QuantityShipped'

        items = []
        for item in item_args:
            if not isinstance(item, dict):
                raise MWSError("`item` argument must be a dict.")
            if not all(k in item for k in
                       [c[0] for c in key_config if c[2]]):
                # Required keys of an item line missing
                raise MWSError((
                    "`item` dict missing required keys: {required}."
                    "\n- Optional keys: {optional}."
                ).format(
                    required=', '.join([c[0] for c in key_config if c[2]]),
                    optional=', '.join([c[0] for c in key_config if not c[2]]),
                ))

            # Get data from the item.
            # Convert to str if present, or leave as None if missing
            quantity = item.get('quantity')
            if quantity is not None:
                quantity = str(quantity)

            quantity_in_case = item.get('quantity_in_case')
            if quantity_in_case is not None:
                quantity_in_case = str(quantity_in_case)

            item_dict = {
                'SellerSKU': item.get('sku'),
                quantity_key: quantity,
                'QuantityInCase': quantity_in_case,
            }
            item_dict.update({
                c[1]: item.get(c[0], c[3])
                for c in key_config
                if c[0] not in ['sku', 'quantity', 'quantity_in_case']
            })
            items.append(item_dict)

        return items

    def create_inbound_shipment_plan(self, items, country_code='US',
                                     subdivision_code='', label_preference=''):
        """
        Returns one or more inbound shipment plans, which provide the
        information you need to create inbound shipments.

        At least one dictionary must be passed as `args`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'asin', 'condition', 'quantity_in_case'

        'from_address' is required. Call 'set_ship_from_address' first before
        using this operation.
        """
        if not items:
            raise MWSError("One or more `item` dict arguments required.")
        subdivision_code = subdivision_code or None
        label_preference = label_preference or None

        items = self._parse_item_args(items, 'CreateInboundShipmentPlan')
        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))

        data = dict(
            Action='CreateInboundShipmentPlan',
            ShipToCountryCode=country_code,
            ShipToCountrySubdivisionCode=subdivision_code,
            LabelPrepPreference=label_preference,
        )
        data.update(self.from_address)
        data.update(utils.enumerate_keyed_param(
            'InboundShipmentPlanRequestItems.member', items,
        ))
        return self.make_request(data, method="POST")

    def create_inbound_shipment(self, shipment_id, shipment_name,
                                destination, items, shipment_status='',
                                label_preference='', case_required=False,
                                box_contents_source=None):
        """
        Creates an inbound shipment to Amazon's fulfillment network.

        At least one dictionary must be passed as `items`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'quantity_in_case'

        'from_address' is required. Call 'set_ship_from_address' first before
        using this operation.
        """
        assert isinstance(shipment_id, str), "`shipment_id` must be a string."
        assert isinstance(shipment_name, str), "`shipment_name` must be a string."
        assert isinstance(destination, str), "`destination` must be a string."

        if not items:
            raise MWSError("One or more `item` dict arguments required.")

        items = self._parse_item_args(items, 'CreateInboundShipment')

        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))
        from_address = self.from_address
        from_address = {'InboundShipmentHeader.{}'.format(k): v
                        for k, v in from_address.items()}

        if shipment_status not in self.SHIPMENT_STATUSES:
            # Status is required for `create` request.
            # Set it to default.
            shipment_status = self.DEFAULT_SHIP_STATUS

        if label_preference not in self.LABEL_PREFERENCES:
            # Label preference not required. Set to None
            label_preference = None

        # Explict True/False for case_required,
        # written as the strings MWS expects.
        case_required = 'true' if case_required else 'false'

        data = {
            'Action': 'CreateInboundShipment',
            'ShipmentId': shipment_id,
            'InboundShipmentHeader.ShipmentName': shipment_name,
            'InboundShipmentHeader.DestinationFulfillmentCenterId': destination,
            'InboundShipmentHeader.LabelPrepPreference': label_preference,
            'InboundShipmentHeader.AreCasesRequired': case_required,
            'InboundShipmentHeader.ShipmentStatus': shipment_status,
            'InboundShipmentHeader.IntendedBoxContentsSource': box_contents_source,
        }
        data.update(from_address)
        data.update(utils.enumerate_keyed_param(
            'InboundShipmentItems.member', items,
        ))
        return self.make_request(data, method="POST")

    def update_inbound_shipment(self, shipment_id, shipment_name,
                                destination, items=None, shipment_status='',
                                label_preference='', case_required=False,
                                box_contents_source=None):
        """
        Updates an existing inbound shipment in Amazon FBA.
        'from_address' is required. Call 'set_ship_from_address' first before
        using this operation.
        """
        # Assert these are strings, error out if not.
        assert isinstance(shipment_id, str), "`shipment_id` must be a string."
        assert isinstance(shipment_name, str), "`shipment_name` must be a string."
        assert isinstance(destination, str), "`destination` must be a string."

        # Parse item args
        if items:
            items = self._parse_item_args(items, 'UpdateInboundShipment')
        else:
            items = None

        # Raise exception if no from_address has been set prior to calling
        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))
        # Assemble the from_address using operation-specific header
        from_address = self.from_address
        from_address = {'InboundShipmentHeader.{}'.format(k): v
                        for k, v in from_address.items()}

        if shipment_status not in self.SHIPMENT_STATUSES:
            # Passed shipment status is an invalid choice.
            # Remove it from this request by setting it to None.
            shipment_status = None

        if label_preference not in self.LABEL_PREFERENCES:
            # Passed label preference is an invalid choice.
            # Remove it from this request by setting it to None.
            label_preference = None

        case_required = 'true' if case_required else 'false'

        data = {
            'Action': 'UpdateInboundShipment',
            'ShipmentId': shipment_id,
            'InboundShipmentHeader.ShipmentName': shipment_name,
            'InboundShipmentHeader.DestinationFulfillmentCenterId': destination,
            'InboundShipmentHeader.LabelPrepPreference': label_preference,
            'InboundShipmentHeader.AreCasesRequired': case_required,
            'InboundShipmentHeader.ShipmentStatus': shipment_status,
            'InboundShipmentHeader.IntendedBoxContentsSource': box_contents_source,
        }
        data.update(from_address)
        if items:
            # Update with an items paramater only if they exist.
            data.update(utils.enumerate_keyed_param(
                'InboundShipmentItems.member', items,
            ))
        return self.make_request(data, method="POST")
    
    def get_prep_instructions_for_sku(self, skus=None, country_code=None):
        """
        Returns labeling requirements and item preparation instructions
        to help you prepare items for an inbound shipment.
        """
        country_code = country_code or 'US'
        skus = skus or []

        # 'skus' should be a unique list, or there may be an error returned.
        skus = utils.unique_list_order_preserved(skus)

        data = dict(
            Action='GetPrepInstructionsForSKU',
            ShipToCountryCode=country_code,
        )
        data.update(utils.enumerate_params({
            'SellerSKUList.ID.': skus,
        }))
        return self.make_request(data, method="POST")

    def get_prep_instructions_for_asin(self, asins=None, country_code=None):
        """
        Returns item preparation instructions to help with
        item sourcing decisions.
        """
        country_code = country_code or 'US'
        asins = asins or []

        # 'asins' should be a unique list, or there may be an error returned.
        asins = utils.unique_list_order_preserved(asins)

        data = dict(
            Action='GetPrepInstructionsForASIN',
            ShipToCountryCode=country_code,
        )
        data.update(utils.enumerate_params({
            'ASINList.ID.': asins,
        }))
        return self.make_request(data, method="POST")

    def get_package_labels(self, shipment_id, num_packages, page_type=None):
        """
        Returns PDF document data for printing package labels for
        an inbound shipment.
        """
        data = dict(
            Action='GetPackageLabels',
            ShipmentId=shipment_id,
            PageType=page_type,
            NumberOfPackages=str(num_packages),
        )
        return self.make_request(data, method="POST")
    
    def get_transport_content(self, shipment_id):
        """
        Returns current transportation information about an
        inbound shipment.
        """
        data = dict(
            Action='GetTransportContent',
            ShipmentId=shipment_id
        )
        return self.make_request(data, method="POST")
    
    def estimate_transport_request(self, shipment_id):
        """
        Requests an estimate of the shipping cost for an inbound shipment.
        """
        data = dict(
            Action='EstimateTransportRequest',
            ShipmentId=shipment_id,
        )
        return self.make_request(data, method="POST")

    def void_transport_request(self, shipment_id):
        """
        Voids a previously-confirmed request to ship your inbound shipment
        using an Amazon-partnered carrier.
        """
        data = dict(
            Action='VoidTransportRequest',
            ShipmentId=shipment_id
        )
        return self.make_request(data, method="POST")
    
    def get_bill_of_lading(self, shipment_id):
        """
        Returns PDF document data for printing a bill of lading
        for an inbound shipment.
        """
        data = dict(
            Action='GetBillOfLading',
            ShipmentId=shipment_id,
        )
        return self.make_request(data, "POST")
    
    @utils.next_token_action('ListInboundShipments')
    def list_inbound_shipments(self, shipment_ids=None, shipment_statuses=None,
                               last_updated_after=None, last_updated_before=None,):
        """
        Returns list of shipments based on statuses, IDs, and/or
        before/after datetimes.
        """
        last_updated_after = utils.dt_iso_or_none(last_updated_after)
        last_updated_before = utils.dt_iso_or_none(last_updated_before)

        data = dict(
            Action='ListInboundShipments',
            LastUpdatedAfter=last_updated_after,
            LastUpdatedBefore=last_updated_before,
        )
        data.update(utils.enumerate_params({
            'ShipmentStatusList.member.': shipment_statuses,
            'ShipmentIdList.member.': shipment_ids,
        }))
        return self.make_request(data, method="POST")

    @utils.next_token_action('ListInboundShipmentItems')
    def list_inbound_shipment_items(self, shipment_id=None, last_updated_after=None,
                                    last_updated_before=None,):
        """
        Returns list of items within inbound shipments and/or
        before/after datetimes.
        """
        last_updated_after = utils.dt_iso_or_none(last_updated_after)
        last_updated_before = utils.dt_iso_or_none(last_updated_before)

        data = dict(
            Action='ListInboundShipmentItems',
            ShipmentId=shipment_id,
            LastUpdatedAfter=last_updated_after,
            LastUpdatedBefore=last_updated_before,
        )
        return self.make_request(data, method="POST")

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


class Inventory(MWS):
    """ Amazon MWS Inventory Fulfillment API """

    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'
    NS = "{http://mws.amazonaws.com/FulfillmentInventory/2010-10-01}"

    def list_inventory_supply(self, skus=(), datetime=None, response_group='Basic'):
        """ Returns information on available inventory """

        data = dict(Action='ListInventorySupply',
                    QueryStartDateTime=datetime,
                    ResponseGroup=response_group,
                    )
        data.update(self.enumerate_param('SellerSkus.member.', skus))
        return self.make_request(data, "POST")

    def list_inventory_supply_by_next_token(self, token):
        data = dict(Action='ListInventorySupplyByNextToken', NextToken=token)
        return self.make_request(data, "POST")


class OutboundShipments(MWS):
    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    # To be completed


class Recommendations(MWS):

    """ Amazon MWS Recommendations API """

    URI = '/Recommendations/2013-04-01'
    VERSION = '2013-04-01'
    NS = "{https://mws.amazonservices.com/Recommendations/2013-04-01}"

    def get_last_updated_time_for_recommendations(self, marketplaceid):
        """
        Checks whether there are active recommendations for each category for the given marketplace, and if there are,
        returns the time when recommendations were last updated for each category.
        """

        data = dict(Action='GetLastUpdatedTimeForRecommendations',
                    MarketplaceId=marketplaceid)
        return self.make_request(data, "POST")

    def list_recommendations(self, marketplaceid, recommendationcategory=None):
        """
        Returns your active recommendations for a specific category or for all categories for a specific marketplace.
        """

        data = dict(Action="ListRecommendations",
                    MarketplaceId=marketplaceid,
                    RecommendationCategory=recommendationcategory)
        return self.make_request(data, "POST")

    def list_recommendations_by_next_token(self, token):
        """
        Returns the next page of recommendations using the NextToken parameter.
        """

        data = dict(Action="ListRecommendationsByNextToken",
                    NextToken=token)
        return self.make_request(data, "POST")
