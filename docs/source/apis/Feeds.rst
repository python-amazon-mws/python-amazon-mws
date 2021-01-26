Feeds
#####

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/feeds/Feeds_Overview.html>`_:

  The Amazon MWS Feeds API section of the Amazon Marketplace Web Service
  (Amazon MWS) API lets you upload inventory and order data to Amazon.
  You can also use the Amazon MWS Feeds API section to get information about
  the processing of feeds.

More details on how to utilize the Feeds API per MWS requirements can be
found at the above link. Below we'll provide details on how to use this API
with :py:class:`Feeds <mws.apis.feeds.Feeds>`.

Uploading metadata for VAT invoices
===================================

Metadata for VAT invoices is processed as a ``FeedOptions`` parameter to the ``SubmitFeed`` operation, as described in
Amazon's documentation, `Invoice Uploader Developer Guide (PDF)
<https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_
This parameter is not described in the standard MWS developer documentation, unfortunately, which can lead to some
confusion.

When submitting a feed, you can either build the metadata string yourself following the above guidelines,
or provide a dict to the ``feed_options`` arg for :py:meth:`mws.apis.feeds.Feeds.submit_feed`:

.. code-block:: python

    from mws import Feeds, Marketplaces

    feeds_api = Feeds(MY_ACCESS_KEY, MY_SECRET_KEY, MY_ACCOUNT_ID)

    feed_opts = {'orderid': '407-XXXXXX-6760332', 'invoicenumber': 51}

    response = feeds_api.submit_feed(
        feed=my_invoice_file.encode(),
        feed_type='_UPLOAD_VAT_INVOICE_',
        feed_options=feed_opts,
        marketplace_ids=Marketplaces.UK.marketplace_id,
    )

The above will automatically convert ``feed_opts`` into the formatted string
``'metadata:orderid=407-XXXXXX-6760332;metadata:invoicenumber=51'`` when the request is sent.
You can also send this same string as ``feed_options``, if you wish to perform your own formatting:

.. code-block:: python

    response = feeds_api.submit_feed(
        feed=my_invoice_file.encode(),
        feed_type='_UPLOAD_VAT_INVOICE_',
        feed_options='metadata:orderid=407-XXXXXX-6760332;metadata:invoicenumber=51',
        marketplace_ids=Marketplaces.UK.marketplace_id,
    )

Formatting your own FeedOptions metadata
----------------------------------------

Amazon's `documentation <https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_
describes the format for the ``FeedOptions`` parameter string as follows:

  Seller can input key value pairs to give important metadata along with the PDF
  invoice. These key value pairs should be:

  - **OrderId** (mandatory) – The order id for which the invoice is being submitted.
  - **InvoiceNumber** (mandatory) – The invoice number used in the invoice. This invoice number may be
    shared with Customers.
  - **TotalAmount** (optional) – The total amount on the invoice. This is VAT inclusive item + VAT inclusive
    gift wrap + VAT inclusive shipping – VAT inclusive promotion on item – VAT inclusive promotion on
    shipping – VAT inclusive promotion on gift wrap.
  - **VATAmount** (optional) – The total VAT amount on the invoice. This is VAT on the item + VAT on gift
    wrap + VAT on shipping – VAT on item promotion – VAT on shipping promotion – VAT on gift wrap
    promotion.
  - **DocumentType** (optional) – The value in this key can be either 'Invoice' or 'CreditNote'. If the
    document that is being uploaded is an Invoice, then input the text 'Invoice'. If the document that is
    being uploaded is a credit note for a refund or a return, then input the text 'CreditNote'. If no value
    is provided for DocumentType, the default 'Invoice' will be used.

  The key value pairs should be separated by a semicolon ``;``. The keys should be prefixed with the word
  'metadata', followed by a colon ``:`` and the key name. Keys can be upper case or lower case. Amazon will trim
  any spaces in between.

  Amazon will trim spaces in the entire string. Do not provide quotation marks around keys or values. Amazon
  will only accept the following characters in any of the inputs: Commas, slashes, spaces, - (dash), _ (underscore),
  ; (semi colon), : (colon), /, \, 0-9, A-Z, a-z, #

Following this formatting, utility function :py:func:`mws.apis.feeds.feed_options_str`
will converts a dict of key-value pairs to the appropriate format:

.. code-block:: python

    import string


    def clean_feed_option_val(val):
        permitted = string.ascii_letters + string.digits + ",\\/-_;:#" + " "
        # Note the intentional space character added at the end for clarity!
        return "".join(c for c in val if c in permitted)


    def feed_options_str(feed_options):
        output = []
        for key, val in feed_options.items():
            clean_val = clean_feed_option_val(val)
            output.append("metadata:{}={}".format(key, clean_val))
        return ";".join(output)

You are welcome to use a similar method to perform your own FeedOptions string formatting.

.. note:: The cleaning method we use will simply strip any characters that aren't in the permitted set. If this would
   produce incorrect output for your data, you will need to perform your own input cleaning, ensuring only permitted
   characters are sent.

Feeds API reference
===================

.. autoclass:: mws.apis.feeds.Feeds
   :members:

.. autofunction:: mws.apis.feeds.clean_feed_option_val
.. autofunction:: mws.apis.feeds.feed_options_str
