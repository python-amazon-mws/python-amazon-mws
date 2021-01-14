Products
########

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/products/Products_Overview.html>`_:

   The Products API section of Amazon Marketplace Web Service (Amazon MWS) helps you get information to match your
   products to existing product listings on Amazon Marketplace websites and to make sourcing and pricing decisions for
   listing those products on Amazon Marketplace websites. The Amazon MWS Products API returns product attributes,
   current Marketplace pricing information, and a variety of other product and listing information.

The Products API is available in all marketplaces and consists of 15 different operations:

GetMatchingProduct
==================

ASINs can be provided either as a list, or as a single ASIN string:

.. code-block:: python

    resp = products_api.get_matching_product(
        marketplace_id=my_marketplace,
        asins=["B085G58KWT", "B07ZZW7QCM"],
    )
    # OR:
    resp = products_api.get_matching_product(
        marketplace_id=my_marketplace,
        asins="B085G58KWT",
    )

.. code-block:: python

    # Access individual ASINs:
    resp.parsed[0]

    print(resp.parsed[0].ASIN)
    # B085G58KWT

    print(resp.parsed[0].Product.AttributeSets.ItemAttributes.ListPrice.Amount)
    # 89.99

Examples:
---------

.. code-block:: python

    resp.parsed.ASIN
    # B085G58KWT

.. code-block:: python

    resp.parsed.Product.AttributeSets.ItemAttributes.Color
    # Charcoal

GetMatchingProductForId
=======================

Same as above GetMatchingProduct but allows extra id types.

.. code-block:: python

    resp = products_api.get_matching_product_for_id(
        marketplace_id=my_marketplace,
        type_="ASIN", # can be ASIN, GCID, SellerSKU,UPC, EAN,ISBN, JAN
        ids=["B085G58KWT", "B07ZZW7QCM"],
    )

GetCompetitivePricingForSKU
===========================

.. code-block:: python

    resp = products_api.get_competitive_pricing_for_sku(
        marketplace_id=my_marketplace,
        skus=["OO-NL0F-795Z"],
    )


Example:
--------

Buy Box price

.. code-block:: python

    resp.parsed.Product.CompetitivePricing.CompetitivePrices.CompetitivePrice.Price.LandedPrice.Amount

GetCompetitivePricingForASIN
============================

From Amazon:
   Returns the current competitive price of a product, based on ASIN.

.. code-block:: python

    resp = products_api.get_competitive_pricing_for_asin(
        marketplace_id=my_marketplace,
        asins=["B085G58KWT"],
    )

Same as GetCompetitivePricingForSKU above, but pass in a list of ASINs rather than SKUs.

GetLowestOfferListingsForSKU
============================

.. code-block:: python

    resp = products_api.get_lowest_offer_listings_for_sku(
        marketplace_id=my_marketplace,
        skus=["OO-NL0F-795Z"],
        condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
    )

GetLowestOfferListingsForASIN
=============================

.. code-block:: python

    resp = products_api.get_lowest_offer_listings_for_asin(
        marketplace_id=my_marketplace,
        asins=["B085G58KWT"],
        condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
    )

GetLowestPricedOffersForSKU
===========================

.. code-block:: python

    resp = products_api.get_lowest_priced_offers_for_sku(
        marketplace_id=my_marketplace,
        skus=["OO-NL0F-795Z"],
        condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
    )

GetLowestPricedOffersForASIN
============================

.. code-block:: python

    resp = products_api.get_lowest_priced_offers_for_asin(
        marketplace_id=my_marketplace,
        asins=["B085G58KWT"],
        condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
    )

GetMyFeesEstimate
=================

.. code-block:: python

    my_price = MoneyType(amount=123.45, currency_code="GBP")
    my_shipping = MoneyType(amount=0.00, currency_code="GBP")
    my_product_price = PriceToEstimateFees(listing_price=my_price, shipping=my_shipping)

    my_product = FeesEstimateRequest(
        marketplace_id = my_marketplace,
        id_type="ASIN",  # ASIN or SKU
        id_value="B07QR73T66",
        price_to_estimate_fees=my_product_price,
        is_amazon_fulfilled=False,
        identifier="request001",  # any identifier you want
    )

    resp = products_api.get_my_fees_estimate(my_product)

GetMyPriceForSKU
================

.. code-block:: python

    resp = pr oducts_api.get_my_price_for_sku(
        marketplace_id = my_marketplace,
        skus="OO-NL0F-795Z",
        condition="New"
        # Any, New, Used, Collectible, Refurbished, Club. Default = All
    )

GetMyPriceForASIN
=================

.. code-block:: python

    resp = products_api.get_my_price_for_asin(
        marketplace_id=my_marketplace,
        asins="B07QR73T66",
        condition="New"
        # Any, New, Used, Collectible, Refurbished, Club. Default = All
    )

GetProductCategoriesForSKU
==========================

.. code-block:: python

    resp = products_api.get_product_categories_for_sku(
        marketplace_id=my_marketplace,
        sku="OO-NL0F-795Z"
    )

GetProductCategoriesForASIN
===========================

.. code-block:: python

    resp = products_api.get_product_categories_for_asin(
        marketplace_id=my_marketplace,
        asin="B07QR73T66"
    )

Products API
============

All examples below assume you have setup your Products API instance appropriately. Refer to :doc:`../gettingStarted`
for details:

.. code-block:: python

    from mws import Products

    products_api = Products(
        access_key="...",
        secret_key="...",
        account_id="...",
        auth_token="...",
    )

All request methods in the Products API also require a **Marketplace ID** to specify which marketplace the products
are sold in. For example, using the US marketplace:

.. code-block:: python

    from mws import Marketplaces

    my_marketplace = Marketplaces.US.marketplace_id

.. ################################################# Class definition ##################################################
.. autoclass:: mws.apis.products.Products

   .. ############################################## ListMatchingProducts ##############################################
   .. automethod:: list_matching_products

      .. rubric:: Examples:

      - Obtaining ASINs for products returned by the query ``"Python"``:

        .. code-block:: python

            resp = products_api.list_matching_products(
                marketplace_id=my_marketplace,
                query=“Python”,
            )

            for product in resp.parsed.Products.Product:
                asin = product.Identifiers.MarketplaceASIN.ASIN
                print(f"ASIN: {asin}")

        .. note:: As a shorthand, you may access the first product from the response using a list index:

           .. code-block:: python

               resp.parsed.Products.Product[0].Identifiers.MarketplaceASIN.ASIN

           Beware: if only one product is returned, this may result in an error, as the ``Product`` node
           will not be a list. Iterating nodes is generally safer to avoid this issue (see:
           :ref:`DotDict Native Iteration <native_iteration>`).

      - Returning sales rank categories and rank numbers:

        .. code-block:: python

            for product in resp.parsed.Products.Product:
                for rank in product.SalesRankings.SalesRank:
                    category_id = rank.ProductCategoryId
                    sales_rank = rank.Rank
                    print(f"Category: {category_id}, Rank: {sales_rank}")

      - Returning product titles:

        .. code-block:: python

            for product in resp.parsed.Products.Product:
                product_title = product.AttributeSets.ItemAttributes.Title
                print(f"Title: {product_title}")

   .. ############################################### GetMatchingProduct ###############################################
   .. automethod:: get_matching_product

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ############################################ GetMatchingProductForId #############################################
   .. automethod:: get_matching_product_for_id(marketplace_id: str, type_: str, ids: Union[List[str], str])

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetCompetitivePricingForSKU ###########################################
   .. automethod:: get_competitive_pricing_for_sku

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetCompetitivePricingForASIN ##########################################
   .. automethod:: get_competitive_pricing_for_asin

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetLowestOfferListingsForSKU ##########################################
   .. automethod:: get_lowest_offer_listings_for_sku

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetLowestOfferListingsForASIN #########################################
   .. automethod:: get_lowest_offer_listings_for_asin

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetLowestPricedOffersForSKU ###########################################
   .. automethod:: get_lowest_priced_offers_for_sku

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################## GetLowestPricedOffersForASIN ##########################################
   .. automethod:: get_lowest_priced_offers_for_asin

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ############################################### GetMyFeesEstimate ################################################
   .. automethod:: get_my_fees_estimate

      Accepts one or more :py:class:`FeesEstimateRequest <mws.models.products.FeesEstimateRequest>` instances as
      arguments.

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ################################################ GetMyPriceForSKU ################################################
   .. automethod:: get_my_price_for_sku

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ################################################ GetMyPriceForASIN ###############################################
   .. automethod:: get_my_price_for_asin

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################### GetProductCategoriesForSKU ###########################################
   .. automethod:: get_product_categories_for_sku

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo

   .. ########################################### GetProductCategoriesForASIN ##########################################
   .. automethod:: get_product_categories_for_asin

      .. rubric:: Examples

      - Something:

        .. code-block:: python

            # foo
