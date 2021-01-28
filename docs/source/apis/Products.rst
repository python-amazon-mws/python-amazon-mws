Products
########

According to `Amazon's documentation
<https://docs.developer.amazonservices.com/en_US/products/Products_Overview.html>`_:

   The Products API section of Amazon Marketplace Web Service (Amazon MWS) helps you get information to match your
   products to existing product listings on Amazon Marketplace websites and to make sourcing and pricing decisions for
   listing those products on Amazon Marketplace websites. The Amazon MWS Products API returns product attributes,
   current Marketplace pricing information, and a variety of other product and listing information.

Using examples on this page
===========================

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

All request methods in the Products API also require a **MarketplaceId** to specify which marketplace the products
are sold in. MarketplaceId values should match one of the values specified in Amazon documentation:
`Amazon MWS endpoints and MarkeplaceId values <https://docs.developer.amazonservices.com/en_US/dev_guide/DG_Endpoints.html>`_

python-amazon-mws makes these values available through the :py:class:`Marketplaces <mws.mws.Marketplaces>` Enum, which
contains both the ``endpoint`` and ``marketplace_id`` for each Amazon region via that region's country code.

For convenience, a ``Marketplaces`` instance will return its MarketplaceId through the ``.value`` attribute, as well.
Further, all request methods in python-amazon-mws will automatically "clean" Enum instances by returning their ``.value``
attributes.

The following are all valid methods for obtaining, for example, the MarketplaceId for the US region and passing it
to a request method in the ``Products`` API:

.. code-block:: python

    from mws import Marketplaces

    my_market = Marketplaces.US
    # Returns the Enum instance for the US region.
    # When used in a request method, the `marketplace_id` value will be used automatically.

    print(my_market.marketplace_id)
    # 'ATVPDKIKX0DER'
    print(my_market.value)
    # 'ATVPDKIKX0DER'
    # (alias for `.marketplace_id`)

    # You can also return the endpoint for that region, if needed:
    print(my_market.endpoint)
    # 'https://mws.amazonservices.com'

In all examples below, replace ``my_market`` with the ``Marketplaces`` Enum instance or MarketplaceId string value
relevant to your region.

Products API reference
======================

.. ################################################# Class definition ##################################################
.. autoclass:: mws.apis.products.Products

   .. ############################################## ListMatchingProducts ##############################################
   .. automethod:: list_matching_products

      .. rubric:: Examples:

      - Obtaining ASINs for products returned by the query ``"Python"``:

        .. code-block:: python

            resp = products_api.list_matching_products(
                marketplace_id=my_market,
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

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_matching_product(
              marketplace_id=my_market,
              asins=["B085G58KWT", "B07ZZW7QCM"],
          )

          # Iterate over products returned by the request
          for product in resp.parsed.Product:
              # Access identifiers
              print(product.Identifiers.MarketplaceASIN.ASIN)
              print(product.Identifiers.MarketplaceASIN.MarketplaceId)

              # Attributes of the product, for instance a ListPrice (by amount and currency code):
              print(product.AttributeSets.ItemAttributes.ListPrice.Amount)
              print(product.AttributeSets.ItemAttributes.ListPrice.CurrencyCode)

   .. ############################################ GetMatchingProductForId #############################################
   .. automethod:: get_matching_product_for_id(marketplace_id: str, type_: str, ids: Union[List[str], str])

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_matching_product_for_id(
              marketplace_id=my_market,
              type_="ASIN",
              ids=["B085G58KWT", "B07ZZW7QCM"],
          )

   .. ########################################## GetCompetitivePricingForSKU ###########################################
   .. automethod:: get_competitive_pricing_for_sku

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_competitive_pricing_for_sku(
              marketplace_id=my_market,
              skus=["OO-NL0F-795Z"],
          )

          for product in resp.parsed.Product:
              product.CompetitivePricing.NumberOfOfferListings
              product.CompetitivePricing.CompetitivePrices.CompetitivePrice.Price.LandedPrice.Amount

   .. ########################################## GetCompetitivePricingForASIN ##########################################
   .. automethod:: get_competitive_pricing_for_asin

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_competitive_pricing_for_asin(
              marketplace_id=my_market,
              asins=["B085G58KWT"],
          )

   .. ########################################## GetLowestOfferListingsForSKU ##########################################
   .. automethod:: get_lowest_offer_listings_for_sku

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_lowest_offer_listings_for_sku(
              marketplace_id=my_market,
                skus=["OO-NL0F-795Z"],
                condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
            )

   .. ########################################## GetLowestOfferListingsForASIN #########################################
   .. automethod:: get_lowest_offer_listings_for_asin

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_lowest_offer_listings_for_asin(
              marketplace_id=my_market,
              asins=["B085G58KWT"],
              condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
          )

   .. ########################################## GetLowestPricedOffersForSKU ###########################################
   .. automethod:: get_lowest_priced_offers_for_sku

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_lowest_priced_offers_for_sku(
              marketplace_id=my_market,
              skus=["OO-NL0F-795Z"],
              condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
          )

   .. ########################################## GetLowestPricedOffersForASIN ##########################################
   .. automethod:: get_lowest_priced_offers_for_asin

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_lowest_priced_offers_for_asin(
              marketplace_id=my_market,
              asins=["B085G58KWT"],
              condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
          )

   .. ############################################### GetMyFeesEstimate ################################################
   .. automethod:: get_my_fees_estimate

      Accepts one or more :py:class:`FeesEstimateRequest <mws.models.products.FeesEstimateRequest>` instances as
      arguments:

      .. rubric:: Example
      .. code-block:: python

          estimate_request = FeesEstimateRequest(...)
          resp = products_api.get_my_fees_estimate(estimate_request)

      Multiple estimates can be requested at the same time, as well:

      .. code-block:: python

          estimate_request1 = FeesEstimateRequest(...)
          estimate_request2 = FeesEstimateRequest(...)
          resp = products_api.get_my_fees_estimate(estimate_request1, estimate_request2, ...)

   .. ################################################ GetMyPriceForSKU ################################################
   .. automethod:: get_my_price_for_sku

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_my_price_for_sku(
            marketplace_id = my_market,
            skus="OO-NL0F-795Z",
            condition="New"
            # Any, New, Used, Collectible, Refurbished, Club. Default = All
        )

   .. ################################################ GetMyPriceForASIN ###############################################
   .. automethod:: get_my_price_for_asin

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_my_price_for_asin(
              marketplace_id=my_market,
              asins="B07QR73T66",
              condition="New"
              # Any, New, Used, Collectible, Refurbished, Club. Default = All
          )

   .. ########################################### GetProductCategoriesForSKU ###########################################
   .. automethod:: get_product_categories_for_sku

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_product_categories_for_sku(
              marketplace_id=my_market,
              sku="OO-NL0F-795Z"
          )

   .. ########################################### GetProductCategoriesForASIN ##########################################
   .. automethod:: get_product_categories_for_asin

      .. rubric:: Example
      .. code-block:: python

          resp = products_api.get_product_categories_for_asin(
              marketplace_id=my_market,
              asin="B07QR73T66"
          )

Data models
===========

.. autoclass:: mws.models.products.FeesEstimateRequest

   Instances of this model are required for the argument(s) of
   :py:meth:`get_my_fees_estimate <mws.apis.products.Products.get_my_fees_estimate>`. Constructing an instance of this
   model requires the use of other data models in the Products API, as well.

   .. rubric:: Example

   1. Start by creating :py:class:`MoneyType <mws.models.products.MoneyType>` instances to account for different prices
      associated with the request, such as ``listing_price`` and ``shipping``:

      .. code-block:: python

          from mws.models.products import MoneyType, CurrencyCode

          my_price = MoneyType(amount=123.45, currency_code=CurrencyCode.GBP)
          # Note the `currency_code` argument also accepts string literals of the currency code:
          my_shipping = MoneyType(amount=5.00, currency_code='GBP')

   2. Combine these prices into a :py:class:`PriceToEstimateFees <mws.models.products.PriceToEstimateFees>` instance:

      .. code-block:: python

          from mws.models.products import PriceToEstimateFees

          my_product_price = PriceToEstimateFees(listing_price=my_price, shipping=my_shipping)

      For the JP market only, this price to estimate fees may optionally include
      :py:class:`Points <mws.models.products.Points>`.

   3. Use the ``PriceToEstimateFees`` instance along with other data to construct the final
      ``FeesEstimateRequest`` instance:

      .. code-block:: python

          from mws.models.products import FeesEstimateRequest

          estimate_request = FeesEstimateRequest(
              marketplace_id=my_market,
              id_type="ASIN",  # either 'ASIN' or 'SKU', indicating the type of the `id_value` argument:
              id_value="B07QR73T66",
              price_to_estimate_fees=my_product_price,  # your `PriceToEstimateFees` instance
              is_amazon_fulfilled=False,
              identifier="request001",  # a unique identifier of your choosing
          )

.. autoclass:: mws.models.products.PriceToEstimateFees

   Accepts instances of :py:class:`MoneyType <mws.models.products.MoneyType>` for its ``listing_price`` and
   ``shipping``, and optionally accepts a :py:class:`Points <mws.models.products.Points>` instance
   to denote a points value (in JP region only).

.. autoclass:: mws.models.products.MoneyType

   .. rubric:: Example
   .. code-block:: python

      from mws.models.products import MoneyType, CurrencyCode

      my_money = MoneyType(amount=3.50, currency_code=CurrencyCode.USD)

.. autoclass:: mws.models.products.Points

   Points are expressed in terms of a ``points_number`` and a ``monetary_value`` for those points, the latter of which
   must be an instance of :py:class:`MoneyType <mws.models.products.MoneyType>`.

   .. rubric:: Example:
   .. code-block:: python

      from mws.models.products import Points, MoneyType, CurrencyCode

      # A monetary value of 2000 Japanese yen
      monetary_value = MoneyType(amount=2000.0, currency_code=CurrencyCode.JPY)

      # Now assign the points like so:
      points = Points(points_number=35, monetary_value=monetary_value)

   When used in a request, `points` will be converted to a set of parameters like so:

   .. code-block:: python

      print(points.to_params())
      # {'PointsNumber': 35, 'PointsMonetaryValue.Amount': 2000.0, 'PointsMonetaryValue.CurrencyCode': <CurrencyCode.JPY: ('JPY', 'Japanese yen')>}

   .. note:: You will see the ``PointsMonetaryValue.CurrencyCode`` element remains an instance of Enum at this stage.
      When used in a request, it is automatically "cleaned" to its parameterized value, ``'JPY'``.

      Passing the string literal ``'JPY'`` as the ``MoneyType.currency_code`` argument is also accepted.

Enums
=====

.. autoclass:: mws.models.products.CurrencyCode

   The following currency codes are available:

   - ``USD``: United States dollar
   - ``EUR``: European euro
   - ``GBP``: Great Britain pounds
   - ``RMB``: Chinese yuan
   - ``INR``: Indian rupee
   - ``JPY``: Japanese yen
   - ``CAD``: Canadian dollar
   - ``MXN``: Mexican peso

   .. rubric:: Example:
   .. code-block:: python

      from mws.models.products import MoneyType, CurrencyCode

      # 10 US dollars
      listing_price = MoneyType(amount=10.0, currency_code=CurrencyCode.USD)
      print(listing_price.to_params())
      # {"Amount": 10.0, "CurrencyCode": "USD"}

      # 30 Chinese yuan
      shipping = MoneyType(30.0, CurrencyCode.RMB)
      print(shipping.to_params())
      # {"Amount": 30.0, "CurrencyCode": "RMB"}
