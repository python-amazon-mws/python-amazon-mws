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
with :py:class:`Feeds <mws.Feeds>`.

Uploading metadata for VAT invoices
===================================

Metadata for VAT invoices is processed as a ``FeedOptions`` parameter to the ``SubmitFeed`` operation, as described in
Amazon's documentation, `Invoice Uploader Developer Guide (PDF)
<https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_
This parameter is not described in the standard MWS developer documentation, unfortunately, which can lead to some
confusion.

When submitting a feed, you can either build the metadata string yourself following the above guidelines,
or provide a dict to the ``feed_options`` arg for :py:meth:`Feeds.submit_feed <mws.Feeds.submit_feed>`:

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

.. note:: The format for the FeedOptions string is described in Amazon's documentation
   `here <https://m.media-amazon.com/images/G/03/B2B/invoice-uploader-developer-documentation.pdf>`_ (PDF).
   You are welcome to format your own FeedOptions string, if you find that the python-amazon-mws implementation
   is not suitable for your specific needs.

   You can find our implementation for this formatting within the source for :py:class:`Feeds <mws.Feeds>`.

Feeds API reference
===================

.. autoclass:: mws.Feeds
   :members:
