"""Tests for the Feeds API class."""

import unittest
import datetime
import mws
from mws.utils import clean_date

from .utils import CommonAPIRequestTools


class FeedsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Feeds."""

    api_class = mws.Feeds

    # TODO feed submission requires some file content.
    # def test_submit_feed(self):
    #     """SubmitFeed operation"""
    #     pass

    def test_get_feed_submission_list(self):
        """GetFeedSubmissionList operation"""
        from_date = datetime.datetime.utcnow()
        from_date_stamp = clean_date(from_date)
        to_date = datetime.datetime.utcnow()
        to_date_stamp = clean_date(to_date)
        feed_ids = [
            "1058369303",
            "1228369302",
        ]
        feed_types = [
            "_POST_PRODUCT_DATA_",
            "_POST_FULFILLMENT_ORDER_CANCELLATION_REQUEST_DATA_",
        ]
        processing_statuses = [
            "_SUBMITTED_",
            "_AWAITING_ASYNCHRONOUS_REPLY_",
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
        self.assert_common_params(params, action="GetFeedSubmissionList")
        self.assertEqual(params["SubmittedFromDate"], from_date_stamp)
        self.assertEqual(params["SubmittedToDate"], to_date_stamp)
        self.assertEqual(params["MaxCount"], str(max_count))
        self.assertEqual(params["FeedSubmissionIdList.Id.1"], feed_ids[0])
        self.assertEqual(params["FeedSubmissionIdList.Id.2"], feed_ids[1])
        self.assertEqual(params["FeedTypeList.Type.1"], feed_types[0])
        self.assertEqual(params["FeedTypeList.Type.2"], feed_types[1])
        self.assertEqual(
            params["FeedProcessingStatusList.Status.1"], processing_statuses[0]
        )
        self.assertEqual(
            params["FeedProcessingStatusList.Status.2"], processing_statuses[1]
        )

    def test_get_feed_submission_list_by_next_token(self):
        """GetFeedSubmissionListByNextToken operation, via method decorator"""
        next_token = "0Ys0j83sOL"
        params = self.api.get_feed_submission_list(next_token=next_token)
        self.assert_common_params(params, action="GetFeedSubmissionListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_feed_submission_list_by_next_token_alias(self):
        """GetFeedSubmissionListByNextToken operation, via alias method"""
        next_token = "pcq5ZXlm1e"
        params = self.api.get_feed_submission_list_by_next_token(next_token)
        self.assert_common_params(params, action="GetFeedSubmissionListByNextToken")
        self.assertEqual(params["NextToken"], next_token)

    def test_get_feed_submission_count(self):
        """GetFeedSubmissionCount operation"""
        from_date = datetime.datetime.utcnow()
        from_date_stamp = clean_date(from_date)
        to_date = datetime.datetime.utcnow()
        to_date_stamp = clean_date(to_date)
        feed_types = [
            "_POST_PRODUCT_OVERRIDES_DATA_",
            "_POST_FLAT_FILE_FULFILLMENT_ORDER_CANCELLATION_REQUEST_DATA_",
        ]
        processing_statuses = [
            "_IN_PROGRESS_",
            "_UNCONFIRMED_",
        ]
        params = self.api.get_feed_submission_count(
            feed_types=feed_types,
            processing_statuses=processing_statuses,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="GetFeedSubmissionCount")
        self.assertEqual(params["SubmittedFromDate"], from_date_stamp)
        self.assertEqual(params["SubmittedToDate"], to_date_stamp)
        self.assertEqual(params["FeedTypeList.Type.1"], feed_types[0])
        self.assertEqual(params["FeedTypeList.Type.2"], feed_types[1])
        self.assertEqual(
            params["FeedProcessingStatusList.Status.1"], processing_statuses[0]
        )
        self.assertEqual(
            params["FeedProcessingStatusList.Status.2"], processing_statuses[1]
        )

    def test_cancel_feed_submissions(self):
        """CancelFeedSubmissions operation"""
        from_date = datetime.datetime.utcnow()
        from_date_stamp = clean_date(from_date)
        to_date = datetime.datetime.utcnow()
        to_date_stamp = clean_date(to_date)
        feed_ids = [
            "SUB63kvutS",
            "l8dM04jxGD",
        ]
        feed_types = [
            "_CANCELLED_",
            "_DONE_",
        ]
        params = self.api.cancel_feed_submissions(
            feed_ids=feed_ids,
            feed_types=feed_types,
            from_date=from_date,
            to_date=to_date,
        )
        self.assert_common_params(params, action="CancelFeedSubmissions")
        self.assertEqual(params["SubmittedFromDate"], from_date_stamp)
        self.assertEqual(params["SubmittedToDate"], to_date_stamp)
        self.assertEqual(params["FeedSubmissionIdList.Id.1"], feed_ids[0])
        self.assertEqual(params["FeedSubmissionIdList.Id.2"], feed_ids[1])
        self.assertEqual(params["FeedTypeList.Type.1"], feed_types[0])
        self.assertEqual(params["FeedTypeList.Type.2"], feed_types[1])

    def test_get_feed_submission_result(self):
        """GetFeedSubmissionResult operation"""
        feed_id = "SJT63jt6M3"
        params = self.api.get_feed_submission_result(feed_id)
        self.assert_common_params(params, action="GetFeedSubmissionResult")
        self.assertEqual(params["FeedSubmissionId"], feed_id)
