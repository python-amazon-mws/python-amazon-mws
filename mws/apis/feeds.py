"""
Amazon MWS Feeds API
"""
from __future__ import absolute_import
import warnings

from ..mws import MWS
from .. import utils
from ..decorators import next_token_action


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
        md5_hash = utils.calc_md5(feed)
        return self.make_request(data, method="POST", body=feed,
                                 extra_headers={'Content-MD5': md5_hash, 'Content-Type': content_type})

    @next_token_action('GetFeedSubmissionList')
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
