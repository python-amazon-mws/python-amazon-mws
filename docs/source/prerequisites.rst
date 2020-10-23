Prerequisites for MWS connectivity
##################################

.. seealso:: All links in this documentation point to the ``developer.amazonservices.com``
   domain, but other regional domains are provided by Amazon. For a list of portals for other
   regions, please see `Related Resources (MWS documentation link)
   <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Resources.html>`_.

In order to use python-amazon-mws, you must have an Amazon Professional Seller account,
and you must `register as a developer
<http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Registering.html>`_.
You will then be provided a set of MWS credentials, which include your
**Seller ID**, **Access Key**, and **Secret Key**  (and, possibly, **Auth Token**).

These credentials, along with a `Marketplace ID
<http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html>`_,
will be needed to make requests to MWS, whether using python-amazon-mws or
any other MWS-related service.

Test MWS access using Scratchpad
================================

You can test your access to MWS using **Amazon MWS Scratchpad** (`docs
<http://docs.developer.amazonservices.com/en_US/scratchpad/Scratchpad_Using.html>`_):

1. Open the `Scratchpad <https://mws.amazonservices.com/scratchpad/index.html>`_.

   .. warning:: Always verify the URL of the Scratchpad before entering your MWS credentials!
     The domain should be ``mws.amazonservices.com`` or one of Amazon's other regional domains
     (see `here <http://docs.developer.amazonservices.com/en_US/scratchpad/Scratchpad_Using.html>`_
     for a list of regional portals).

2. Enter your **MWS credentials** in the **Authentication** section.
3. In **API Section**, choose "Products".
4. In **Operation**, choose "ListMatchingProducts".
5. Under **Required API Parameters**, enter:

   - ``MarketplaceID``: A valid MarketplaceID for your desired marketplace
     (example: ``ATVPDKIKX0DER`` for the US market).
     See: `Amazon MWS endpoints and MarketplaceId values
     <http://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html>`_.
   - ``Query``: ``python``, to search for products containing "python" somewhere in their description.

6. Click **Submit**.

If your access works, you should an XML response beginning with ``ListMatchingProductsResponse``.
Otherwise, you may see an ``ErrorResponse``, with an error message indicating the problem.
