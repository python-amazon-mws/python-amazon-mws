#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Basic interface to Amazon MWS
# Based on http://code.google.com/p/amazon-mws-python
#

import re
import urllib
import hashlib
import hmac
import base64
import md5
from pprint import pprint
from httplib import HTTPSConnection, HTTPException
from xml.etree.ElementTree import fromstring, ParseError
from time import strftime, gmtime



class MWSError(Exception):
    pass


class MWS(object):
    """ Base Amazon API class """

    # This is used to post/get to the different uris used by amazon per api
    # ie. /Orders/2011-01-01, all subclasses must define their own URI only if needed
    URI = "/"

    # The API version varies in most amazon APIs
    VERSION = "2009-01-01"

    # There seem to be some xml namespace issues. therefore every api subclass 
    # is recommended to define its namespace, so that it can be referenced 
    # like so AmazonAPISubclass.NS.
    # For more information see http://stackoverflow.com/a/8719461/389453
    NS = ''

    def __init__(self, access_key, secret_key, merchant_id,
                 domain='https://mws.amazonservices.com', uri="", version=""):
        self.access_key = access_key
        self.secret_key = secret_key
        self.merchant_id = merchant_id
        self.domain = domain
        self.uri = uri or self.URI
        self.version = version or self.VERSION

    def make_request(self, extra_data, method="GET", **kwargs):
        """Make request to Amazon MWS API with these parameters
        """
        conn = HTTPSConnection('mws.amazonservices.com')
        data = {
            'AWSAccessKeyId': self.access_key,
            'Merchant': self.merchant_id,
            'SignatureVersion': '2',
            'Timestamp': self.get_timestamp(),
            'Version': self.version,
            'SignatureMethod': 'HmacSHA256',
        }
        data.update(extra_data)
        request_description = '&'.join(['%s=%s' % (k, urllib.quote(data[k], safe='-_.~').encode('utf-8')) for k in sorted(data)])
        signature = self.calc_signature(method, request_description)
        uri = '%s?%s&Signature=%s' % (self.uri, request_description, urllib.quote(signature))
        headers={'User-Agent':'App/Version (Language=Python)'}
        headers.update(kwargs.get('extra_headers', {}))

                          
        try:
            conn.request(method, uri, kwargs.get('body', ''),
                         headers)
            response = conn.getresponse().read()
            parsed_response = self.parse_response(response)
        except HTTPException, e:
            response = e.read()
            raise MWSError(response)
        except ParseError:
            return response
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
        """Return current timestamp in proper format
        """
        return strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())

class Feeds(MWS):
    """ Amazon MWS Feeds API """

    def get_feed_submission_list(self):
        data = dict(Action='GetFeedSubmissionList')
        return self.make_request(data)

    def submit_feed(self, feed, feed_type, content_type="text/xml", purge='false'):
        data = dict(Action='SubmitFeed', FeedType=feed_type, PurgeAndReplace=purge)
        md = self.calc_md5(feed)
        return self.make_request(data, method = "POST", body=feed,
                                 extra_headers = {'Content-MD5': md, 'Content-Type': content_type})


class Reports(MWS):
    """ Amazon MWS Reports API """
    
    def get_report_count(self):
        data = dict(Action='GetReportCount')
        return self.make_request(data)

    def request_report(self, report_type, start_date='', end_date=''):
        data = dict(Action='RequestReport', StartDate=start_date, EndDate=end_date, ReportType=report_type)
        return self.make_request(data)

    def get_report(self, report_id):
        data = dict(Action='GetReport', ReportId=report_id)
        return self.make_request(data)
    
    def get_report_request_list(self, **kwargs):
        data = dict(Action='GetReportRequestList')
        data.update(kwargs)
        return self.make_request(data)


class Orders(MWS):
    """ Amazon Orders API """

    URI = "/Orders/2011-01-01"
    Version = "2011-01-01"
    NS = '{https://mws.amazonservices.com/Orders/2011-01-01}'

    def list_orders(marketplaceids, **kwargs):
        data = dict(Action='ListOrders', SellerId=self.merchant_id)
        for num, mid in enumerate(marketplaceids):
            key = 'MarketplaceId.Id.%d' % num + 1
            data[key] = mid
        data.update(kwargs)
        return self.make_request(data)
    
    def list_orders_by_next_token(next_token):
        data = dict(Action='ListOrdersByNextToken', SellerId=self.merchant_id, NextToken=next_token)
        return self.make_request(data)


class Fulfillment(MWS):
    """ Amazon MWS Fulfillment API """

    URI = '/FulfillmentInventory/2010-10-01'
    VERSION = '2010-10-01'

    def list_inventory_supply(self, skus, date_query=False, detail='Basic'):
        """ Returns information on available inventory """
        data = dict(Action='ListInventorySupply', SellerId=self.merchant_id, ResponseGroup=detail)
        # DateQuery is not supported for now :(
        for num, sku in enumerate(skus):
            data['SellerSkus.member.%d' % (num + 1)] = sku
        return self.make_request(data, "POST")
    


class Products(MWS):
    """ Amazon MWS Products API """

    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NS = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'
    

    def list_matching_products(self, query, marketplaceid, contextid=''):
        """ Returns a list of products and their attributes, ordered by 
            relevancy, based on a search query that you specify. 
            Your search query can be a phrase that describes the product 
            or it can be a product identifier such as a UPC, EAN, ISBN, or JAN.
        """
        data = dict(Action='ListMatchingProducts', 
                    SellerId=self.merchant_id,
                    MarketplaceId=marketplaceid,
                    Query=query, 
                    QueryContextId=contextid)
        return self.make_request(data)

    
    def get_matching_product(self, marketplaceid, asins):
        """ Returns a list of products and their attributes, based on a list of 
            ASIN values that you specify.
        """
        data = dict(SellerId=self.merchant_id, MarketplaceId=marketplaceid)
        for num, asin in enumerate(asins):
            data['ASINList.ASIN.%d' % (num + 1)] = asin
        return self.make_request(data)


    def get_competitive_pricing_for_sku(self, marketplaceid, skus):
        """ Returns the current competitive pricing of a product, 
            based on the SellerSKU and MarketplaceId that you specify.
        """
        data = dict(SellerId=self.merchant_id, MarketplaceId=marketplaceid)
        for num, asin in enumerate(skus):
            data['SellerSKUList.SellerSKU.%d' % (num + 1)] = asin
        return self.make_request(data)
