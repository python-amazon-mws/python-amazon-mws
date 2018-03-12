"""
Tests for the Feeds API class.
"""
import unittest
import datetime
import mws
from .utils import CommonRequestTestTools


class FeedsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Feeds.
    """
    # TODO: Add remaining methods for Feeds
    def setUp(self):
        self.api = mws.Feeds(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    # # TODO feed submission requires some file content. Building a test object will take time.
    # def test_submit_feed(self):
    #     """
    #     SubmitFeed operation
    #     """
    #     pass

    def test_get_feed_submission_list(self):
        """
        GetFeedSubmissionList operation
        """
        from_date = datetime.datetime.utcnow()
        from_date_stamp = from_date.isoformat()
        to_date = datetime.datetime.utcnow()
        to_date_stamp = from_date.isoformat()
        feed_ids = [
            '1058369303',
            '1228369302',
            '6987532174',
        ]
        feed_types = [
            '_POST_PRODUCT_DATA_',
            '_POST_FULFILLMENT_ORDER_CANCELLATION_REQUEST_DATA_',
            '_POST_UIEE_BOOKLOADER_DATA_',
        ]
        processing_statuses = [
            '_CANCELLED_',
            '_AWAITING_ASYNCHRONOUS_REPLY_',
            '_DONE_',
        ]
        max_count = 698
        params = self.api.get_feed_submission_list(
            feed_ids=feed_ids,
            max_count=max_count,
            feed_types=feed_types,
            processing_statuses=processing_statuses,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params)
        assert params['Action'] == 'GetFeedSubmissionList'
        assert params['SubmittedFromDate'] == from_date_stamp
        assert params['SubmittedToDate'] == to_date_stamp
        assert params['MaxCount'] == max_count
        assert params['FeedSubmissionIdList.Id.1'] == feed_ids[0]
        assert params['FeedSubmissionIdList.Id.2'] == feed_ids[1]
        assert params['FeedSubmissionIdList.Id.3'] == feed_ids[2]
        assert params['FeedTypeList.Type.1'] == feed_types[0]
        assert params['FeedTypeList.Type.2'] == feed_types[1]
        assert params['FeedTypeList.Type.3'] == feed_types[2]
        assert params['FeedProcessingStatusList.Status.1'] == processing_statuses[0]
        assert params['FeedProcessingStatusList.Status.2'] == processing_statuses[1]
        assert params['FeedProcessingStatusList.Status.3'] == processing_statuses[2]

    def test_get_feed_submission_list_by_next_token(self):
        """
        GetFeedSubmissionListByNextToken operation, via method decorator
        """
        next_token = '0Ys0j83sOL'
        params = self.api.get_feed_submission_list(next_token=next_token)
        self.assert_common_params(params)
        assert params['Action'] == 'GetFeedSubmissionListByNextToken'
        assert params['NextToken'] == next_token

    def test_get_feed_submission_list_by_next_token_alias(self):
        """
        GetFeedSubmissionListByNextToken operation, via alias method
        """
        next_token = 'pcq5ZXlm1e'
        params = self.api.get_feed_submission_list_by_next_token(next_token)
        self.assert_common_params(params)
        assert params['Action'] == 'GetFeedSubmissionListByNextToken'
        assert params['NextToken'] == next_token

    # TODO Complete these later
    # def test_get_feed_submission_count(self):
    #     """
    #     GetFeedSubmissionCount operation
    #     """
    #     pass

    # def test_cancel_feed_submissions(self):
    #     """
    #     CancelFeedSubmissions operation
    #     """
    #     pass

    # def test_get_feed_submission_result(self):
    #     """
    #     GetFeedSubmissionResult operation
    #     """
    #     pass
