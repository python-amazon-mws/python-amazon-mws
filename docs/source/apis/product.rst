########
Products
########
  

According to `Amazon’s documentation <http://docs.developer.amazonservices.com/en_US/products/Products_Overview.html>`_: 


   The Products API section of Amazon Marketplace Web Service (Amazon MWS) helps you get information to match your products to existing product listings on Amazon Marketplace websites and to make sourcing and pricing decisions for listing those products on Amazon Marketplace websites. The Amazon MWS Products API returns product attributes, current Marketplace pricing information, and a variety of other product and listing information.
  

The Products API is available in all marketplaces and consists of 15 different operations:
  
   `ListMatchingProducts <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#listmatchingproducts>`_ = `list_matching_products() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L29>`_
  
   `GetMatchingProduct <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getmatchingproduct>`_ = `get_matching_product() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L45>`_
  
   `GetMatchingProductForId <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getmatchingproductforid>`_ = `get_matching_product_for_id() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L56>`_
  
   `GetCompetitivePricingForSKU <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getcompetitivepricingforsku>`_ = `get_competitive_pricing_for_sku() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L71>`_
  
   `GetCompetitivePricingForASIN <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getcompetitivepricingforasin>`_ = `get_competitive_pricing_for_asin() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L82>`_
  
   `GetLowestOfferListingsForSKU <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getlowestofferlistingsforsku>`_ = `get_lowest_offer_listings_for_sku() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L95>`_
  
   `GetLowestOfferListingsForASIN <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getlowestofferlistingsforasin>`_ = `get_lowest_offer_listings_for_asin() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L117>`_
  
   `GetLowestPricedOffersForSKU <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getlowestpricedoffersforsku>`_ = `get_lowest_priced_offers_for_sku() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L138>`_
  
   `GetLowestPricedOffersForASIN <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getlowestpricedoffersforasin>`_ = `get_lowest_priced_offers_for_asin() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L161>`_
  
   `GetMyFeesEstimate <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getmyfeesestimate>`_ = `get_my_fees_estimate() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L181>`_
  
   `GetMyPriceForSKU <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getmypriceforsku>`_ = `get_my_price_for_sku() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L196>`_
  
   `GetMyPriceForASIN <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getmypriceforasin>`_ = `get_my_price_for_asin() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L210>`_
  
   `GetProductCategoriesForSKU <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getproductcategoriesforsku>`_ = `get_product_categories_for_sku() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L224>`_
  
   `GetProductCategoriesForASIN <https://github.com/Ryan-Daly/python-amazon-mws/blob/develop/docs/source/apis/product.rst#getproductcategoriesforasin>`_ = `get_product_categories_for_asin() <https://github.com/python-amazon-mws/python-amazon-mws/blob/bba6c5ed2080e5864840098ecb9f6ab7f9ac2def/mws/apis/products.py#L236>`_
  
  
***************
Getting Started
***************
  
Please read through gettingStarted.rst, as these docs build upon those.

.. code-block:: python

      import mws

      access_key = “XXXXXXXXXXXXXXXXXXXX”
      secret_key = “XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX”
      seller_id = “XXXXXXXXXXXXXX”
      region = “XX”
      my_marketplace = Marketplace.US.marketplace_id
      
      products_api = mws.Products(access_key, secret_key, seller_id, region)
  
  
  
************************
`ListMatchingProducts <https://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html>`_
************************

From Amazon:

   The ListMatchingProducts operation returns a list of products and their attributes, ordered by relevancy, based on a search query that you specify. Your search query can be a phrase that describes the product or it can be a product identifier such as a GCID, UPC, EAN, ISBN, or JAN. Returns 10 results.
  

.. code-block:: python

      response = products_api.list_matching_products(
         marketplace_id = my_marketplace,
         query = “Amazon alexa”
      )



  
Examples
========

We can access individual results with:

.. code-block:: python

      response.parsed.Products.product[0]
  
Sales Rank:

.. code-block:: python

      response.parsed.Products.Product[0].SalesRankings.SalesRank[0].Rank
      # 6
  
ASIN:

.. code-block:: python

      response.parsed.Products.Product[0].Identifiers.MarketplaceASIN.ASIN
      # B085G58KWT
  
Title:

.. code-block:: python

      response.parsed.Products.Product[0].AttributeSets.ItemAttributes.Title
      # All-new Echo (4th generation) | With premium sound, smart home hub and Alexa | Charcoal
  
  

*********************
`GetMatchingProduct <http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProduct.html>`_
*********************

From Amazon:
   The GetMatchingProduct operation returns a list of products and their attributes, based on a list of ASIN values that you specify. This operation returns a maximum of ten products.
  
Can supply ASINs as a list:
.. code-block:: python

      response = products_api.get_matching_product(
         marketplace_id=my_marketplace,
         asins=["B085G58KWT", "B07ZZW7QCM"],
      )
  
  
Example:
========

Access individual ASINs:

.. code-block:: python

      response.parsed[0]

.. code-block:: python

      response.parsed[0].ASIN
      # B085G58KWT

.. code-block:: python

      response.parsed[0].Product.AttributeSets.ItemAttributes.ListPrice.Amount
      # 89.99
	

  
Or as a single string ASIN:

.. code-block:: python

      response = products_api.get_matching_product(
         marketplace_id=my_marketplace,
         asins="B085G58KWT",
      )
  
  
Examples:
=========

.. code-block:: python

      response.parsed.ASIN
      # B085G58KWT

.. code-block:: python

      response.parsed.Product.AttributeSets.ItemAttributes.Color
      # Charcoal
  
  

**************************
`GetMatchingProductForId <https://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html>`_
**************************


Same as above GetMatchingProduct but allows extra id types.
  
From Amazon:
   Returns a list of products and their attributes, based on a list of ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.
  

.. code-block:: python

      response = products_api.get_matching_product_for_id(
         marketplace_id=my_marketplace,
         type_="ASIN", # can be ASIN, GCID, SellerSKU,UPC, EAN,ISBN, JAN
         ids=["B085G58KWT", "B07ZZW7QCM"],
      )
  
  
  
******************************
`GetCompetitivePricingForSKU <https://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForSKU.html>`_
******************************


From Amazon:
   The GetCompetitivePricingForSKU operation returns the current competitive pricing of a product, based on the SellerSKU and MarketplaceId that you specify. This operation returns pricing for active offer listings based on two pricing models: New Buy Box Price and Used Buy Box Price.
   Maximum: 20 SellerSKU values
  

.. code-block:: python

      response = products_api.get_competitive_pricing_for_sku(
         marketplace_id=my_marketplace,
         skus=["OO-NL0F-795Z"],
      )
  
  
Example:
========

Buy Box price

.. code-block:: python

      response.parsed.Product.CompetitivePricing.CompetitivePrices.CompetitivePrice.Price.LandedPrice.Amount
  
  

*******************************
`GetCompetitivePricingForASIN <https://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForASIN.html>`_
*******************************


From Amazon:
   Returns the current competitive price of a product, based on ASIN.

.. code-block:: python

      response = products_api.get_competitive_pricing_for_asin(
         marketplace_id=my_marketplace,
         asins=["B085G58KWT"],
      )


Same as GetCompetitivePricingForSKU above, but pass in a list of ASINs rather than SKUs.


*******************************
`GetLowestOfferListingsForSKU <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForSKU.html>`_
*******************************


From Amazon:
   Returns pricing information for the lowest-price active offer listings for up to 20 products, based on SellerSKU.

.. code-block:: python

      response = products_api.get_lowest_offer_listings_for_sku(
         marketplace_id=my_marketplace,
         skus=["OO-NL0F-795Z"],
         condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
      )


********************************
`GetLowestOfferListingsForASIN <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForASIN.html>`_
********************************


From Amazon:
   Returns pricing information for the lowest-price active offer listings for up to 20 products, based on ASIN.

.. code-block:: python

      response = products_api.get_lowest_offer_listings_for_asin(
         marketplace_id=my_marketplace,
         asins=["B085G58KWT"],
         condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
      )


*******************************
`GetLowestPricedOffersForSKU <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForSKU.html>`_
*******************************


From Amazon:
   Returns lowest priced offers for a single product, based on SellerSKU.

.. code-block:: python

      response = products_api.get_lowest_priced_offers_for_sku(
         marketplace_id=my_marketplace,
         skus=["OO-NL0F-795Z"],
         condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
      )


********************************
`GetLowestPricedOffersForASIN <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForASIN.html>`_
********************************


From Amazon:
   Returns lowest priced offers for a single product, based on ASIN.

.. code-block:: python

      response = products_api.get_lowest_priced_offers_for_asin(
         marketplace_id=my_marketplace,
         asins=["B085G58KWT"],
         condition="New" # Any, New, Used, Collectible, Refurbished, Club. Default = Any
      )


********************
`GetMyFeesEstimate <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyFeesEstimate.html>`_
********************


From Amazon:
   Returns the estimated fees for a list of products.

.. code-block:: python 

      my_price = MoneyType(amount=123.45, currency_code="GBP")
      my_shipping = MoneyType(amount=0.00, currency_code="GBP")
      my_product_price = PriceToEstimateFees(listing_price=my_price, shipping=my_shipping)
   
      my_product = FeesEstimateRequest(
         marketplace_id = my_marketplace,
         id_type="ASIN", #ASIN or SKU
         id_value="B07QR73T66",
         price_to_estimate_fees=my_product_price,
         is_amazon_fulfilled=False, #True or False
         identifier="request001", #any identifier you want
      )

      response = products_api.get_my_fees_estimate(my_product)


*******************
`GetMyPriceForSKU <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForSKU.html>`_
*******************


From Amazon:
   Returns pricing information for your own active offer listings, based on SellerSKU.

.. code-block:: python

      response = pr oducts_api.get_my_price_for_sku(
         marketplace_id = my_marketplace,
         skus = "OO-NL0F-795Z",
         condition = "New" # Any, New, Used, Collectible, Refurbished, Club. Default = All
      )



********************
`GetMyPriceForASIN <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForASIN.html>`_
********************


From Amazon:
   Returns pricing information for your own active offer listings, based on ASIN.

.. code-block:: python

      response = products_api.get_my_price_for_asin(
         marketplace_id = my_marketplace,
         asins = "B07QR73T66",
         condition = "New" # Any, New, Used, Collectible, Refurbished, Club. Default = All
      )


*****************************
`GetProductCategoriesForSKU <https://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForSKU.html>`_
*****************************

From Amazon:
   Returns the parent product categories that a product belongs to, based on SellerSKU.

.. code-block:: python

      response = products_api.get_product_categories_for_sku(
         marketplace_id = my_marketplace,
         sku = "OO-NL0F-795Z"
      )


******************************
`GetProductCategoriesForASIN <https://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForASIN.html>`_
******************************


From Amazon:
   Returns the parent product categories that a product belongs to, based on ASIN.

.. code-block:: python

      response = products_api.get_product_categories_for_asin(
         marketplace_id = my_marketplace,
         asin = "B07QR73T66"
      )
