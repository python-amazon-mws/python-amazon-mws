"""
Amazon MWS Feeds API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action


# TODO Add FeedProcessingStatus enumeration
# TODO Add FeedType enumeration


def feed_options_str(feed_options):
    """Convert a FeedOptions dict of values into an appropriate string value.
    
    Amazon docs for VAT upload with details:
    https://m.media-amazon.com/images/G/01/B2B/DeveloperGuide/vat_calculation_service__dev_guide_H383rf73k4hsu1TYRH139kk134yzs.pdf
    (section 6.4)
    
    Example:
      feed_options = {
        "shippingid": "283845474",
        "totalAmount": 3.25,
        "totalvatamount": 1.23,
        "invoicenumber": "INT-3431-XJE3",
        "documenttype": "CreditNote",
        "transactionid": "amzn:crow:429491192ksjfhe39s",
      }
      print(feed_options_str(feed_options))
      >>> "metadata:shippingid=283845474;metadata:totalAmount=3.25;metadata:totalvatamount=1.23;
      metadata:invoicenumber=INT-3431-XJE3;metadata:documenttype=CreditNote;
      metadata:transactionid=amzn:crow:429491192ksjfhe39s"
    """
    if not feed_options:
        return None
    if not isinstance(feed_options, dict):
        raise ValueError("`feed_options` should be a dict or None")
    output = []
    for key, val in feed_options.items():
        outval = val
        if outval is True or outval is False:
            # Convert literal `True` or `False` to strings `"true"` and `"false"`
            outval = str(outval).lower()
        output.append("metadata:{}={}".format(key, outval))
    return ";".join(output)


class Feeds(MWS):
    """
    Amazon MWS Feeds API

    Docs:
    http://docs.developer.amazonservices.com/en_US/feeds/Feeds_Overview.html
    """
    ACCOUNT_TYPE = "Merchant"

    NEXT_TOKEN_OPERATIONS = [
        'GetFeedSubmissionList',
    ]

    def submit_feed(self, feed, feed_type, feed_options=None, marketplace_ids=None,
                    amazon_order_id=None, document_type=None, content_type="text/xml",
                    purge='false'):
        """
        Uploads a feed for processing by Amazon MWS.
        `feed` should contain a file object in XML or flat-file format.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html
        """
        if isinstance(feed_options, dict):
            # Convert dict of options to str value
            feed_options = feed_options_str(feed_options)
        data = {
            'Action': 'SubmitFeed',
            'FeedType': feed_type,
            'FeedOptions': feed_options,
            'PurgeAndReplace': purge,
        }
        # for feed type _POST_EASYSHIP_DOCUMENTS_
        # check http://docs.developer.amazonservices.com/en_IN/easy_ship/EasyShip_HowToGetEasyShipDocs.html
        if amazon_order_id:
            data.update({'AmazonOrderId': amazon_order_id})
            # by default all document pdfs are included
            # allowed values: ShippingLabel, Invoice, Warranty
            if document_type:
                data.update({'DocumentType': document_type})
        if marketplace_ids:
            data.update(utils.enumerate_param('MarketplaceIdList.Id.', marketplace_ids))
        md5_hash = utils.calc_md5(feed)
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md5_hash, 'Content-Type': content_type})

    @next_token_action('GetFeedSubmissionList')
    def get_feed_submission_list(self, feed_ids=None, max_count=None, feed_types=None,
                                 processing_statuses=None, from_date=None, to_date=None,
                                 next_token=None):
        """
        Returns a list of all feed submissions submitted between `from_date` and `to_date`.
        If these parameters are ommitted, defaults to the previous 90 days.

        Pass `next_token` to call "GetFeedSubmissionListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionList.html
        """
        data = {
            'Action': 'GetFeedSubmissionList',
            'MaxCount': max_count,
            'SubmittedFromDate': from_date,
            'SubmittedToDate': to_date,
        }
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id', feed_ids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feed_types))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processing_statuses))
        return self.make_request(data)

    def get_feed_submission_list_by_next_token(self, token):
        """
        Alias for `get_feed_submission_list(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionListByNextToken.html
        """
        return self.get_feed_submission_list(next_token=token)

    def get_feed_submission_count(self, feed_types=None, processing_statuses=None, from_date=None, to_date=None):
        """
        Returns a count of the feeds submitted between `from_date` and `to_date`.
        If these parameters are ommitted, defaults to the previous 90 days.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionCount.html
        """
        data = {
            'Action': 'GetFeedSubmissionCount',
            'SubmittedFromDate': from_date,
            'SubmittedToDate': to_date,
        }
        data.update(utils.enumerate_param('FeedTypeList.Type.', feed_types))
        data.update(utils.enumerate_param('FeedProcessingStatusList.Status.', processing_statuses))
        return self.make_request(data)

    def cancel_feed_submissions(self, feed_ids=None, feed_types=None, from_date=None, to_date=None):
        """
        Cancels one or more feed submissions and returns a count of the feed submissions that were canceled.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_CancelFeedSubmissions.html
        """
        data = {
            'Action': 'CancelFeedSubmissions',
            'SubmittedFromDate': from_date,
            'SubmittedToDate': to_date,
        }
        data.update(utils.enumerate_param('FeedSubmissionIdList.Id.', feed_ids))
        data.update(utils.enumerate_param('FeedTypeList.Type.', feed_types))
        return self.make_request(data)

    def get_feed_submission_result(self, feed_id):
        """
        Returns the feed processing report and the Content-MD5 header.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionResult.html
        """
        data = {
            'Action': 'GetFeedSubmissionResult',
            'FeedSubmissionId': feed_id,
        }
        return self.make_request(data, rootkey='Message')
