# -*- coding: utf-8 -*-
from __future__ import absolute_import

from time import gmtime, strftime
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


__all__ = [
    'Feeds',
    'Inventory',
    'InboundShipments',
    'MWSError',
    'Reports',
    'Orders',
    'Products',
    'Recommendations',
    'Sellers',
    'Finances',
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
    "AU": "https://mws.amazonservices.com.au",  # A39IBJ37TRP1C6
    "BR": "https://mws.amazonservices.com",  # A2Q3Y263D00KWC
}


class MWSError(Exception):
    """
    Main MWS Exception class
    """
    # Allows quick access to the response object.
    # Do not rely on this attribute, always check if its not None.
    response = None


def calc_md5(string):
    """
    Calculates the MD5 encryption for the given string
    """
    md5_hash = hashlib.md5()
    md5_hash.update(string)
    return base64.b64encode(md5_hash.digest()).strip(b'\n')


def calc_request_description(params):
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
            hash_ = calc_md5(self.original)
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

    def get_params(self):
        """
        Get the parameters required in all MWS requests
        """
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

        params = self.get_params()
        params.update(extra_data)
        request_description = calc_request_description(params)
        signature = self.calc_signature(method, request_description)
        url = "{domain}{uri}?{description}&Signature={signature}".format(
            domain=self.domain,
            uri=self.uri,
            description=request_description,
            signature=quote(signature),
        )
        headers = {'User-Agent': 'python-amazon-mws/0.8.6 (Language=Python)'}
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

        except HTTPError as e:
            error = MWSError(str(e.response.text))
            error.response = e.response
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

    def get_timestamp(self):
        """
        Returns the current timestamp in proper format.
        """
        return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

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


class Feeds(MWS):
    """
    Amazon MWS Feeds API
    """
    ACCOUNT_TYPE = "Merchant"

    NEXT_TOKEN_OPERATIONS = [
        'GetFeedSubmissionList',
    ]

    def submit_feed(self, feed, feed_type, marketplaceids=None,
                    content_type="text/xml", purge='false'):
        """
        Uploads a feed ( xml or .tsv ) to the seller's inventory.
        Can be used for creating/updating products on Amazon.
        """
        data = dict(Action='SubmitFeed',
                    FeedType=feed_type,
                    PurgeAndReplace=purge)
        data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        md = calc_md5(feed)
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md, 'Content-Type': content_type})

    @utils.next_token_action('GetFeedSubmissionList')
    def get_feed_submission_list(self, feedids=None, max_count=None, feedtypes=None,
                                 processingstatuses=None, fromdate=None, todate=None,
                                 next_token=None):
        """
        Returns a list of all feed submissions submitted in the previous 90 days.
        That match the query parameters.
        """

        data = dict(Action='GetFeedSubmissionList',
                    MaxCount=max_count,
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate,)
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id', feedids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_submission_list_by_next_token(self, token):
        """
        Deprecated.
        Use `get_feed_submission_list(next_token=token)` instead.
        """
        # data = dict(Action='GetFeedSubmissionListByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `get_feed_submission_list(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.get_feed_submission_list(next_token=token)

    def get_feed_submission_count(self, feedtypes=None, processingstatuses=None, fromdate=None, todate=None):
        data = dict(Action='GetFeedSubmissionCount',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def cancel_feed_submissions(self, feedids=None, feedtypes=None, fromdate=None, todate=None):
        data = dict(Action='CancelFeedSubmissions',
                    SubmittedFromDate=fromdate,
                    SubmittedToDate=todate)
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id.', feedids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feedtypes))
        return self.make_request(data)

    def get_feed_submission_result(self, feedid):
        data = dict(Action='GetFeedSubmissionResult', FeedSubmissionId=feedid)
        return self.make_request(data, rootkey='Message')


class Reports(MWS):
    """
    Amazon MWS Reports API
    """
    ACCOUNT_TYPE = "Merchant"
    NEXT_TOKEN_OPERATIONS = [
        'GetReportRequestList',
        'GetReportList',
        'GetReportScheduleList',
    ]

    # * REPORTS * #

    def get_report(self, report_id):
        data = dict(Action='GetReport', ReportId=report_id)
        return self.make_request(data)

    def get_report_count(self, report_types=(), acknowledged=None, fromdate=None, todate=None):
        data = dict(Action='GetReportCount',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate)
        data.update(utils.enumerate_param('ReportTypeList.Type.', report_types))
        return self.make_request(data)

    @utils.next_token_action('GetReportList')
    def get_report_list(self, requestids=(), max_count=None, types=(), acknowledged=None,
                        fromdate=None, todate=None, next_token=None):
        data = dict(Action='GetReportList',
                    Acknowledged=acknowledged,
                    AvailableFromDate=fromdate,
                    AvailableToDate=todate,
                    MaxCount=max_count)
        data.update(utils.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    def get_report_list_by_next_token(self, token):
        """
        Deprecated.
        Use `get_report_list(next_token=token)` instead.
        """
        # data = dict(Action='GetReportListByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `get_report_list(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.get_report_list(next_token=token)

    def get_report_request_count(self, report_types=(), processingstatuses=(),
                                 fromdate=None, todate=None):
        data = dict(Action='GetReportRequestCount',
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(utils.enumerate_param('ReportTypeList.Type.', report_types))
        data.update(utils.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    @utils.next_token_action('GetReportRequestList')
    def get_report_request_list(self, requestids=(), types=(), processingstatuses=(),
                                max_count=None, fromdate=None, todate=None, next_token=None):
        data = dict(Action='GetReportRequestList',
                    MaxCount=max_count,
                    RequestedFromDate=fromdate,
                    RequestedToDate=todate)
        data.update(utils.enumerate_param('ReportRequestIdList.Id.', requestids))
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        data.update(utils.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        return self.make_request(data)

    def get_report_request_list_by_next_token(self, token):
        """
        Deprecated.
        Use `get_report_request_list(next_token=token)` instead.
        """
        # data = dict(Action='GetReportRequestListByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `get_report_request_list(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.get_report_request_list(next_token=token)

    def request_report(self, report_type, start_date=None, end_date=None, marketplaceids=()):
        data = dict(Action='RequestReport',
                    ReportType=report_type,
                    StartDate=start_date,
                    EndDate=end_date)
        data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        return self.make_request(data)

    # * ReportSchedule * #

    def get_report_schedule_list(self, types=()):
        data = dict(Action='GetReportScheduleList')
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)

    def get_report_schedule_count(self, types=()):
        data = dict(Action='GetReportScheduleCount')
        data.update(utils.enumerate_param('ReportTypeList.Type.', types))
        return self.make_request(data)


class Orders(MWS):
    """
    Amazon Orders API
    """
    URI = "/Orders/2013-09-01"
    VERSION = "2013-09-01"
    NAMESPACE = '{https://mws.amazonservices.com/Orders/2013-09-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListOrders',
        'ListOrderItems',
    ]

    @utils.next_token_action('ListOrders')
    def list_orders(self, marketplaceids=None, created_after=None, created_before=None,
                    lastupdatedafter=None, lastupdatedbefore=None, orderstatus=(),
                    fulfillment_channels=(), payment_methods=(), buyer_email=None,
                    seller_orderid=None, max_results='100', next_token=None):

        data = dict(Action='ListOrders',
                    CreatedAfter=created_after,
                    CreatedBefore=created_before,
                    LastUpdatedAfter=lastupdatedafter,
                    LastUpdatedBefore=lastupdatedbefore,
                    BuyerEmail=buyer_email,
                    SellerOrderId=seller_orderid,
                    MaxResultsPerPage=max_results,
                    )
        data.update(utils.enumerate_param('OrderStatus.Status.', orderstatus))
        data.update(utils.enumerate_param('MarketplaceId.Id.', marketplaceids))
        data.update(utils.enumerate_param('FulfillmentChannel.Channel.', fulfillment_channels))
        data.update(utils.enumerate_param('PaymentMethod.Method.', payment_methods))
        return self.make_request(data)

    def list_orders_by_next_token(self, token):
        """
        Deprecated.
        Use `list_orders(next_token=token)` instead.
        """
        # data = dict(Action='ListOrdersByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_orders(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_orders(next_token=token)

    def get_order(self, amazon_order_ids):
        data = dict(Action='GetOrder')
        data.update(utils.enumerate_param('AmazonOrderId.Id.', amazon_order_ids))
        return self.make_request(data)

    @utils.next_token_action('ListOrderItems')
    def list_order_items(self, amazon_order_id=None, next_token=None):
        data = dict(Action='ListOrderItems', AmazonOrderId=amazon_order_id)
        return self.make_request(data)

    def list_order_items_by_next_token(self, token):
        """
        Deprecated.
        Use `list_order_items(next_token=token)` instead.
        """
        # data = dict(Action='ListOrderItemsByNextToken', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_order_items(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_order_items(next_token=token)


class Products(MWS):
    """
    Amazon MWS Products API
    """
    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NAMESPACE = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'
    # NEXT_TOKEN_OPERATIONS = []

    def list_matching_products(self, marketplaceid, query, contextid=None):
        """
        Returns a list of products and their attributes, ordered by
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
        """
        Returns a list of products and their attributes, based on a list of
        ASIN values that you specify.
        """
        data = dict(Action='GetMatchingProduct', MarketplaceId=marketplaceid)
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_matching_product_for_id(self, marketplaceid, type_, ids):
        """
        Returns a list of products and their attributes, based on a list of
        product identifier values (ASIN, SellerSKU, UPC, EAN, ISBN, GCID  and JAN)
        The identifier type is case sensitive.
        Added in Fourth Release, API version 2011-10-01
        """
        data = dict(Action='GetMatchingProductForId',
                    MarketplaceId=marketplaceid,
                    IdType=type_)

        data.update(utils.enumerate_param('IdList.Id.', ids))
        return self.make_request(data)

    def get_competitive_pricing_for_sku(self, marketplaceid, skus):
        """
        Returns the current competitive pricing of a product,
        based on the SellerSKU and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForSKU', MarketplaceId=marketplaceid)
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_competitive_pricing_for_asin(self, marketplaceid, asins):
        """
        Returns the current competitive pricing of a product,
        based on the ASIN and MarketplaceId that you specify.
        """
        data = dict(Action='GetCompetitivePricingForASIN', MarketplaceId=marketplaceid)
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_lowest_offer_listings_for_sku(self, marketplaceid, skus, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForSKU',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_lowest_offer_listings_for_asin(self, marketplaceid, asins, condition="Any", excludeme="False"):
        data = dict(Action='GetLowestOfferListingsForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition,
                    ExcludeMe=excludeme)
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
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
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_my_price_for_asin(self, marketplaceid, asins, condition=None):
        data = dict(Action='GetMyPriceForASIN',
                    MarketplaceId=marketplaceid,
                    ItemCondition=condition)
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)


class Sellers(MWS):
    """
    Amazon MWS Sellers API
    """
    URI = '/Sellers/2011-07-01'
    VERSION = '2011-07-01'
    NAMESPACE = '{http://mws.amazonservices.com/schema/Sellers/2011-07-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListMarketplaceParticipations',
    ]

    @utils.next_token_action('ListMarketplaceParticipations')
    def list_marketplace_participations(self, next_token=None):
        """
        Returns a list of marketplaces a seller can participate in and
        a list of participations that include seller-specific information in that marketplace.
        The operation returns only those marketplaces where the seller's account is
        in an active state.

        Run with `next_token` kwarg to call related "ByNextToken" action.
        """
        data = dict(Action='ListMarketplaceParticipations')
        return self.make_request(data)

    def list_marketplace_participations_by_next_token(self, token):
        """
        Deprecated.
        Use `list_marketplace_participations(next_token=token)` instead.
        """
        # data = dict(Action='ListMarketplaceParticipations', NextToken=token)
        # return self.make_request(data)
        warnings.warn(
            "Use `list_marketplace_participations(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_marketplace_participations(next_token=token)


class Finances(MWS):
    """
    Amazon MWS Finances API
    """
    URI = "/Finances/2015-05-01"
    VERSION = "2015-05-01"
    NS = '{https://mws.amazonservices.com/Finances/2015-05-01}'
    NEXT_TOKEN_OPERATIONS = [
        'ListFinancialEventGroups',
        'ListFinancialEvents',
    ]

    @utils.next_token_action('ListFinancialEventGroups')
    def list_financial_event_groups(self, created_after=None, created_before=None, max_results=None, next_token=None):
        """
        Returns a list of financial event groups
        """
        data = dict(Action='ListFinancialEventGroups',
                    FinancialEventGroupStartedAfter=created_after,
                    FinancialEventGroupStartedBefore=created_before,
                    MaxResultsPerPage=max_results,
                    )
        return self.make_request(data)

    def list_financial_event_groups_by_next_token(self, token):
        """
        Deprecated.
        Use `list_financial_event_groups(next_token=token)` instead.
        """
        warnings.warn(
            "Use `list_financial_event_groups(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_financial_event_groups(next_token=token)

    @utils.next_token_action('ListFinancialEvents')
    def list_financial_events(self, financial_event_group_id=None, amazon_order_id=None, posted_after=None,
                              posted_before=None, max_results=None, next_token=None):
        """
        Returns financial events for a user-provided FinancialEventGroupId or AmazonOrderId
        """
        data = dict(Action='ListFinancialEvents',
                    FinancialEventGroupId=financial_event_group_id,
                    AmazonOrderId=amazon_order_id,
                    PostedAfter=posted_after,
                    PostedBefore=posted_before,
                    MaxResultsPerPage=max_results,
                    )
        return self.make_request(data)

    def list_financial_events_by_next_token(self, token):
        """
        Deprecated.
        Use `list_financial_events(next_token=token)` instead.
        """
        warnings.warn(
            "Use `list_financial_events(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_financial_events(next_token=token)


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
            self.set_ship_from_address(addr)
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


class Inventory(MWS):
    """
    Amazon MWS Inventory Fulfillment API
    """

    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInventory/2010-10-01}"
    NEXT_TOKEN_OPERATIONS = [
        'ListInventorySupply',
    ]

    @utils.next_token_action('ListInventorySupply')
    def list_inventory_supply(self, skus=(), datetime_=None,
                              response_group='Basic', next_token=None):
        """
        Returns information on available inventory
        """

        data = dict(Action='ListInventorySupply',
                    QueryStartDateTime=datetime_,
                    ResponseGroup=response_group,
                    )
        data.update(utils.enumerate_param('SellerSkus.member.', skus))
        return self.make_request(data, "POST")

    def list_inventory_supply_by_next_token(self, token):
        """
        Deprecated.
        Use `list_inventory_supply(next_token=token)` instead.
        """
        # data = dict(Action='ListInventorySupplyByNextToken', NextToken=token)
        # return self.make_request(data, "POST")
        warnings.warn(
            "Use `list_inventory_supply(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_inventory_supply(next_token=token)


class OutboundShipments(MWS):
    """
    Amazon MWS Fulfillment Outbound Shipments API
    """
    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NEXT_TOKEN_OPERATIONS = [
        'ListAllFulfillmentOrders',
    ]
    # TODO: Complete this class section


class Recommendations(MWS):
    """
    Amazon MWS Recommendations API
    """
    URI = '/Recommendations/2013-04-01'
    VERSION = '2013-04-01'
    NAMESPACE = "{https://mws.amazonservices.com/Recommendations/2013-04-01}"
    NEXT_TOKEN_OPERATIONS = [
        "ListRecommendations",
    ]

    def get_last_updated_time_for_recommendations(self, marketplaceid):
        """
        Checks whether there are active recommendations for each category for the given marketplace, and if there are,
        returns the time when recommendations were last updated for each category.
        """
        data = dict(Action='GetLastUpdatedTimeForRecommendations',
                    MarketplaceId=marketplaceid)
        return self.make_request(data, "POST")

    @utils.next_token_action('ListRecommendations')
    def list_recommendations(self, marketplaceid=None,
                             recommendationcategory=None, next_token=None):
        """
        Returns your active recommendations for a specific category or for all categories for a specific marketplace.
        """
        data = dict(Action="ListRecommendations",
                    MarketplaceId=marketplaceid,
                    RecommendationCategory=recommendationcategory)
        return self.make_request(data, "POST")

    def list_recommendations_by_next_token(self, token):
        """
        Deprecated.
        Use `list_recommendations(next_token=token)` instead.
        """
        # data = dict(Action="ListRecommendationsByNextToken",
        #             NextToken=token)
        # return self.make_request(data, "POST")
        warnings.warn(
            "Use `list_recommendations(next_token=token)` instead.",
            DeprecationWarning,
        )
        return self.list_recommendations(next_token=token)
