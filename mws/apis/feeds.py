"""Amazon MWS Feeds API."""

from mws import MWS
from mws.decorators import next_token_action
from mws.utils.crypto import calc_md5
from mws.utils.params import enumerate_param
from mws.utils.params import clean_value

# TODO Add FeedProcessingStatus enumeration
# TODO Add FeedType enumeration


def feed_options_str(feed_options):
    """Convert a FeedOptions dict of values into an appropriate string value.

    See `Amazon docs on VAT upload details
    <https://m.media-amazon.com/images/G/01/B2B/DeveloperGuide/vat_calculation_service__dev_guide_H383rf73k4hsu1TYRH139kk134yzs.pdf>`_
    (section 6.4)

    Example:

    .. code-block:: python

        options = {
            "shippingid": "283845474",
            "totalAmount": 3.25,
            "totalvatamount": 1.23,
        }
        print(feed_options_str(options))
        # "metadata:shippingid=283845474;metadata:totalAmount=3.25;metadata:totalvatamount=1.23"

    :param dict feed_options: A dict containing key-value pairs to add to metadata.
      Keys will be automatically prefixed with ``"metadata:"`` as required.
      Values will be processed by :py:func:`clean_value <mws.utils.params.clean_value>`
    :return: Metadata string, or None if ``feed_options`` is empty
    """
    if not feed_options:
        return None
    if not isinstance(feed_options, dict):
        raise ValueError("`feed_options` should be a dict or None")
    output = []
    for key, val in feed_options.items():
        outval = clean_value(val)
        output.append("metadata:{}={}".format(key, outval))
    return ";".join(output)


class Feeds(MWS):
    """Amazon MWS Feeds API.

    Docs:
    http://docs.developer.amazonservices.com/en_US/feeds/Feeds_Overview.html
    """

    URI = "/Feeds/2009-01-01"
    ACCOUNT_TYPE = "Merchant"

    NEXT_TOKEN_OPERATIONS = [
        "GetFeedSubmissionList",
    ]

    def submit_feed(
        self,
        feed,
        feed_type,
        feed_options=None,
        marketplace_ids=None,
        amazon_order_id=None,
        document_type=None,
        content_type="text/xml",
        purge=False,
    ):
        """The `SubmitFeed operation.
        <http://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html>`_
        Uploads a feed for processing by Amazon MWS.

        :param feed: A file object in XML or flat-file format, encoded to bytes.
        :param str feed_type: A `FeedType
          <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_FeedType.html>`_
          value, specifying the type of feed to send. The other options you specify
          in this request may depend on the feed type you choose.
        :param feed_options: Optional metadata to submit with the feed, particularly
          for the ``_UPLOAD_VAT_INVOICE_`` feed type.
          See Amazon doc, `Invoice Uploader Developer Guide
          <https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_,
          for details on the string formatting.

          If a dict is provided, ``feed_options`` is passed to
          :py:func:`feed_options_str`, where it is converted to a properly-formatted
          string.
        :type feed_options: dict, str, or None
        :param marketplace_ids: A list of one or more marketplace IDs (of marketplaces
          you are registered to sell in) that you want the feed to be applied to.

          A string can be passed when only one marketplace ID is used, as well.
        :type marketplace_ids: list, str, or None
        :param amazon_order_id: An Amazon-defined order identifier, used to identify
          an Amazon Easy Ship order.

          Available for ``_POST_EASYSHIP_DOCUMENTS_`` feed type and the India
          marketplace.
        :type amazon_order_id: str or None
        :param document_type: The type of PDF document that you want to get for the
          Amazon Easy Ship order identified with the ``amazon_order_id`` parameter.

          Accepts values ``"ShippingLabel"``, ``"Invoice"``, or ``"Warranty"``.
          If left as ``None``, defaults to all types.

          Available for ``_POST_EASYSHIP_DOCUMENTS_`` feed type and the India
          marketplace.
        :type document_type: str or None
        :param str content_type: Specifies the type of ``feed``, setting the request
          header ``"Content-Type"``.
        :param bool purge: According to Amazon docs: "enables the purge and replace
          functionality. Set to ``True`` to purge and replace the existing data;
          otherwise ``False``. This value only applies to product-related flat file
          feed types, which do not have a mechanism for specifying purge and
          replace in the feed body. **Use this parameter only in exceptional cases.**
          Usage is throttled to allow only one purge and replace within a 24-hour
          period."

          Defaults to ``False``.
        """
        if isinstance(feed_options, dict):
            # Convert dict of options to str value
            feed_options = feed_options_str(feed_options)
        data = {
            "FeedType": feed_type,
            "FeedOptions": feed_options,
            "PurgeAndReplace": purge,
        }
        # for feed type _POST_EASYSHIP_DOCUMENTS_
        # check http://docs.developer.amazonservices.com/en_IN/easy_ship/EasyShip_HowToGetEasyShipDocs.html
        if amazon_order_id:
            data.update({"AmazonOrderId": amazon_order_id})
            # by default all document PDFs are included
            # allowed values: ShippingLabel, Invoice, Warranty
            if document_type:
                data.update({"DocumentType": document_type})
        data.update(enumerate_param("MarketplaceIdList.Id.", marketplace_ids))

        # Add headers to this request.
        extra_headers = {"Content-MD5": calc_md5(feed), "Content-Type": content_type}
        return self.make_request(
            "SubmitFeed",
            data,
            method="POST",
            body=feed,
            extra_headers=extra_headers,
        )

    @next_token_action("GetFeedSubmissionList")
    def get_feed_submission_list(
        self,
        feed_ids=None,
        max_count=None,
        feed_types=None,
        processing_statuses=None,
        from_date=None,
        to_date=None,
        next_token=None,
    ):
        """Returns a list of all feed submissions submitted
        between `from_date` and `to_date`. If these params are ommitted,
        defaults to the previous 90 days.

        Pass `next_token` to call "GetFeedSubmissionListByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionList.html
        """
        data = {
            "MaxCount": max_count,
            "SubmittedFromDate": from_date,
            "SubmittedToDate": to_date,
        }
        data.update(enumerate_param("FeedSubmissionIdList.Id", feed_ids))
        data.update(enumerate_param("FeedTypeList.Type.", feed_types))
        data.update(
            enumerate_param("FeedProcessingStatusList.Status.", processing_statuses)
        )
        return self.make_request("GetFeedSubmissionList", data)

    def get_feed_submission_list_by_next_token(self, token):
        """Alias for `get_feed_submission_list(next_token=token)`.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionListByNextToken.html
        """
        return self.get_feed_submission_list(next_token=token)

    def get_feed_submission_count(
        self, feed_types=None, processing_statuses=None, from_date=None, to_date=None
    ):
        """Returns a count of the feeds submitted between `from_date` and `to_date`.
        If these params are ommitted, defaults to the previous 90 days.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionCount.html
        """
        data = {
            "SubmittedFromDate": from_date,
            "SubmittedToDate": to_date,
        }
        data.update(enumerate_param("FeedTypeList.Type.", feed_types))
        data.update(
            enumerate_param("FeedProcessingStatusList.Status.", processing_statuses)
        )
        return self.make_request("GetFeedSubmissionCount", data)

    def cancel_feed_submissions(
        self, feed_ids=None, feed_types=None, from_date=None, to_date=None
    ):
        """Cancels one or more feed submissions and returns a count of the
        feed submissions that were canceled.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_CancelFeedSubmissions.html
        """
        data = {
            "SubmittedFromDate": from_date,
            "SubmittedToDate": to_date,
        }
        data.update(enumerate_param("FeedSubmissionIdList.Id.", feed_ids))
        data.update(enumerate_param("FeedTypeList.Type.", feed_types))
        return self.make_request("CancelFeedSubmissions", data)

    def get_feed_submission_result(self, feed_id):
        """Returns the feed processing report and the Content-MD5 header.

        Docs:
        http://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionResult.html
        """
        return self.make_request(
            "GetFeedSubmissionResult",
            {"FeedSubmissionId": feed_id},
            result_key="Message",
        )
