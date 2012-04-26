#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic interface to Amazon MWS
# Based on http://code.google.com/p/amazon-mws-python
#

import urllib
import hashlib
import hmac
import base64
import md5
from xml.etree.ElementTree import fromstring, ParseError
from time import strftime, gmtime

from requests import request
from requests.exceptions import RequestException


class MWSError(Exception):
    pass


class TreeWrapper(object):
    """ Small wrapper around the find and findall methods of
        the the xml.etree.ElementTree.Element class.
    """

    def __init__(self, xml, ns):
        try:
            self.etree = fromstring(xml)
        except ParseError, e:
            raise MWSError("Invalid xml, maybe amazon error...")

        self.ns = ns

    def find(self, text):
        return self.etree.find(".//" + self.ns + text)

    def findall(self, text):
        return self.etree.findall(".//" + self.ns + text)


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
    # This constant defines the exact name of the parameter Amazon expects for the specific APi
    # being used. All subclasses need to define this if they require another account type
    # like "Seller" in which case you define it like so.
    # ACCOUNT_TYPE = "SellerId"
    # Which is the name of the parameter for that specific account type.
    ACCOUNT_TYPE = "Merchant"

    def __init__(self, access_key, secret_key, account_id,
                 domain='https://mws.amazonservices.com', uri="", version=""):
        self.access_key = access_key
        self.secret_key = secret_key
        self.account_id = account_id
        self.domain = domain
        self.uri = uri or self.URI
        self.version = version or self.VERSION

    def make_request(self, extra_data, method="GET", **kwargs):
        """Make request to Amazon MWS API with these parameters
        """

        params = {
            'AWSAccessKeyId': self.access_key,
            self.ACCOUNT_TYPE: self.self.account_id,
            'SignatureVersion': '2',
            'Timestamp': self.get_timestamp(),
            'Version': self.version,
            'SignatureMethod': 'HmacSHA256',
        }
        params.update(extra_data)
        request_description = '&'.join(['%s=%s' % (k, urllib.quote(params[k], safe='-_.~').encode('utf-8')) for k in sorted(params)])
        signature = self.calc_signature(method, request_description)
        url = '%s%s?%s&Signature=%s' % (self.domain, self.uri, request_description, urllib.quote(signature))
        headers = {'User-Agent': 'python-amazon-mws/0.0.1 (Language=Python)'}
        headers.update(kwargs.get('extra_headers', {}))

        try:
            # Some might wonder as to why i don't pass the params dict as the params argument to request.
            # My answer is, here i have to get the url parsed string of params in order to sign it, so
            # if i pass the params dict as params to request, request will repeat that step because it will need
            # to convert the dict to a url parsed string, so why do it twice if i can just pass the full url :).
            response = request(method, url, data=kwargs.get('body', ''), headers=headers)
            parsed_response = TreeWrapper(response.text, self.NS)
        except RequestException, e:
            error = e.read()
            raise MWSError(error)

        # Store the response object in the parsed_response for quick access
        parsed_response.response = response
        return parsed_response

    def calc_signature(self, method, request_description):
        """Calculate MWS signature to interface with Amazon
        """
        sig_data = method + '\n' + self.domain.replace('https://', '').lower() + '\n' + self.uri + '\n' + request_description
        return base64.b64encode(hmac.new(str(self.secret_key), sig_data, hashlib.sha256).digest())

    def calc_md5(self, string):
        """Calculates the MD5 encryption for the given string
        """
        md = md5.new()
        md.update(string)
        return base64.encodestring(md.digest()).strip('\n')

    def parse_response(self, response):
        return fromstring(response)

    def get_timestamp(self):
        """
            Return current timestamp in proper format.
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

        if not param.endswith('.'):
            param = "%s." % param
        for num, value in enumerate(values):
            params['%s%d' % (param, (num + 1))] = value
        return params


class Feeds(MWS):
    """ Amazon MWS Feeds API """

    def submit_feed(self, feed, feed_type, marketplaceids=(), content_type="text/xml", purge='false'):
        """
            Uploads a feed ( xml or .tsv ) to the seller's inventory.
            Can be used for creating/updating products on amazon.
        """
        data = dict(Action='SubmitFeed', FeedType=feed_type, PurgeAndReplace=purge)
        md = self.calc_md5(feed)
        if marketplaceids:
            data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceidlist))
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md, 'Content-Type': content_type})

    def get_feed_submission_list(self, feedids=(), max_count='', feedtypes=(),
                                    processingstatuses=(), fromdate='', todate=''):
        data = dict(Action='GetFeedSubmissionList')
        if feedids:
            data.update(self.enumerate_param('FeedSubmissionIdList.Id', feedids))
        if max_count:
            data['MaxCount'] = max_count
        if feedtypes:
            data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        if processingstatuses:
            data.update(self.enumerate_param('FeedProcessingStatusList.Status.', feedtypes))
        if fromdate:
            data['SubmittedFromDate'] = fromdate
        if todate:
            data['SubmittedToDate'] = todate
        return self.make_request(data)

    def get_submission_list_by_next_token(self, token):
        data = dict(Action='GetFeedSubmissionListByNextToken', NextToken=token)
        return self.make_request(data)

    def get_feed_submission_count(self, feedtypes=(), processingstatuses=(), fromdate='', todate=''):
        data = dict(Action='GetFeedSubmissionCount')
        if feedtypes:
            data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        if processingstatuses:
            data.update(self.enumerate_param('FeedProcessingStatusList.Status.', feedtypes))
        if fromdate:
            data['SubmittedFromDate'] = fromdate
        if todate:
            data['SubmittedToDate'] = todate
        return self.make_request(data)

    def cancel_feed_submissions(self, feedids=(), feedtypes=(), fromdate='', todate=''):
        data = dict(Action='CancelFeedSubmissions')
        if feedids:
            data.update(self.enumerate_param('FeedSubmissionIdList.Id.', feedsubmissionids))
        if feedtypes:
            data.update(self.enumerate_param('FeedTypeList.Type.', feedtypes))
        if fromdate:
            data['SubmittedFromDate'] = fromdate
        if todate:
            data['SubmittedToDate'] = todate
        return self.make_request(data)

    def get_feed_submission_result(self, feedid):
        data = dict(Action='GetFeedSubmissionResult', FeedSubmissionId=feedid)
        return self.make_request(data)


class Reports(MWS):
    """ Amazon MWS Reports API """

    def request_report(self, report_type, start_date='', end_date='', marketplaceids=''):
        data = dict(Action='RequestReport', ReportType=report_type)
        if start_date:
            data['StartDate'] = start_date
        if end_date:
            data['EndDate'] = end_date
        if marketplaceids:
            data.update(self.enumerate_param('MarketplaceIdList.Id.', marketplaceids))
        return self.make_request(data)

    def get_report_request_list(self, requestids=(), types=(), processingstatuses=(), max_count='', fromdate='', todate=''):
        data = dict(Action='GetReportRequestList')
        if requestids:
            data.update(self.enumerate_param('ReportRequestIdList.Id.', requestids))
        if types:
            data.update(self.enumerate_param('ReportTypeList.Type.', types))
        if processingstatuses:
            data.update(self.enumerate_param('ReportProcessingStatusList.Status.', processingstatuses))
        if max_count:
            data['MaxCount'] = max_count
        if fromdate:
            data['RequestedFromDate'] = fromdate
        if todate:
            data['RequestedToDate'] = todate
        return self.make_request(data)

    def get_report_count(self, report_types=(), acknowledged=None, fromdate='', todate=''):
        data = dict(Action='GetReportCount')
        if report_types:
            data.update(self.enumerate_param('ReportTypeList.Type.', report_types))
        if acknowledged:
            data['Acknowledged'] = acknowledged
        if fromdate:
            data['AvailableFromDate'] = fromdate
        if todate:
            data['AvailableToDate'] = todate
        return self.make_request(data)

    def get_report(self, report_id):
        data = dict(Action='GetReport', ReportId=report_id)
        return self.make_request(data)


class Orders(MWS):
    """ Amazon Orders API """

    URI = "/Orders/2011-01-01"
    VERSION = "2011-01-01"
    NS = '{https://mws.amazonservices.com/Orders/2011-01-01}'
    ACCOUNT_TYPE = "SellerId"

    # Not ready !!!
    # def list_orders(self, marketplaceids, **kwargs):
    #     data = dict(Action='ListOrders', SellerId=self.merchant_id)
    #     for num, mid in enumerate(marketplaceids):
    #         data['MarketplaceId.Id.%d' % (num + 1)] = mid
    #     data.update(kwargs)
    #     return self.make_request(data)

    def list_orders_by_next_token(self, next_token):
        data = dict(Action='ListOrdersByNextToken', NextToken=next_token)
        return self.make_request(data)


class Inventory(MWS):
    """ Amazon MWS Fulfillment API """

    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'
    ACCOUNT_TYPE = "SellerId"

    def list_inventory_supply(self, skus=(), datetime=False, response_group='Basic'):
        """ Returns information on available inventory """
        data = dict(Action='ListInventorySupply', ResponseGroup=response_group)
        if skus:
            data.update(self.enumerate_param('SellerSkus.member.', skus))
        if datetime:
            data['QueryStartDateTime'] = datetime
        return self.make_request(data, "POST")


class Products(MWS):
    """ Amazon MWS Products API """

    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NS = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'
    ACCOUNT_TYPE = "SellerId"

    def list_matching_products(self, query, marketplaceid, contextid='All'):
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
        for num, asin in enumerate(asins):
            data['ASINList.ASIN.%d' % (num + 1)] = asin
        return self.make_request(data)

    def get_competitive_pricing_for_sku(self, marketplaceid, skus):
        """ Returns the current competitive pricing of a product,
            based on the SellerSKU and MarketplaceId that you specify.
        """
        data = dict(MarketplaceId=marketplaceid)
        for num, asin in enumerate(skus):
            data['SellerSKUList.SellerSKU.%d' % (num + 1)] = asin
        return self.make_request(data)
