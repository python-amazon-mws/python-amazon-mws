"""Amazon MWS Feeds API."""

import string
import datetime

from mws import MWS
from mws.decorators import next_token_action
from mws.utils.crypto import calc_md5
from mws.utils.params import coerce_to_bool
from mws.utils.params import enumerate_param

# DEPRECATIONS for argument names in v1.1
from mws.utils.deprecation import kwargs_renamed_for_v11


# TODO Add FeedProcessingStatus enumeration
# TODO Add FeedType enumeration


def clean_feed_option_val(val):
    """Cleans ``val`` for use in the FeedOptions parameter when submitting a feed
    for "_UPLOAD_VAT_INVOICE_" feed type.

    - Values of `None` are returned as `None`. The calling method is expected to
      exclude the key-value pair for this value from its output.
    - Booleans (True/False) will be converted to string in lowercase ('true'/'false')
    - datetime.datetime or datetime.date instances will be formatted as ISO-8601 strings

    For any other value

    Amazon states the only safe characters are:

        ``,`` (commas), ``/`` and ``\\`` (slashes), ``-`` (dash), ``_`` (underscore),
        ``;`` (semi colon), ``:`` (colon), ``#``, 0-9, A-Z, a-z, spaces

    Any character not matching the above set is stripped.
    """
    if val is None:
        return None

    if val is True or val is False:
        # Stringify and lowercase the boolean
        val = str(val).lower()
    elif isinstance(val, (datetime.datetime, datetime.date)):
        # Convert that date to ISO-8601 format string.
        # We explicitly set microseconds to 0, however, because the ``.`` character
        # (used to denote microseconds, if present) is NOT permitted in final output.
        val = val.replace(microsecond=0).isoformat()
        # NOTE granted, users are likely not going to send datetime objects through
        # this method. But it's best to be safe!

    # Convert val from any other type into string before further processing.
    val = str(val)

    # Only the following characters are permitted in Amazon output
    # (Note the intentional space character added at the end for clarity!)
    permitted = string.ascii_letters + string.digits + ",\\/-_;:#" + " "

    # Join permitted characters and return the result.
    return "".join(c for c in val if c in permitted)


def feed_options_str(feed_options):
    """Convert a ``feed_options`` dict into a formatted metadata string,
    for use with the SubmitFeed ``FeedOptions`` parameter when submitting
    VAT invoices.

    Example:

    .. code-block:: python

        feed_opts = {'orderid': '407-XXXXXX-6760332', 'invoicenumber': 51}
        opts_str = feed_options_str(feed_opts)
        # 'metadata:orderid=407-XXXXXX-6760332;metadata:invoicenumber=51'

    See Amazon documentation, `Invoice Uploader Developer Guide (PDF)
    <https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_
    (section 6.4), for details.
    """
    if not feed_options:
        return None
    if not isinstance(feed_options, dict):
        raise ValueError("`feed_options` should be a dict or None")
    output = []
    for key, val in feed_options.items():
        clean_val = clean_feed_option_val(val)
        if clean_val is not None:
            output.append("metadata:{}={}".format(key, clean_val))
    return ";".join(output)


class Feeds(MWS):
    """Amazon MWS Feeds API.

    Docs:
    https://docs.developer.amazonservices.com/en_US/feeds/Feeds_Overview.html
    """

    URI = "/Feeds/2009-01-01"
    ACCOUNT_TYPE = "Merchant"

    NEXT_TOKEN_OPERATIONS = [
        "GetFeedSubmissionList",
    ]

    @kwargs_renamed_for_v11([("marketplaceids", "marketplace_ids")])
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
        <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_SubmitFeed.html>`_
        Uploads a feed for processing by Amazon MWS.

        Requires ``feed``, a file in XML or flat-file format encoded to bytes; and
        ``feed_type``, a string detailing a `FeedType enumeration
        <https://docs.developer.amazonservices.com/en_US/feeds/Feeds_FeedType.html>`_.

        All other parameters may change depending on the ``feed_type`` you select.
        See Amazon docs for details.

        ``feed_options`` is used for ``feed_type`` "_UPLOAD_VAT_INVOICE_", to provide
        FeedOption metadata. See `Invoice Uploader Developer Guide (PDF)
        <https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_,
        for details. Can accept a dict of simple key-value pairs, which will be
        converted to the proper string format automatically.

        ``marketplace_ids`` accepts a list of one or more marketplace IDs where you
        want the feed to be applied. Can also accept a single marketplace ID as a
        string.

        ``amazon_order_id`` and ``document_type`` are used for ``feed_type``
        "_POST_EASYSHIP_DOCUMENTS_", used for Amazon Easy Ship orders
        (available only in India marketplace). Provide an Amazon Order ID as a string
        and the type of PDF document ("ShippingLabel", "Invoice", or "Warranty"; or
        `None` to get all).

        ``content_type`` sets the "Content-Type" request header, indicating the type
        of file being sent. Defaults to ``"text/xml"``.

        ``purge`` enables Amazon's "purge and replace" functionality. Set to ``True``
        to purge and replace existing data, otherwise use ``False`` (the default).
        Only applies to product-related flat file feed types.
        **Use only in exceptional cases.**
        Usage is throttled to allow only one purge and replace within a 24-hour period.
        """
        if isinstance(feed_options, dict):
            # Convert dict of options to str value
            feed_options = feed_options_str(feed_options)
        if purge is not None:
            purge = coerce_to_bool(purge)
        data = {
            "FeedType": feed_type,
            "FeedOptions": feed_options,
            "PurgeAndReplace": purge,
        }
        # for feed type _POST_EASYSHIP_DOCUMENTS_
        # check https://docs.developer.amazonservices.com/en_IN/easy_ship/EasyShip_HowToGetEasyShipDocs.html
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

    @kwargs_renamed_for_v11(
        [
            ("feedids", "feed_ids"),
            ("feedtypes", "feed_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
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
        https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionList.html
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
        https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionListByNextToken.html
        """
        return self.get_feed_submission_list(next_token=token)

    @kwargs_renamed_for_v11(
        [
            ("feedtypes", "feed_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
    )
    def get_feed_submission_count(
        self, feed_types=None, processing_statuses=None, from_date=None, to_date=None
    ):
        """Returns a count of the feeds submitted between `from_date` and `to_date`.
        If these params are ommitted, defaults to the previous 90 days.

        Docs:
        https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionCount.html
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

    @kwargs_renamed_for_v11(
        [
            ("feedids", "feed_ids"),
            ("feedtypes", "feed_types"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ]
    )
    def cancel_feed_submissions(
        self, feed_ids=None, feed_types=None, from_date=None, to_date=None
    ):
        """Cancels one or more feed submissions and returns a count of the
        feed submissions that were canceled.

        Docs:
        https://docs.developer.amazonservices.com/en_US/feeds/Feeds_CancelFeedSubmissions.html
        """
        data = {
            "SubmittedFromDate": from_date,
            "SubmittedToDate": to_date,
        }
        data.update(enumerate_param("FeedSubmissionIdList.Id.", feed_ids))
        data.update(enumerate_param("FeedTypeList.Type.", feed_types))
        return self.make_request("CancelFeedSubmissions", data)

    @kwargs_renamed_for_v11(
        [
            ("feedid", "feed_id"),
        ]
    )
    def get_feed_submission_result(self, feed_id):
        """Returns the feed processing report and the Content-MD5 header.

        Docs:
        https://docs.developer.amazonservices.com/en_US/feeds/Feeds_GetFeedSubmissionResult.html
        """
        return self.make_request(
            "GetFeedSubmissionResult",
            {"FeedSubmissionId": feed_id},
            result_key="Message",
        )
