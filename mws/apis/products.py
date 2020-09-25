"""Amazon MWS Products API."""

from mws import MWS, utils


class Products(MWS):
    """
    Amazon MWS Products API

    Docs:
    http://docs.developer.amazonservices.com/en_US/products/Products_Overview.html
    """

    URI = "/Products/2011-10-01"
    VERSION = "2011-10-01"
    NAMESPACE = "{http://mws.amazonservices.com/schema/Products/2011-10-01}"
    # NEXT_TOKEN_OPERATIONS = []

    def list_matching_products(self, marketplace_id, query, context_id=None):
        """
        Returns a list of products and their attributes, based on a search query.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html
        """
        data = {
            "Action": "ListMatchingProducts",
            "MarketplaceId": marketplace_id,
            "Query": query,
            "QueryContextId": context_id,
        }
        return self.make_request(data)

    def get_matching_product(self, marketplace_id, asins):
        """
        Returns a list of products and their attributes, based on a list of ASIN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProduct.html
        """
        data = {
            "Action": "GetMatchingProduct",
            "MarketplaceId": marketplace_id,
        }
        data.update(utils.enumerate_param("ASINList.ASIN.", asins))
        return self.make_request(data)

    def get_matching_product_for_id(self, marketplace_id, type_, ids):
        """
        Returns a list of products and their attributes, based on a list of
        ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html
        """
        data = {
            "Action": "GetMatchingProductForId",
            "MarketplaceId": marketplace_id,
            "IdType": type_,
        }

        data.update(utils.enumerate_param("IdList.Id.", ids))
        return self.make_request(data)

    def get_competitive_pricing_for_sku(self, marketplace_id, skus):
        """
        Returns the current competitive price of a product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForSKU.html
        """
        data = {
            "Action": "GetCompetitivePricingForSKU",
            "MarketplaceId": marketplace_id,
        }
        data.update(utils.enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request(data)

    def get_competitive_pricing_for_asin(self, marketplace_id, asins):
        """
        Returns the current competitive price of a product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForASIN.html
        """
        data = {
            "Action": "GetCompetitivePricingForASIN",
            "MarketplaceId": marketplace_id,
        }
        data.update(utils.enumerate_param("ASINList.ASIN.", asins))
        return self.make_request(data)

    def get_lowest_offer_listings_for_sku(
        self, marketplace_id, skus, condition="Any", exclude_me="false"
    ):
        """
        Returns pricing information for the lowest-price active offer listings for up to 20 products,
        based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForSKU.html
        """
        data = {
            "Action": "GetLowestOfferListingsForSKU",
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        data.update(utils.enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request(data)

    def get_lowest_offer_listings_for_asin(
        self, marketplace_id, asins, condition="Any", exclude_me="false"
    ):
        """
        Returns pricing information for the lowest-price active offer listings for up to 20 products, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForASIN.html
        """
        data = {
            "Action": "GetLowestOfferListingsForASIN",
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        data.update(utils.enumerate_param("ASINList.ASIN.", asins))
        return self.make_request(data)

    def get_lowest_priced_offers_for_sku(
        self, marketplace_id, sku, condition="New", exclude_me="false"
    ):
        """
        Returns lowest priced offers for a single product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForSKU.html
        """
        data = {
            "Action": "GetLowestPricedOffersForSKU",
            "MarketplaceId": marketplace_id,
            "SellerSKU": sku,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        return self.make_request(data)

    def get_lowest_priced_offers_for_asin(
        self, marketplace_id, asin, condition="New", exclude_me="false"
    ):
        """
        Returns lowest priced offers for a single product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForASIN.html
        """
        data = {
            "Action": "GetLowestPricedOffersForASIN",
            "MarketplaceId": marketplace_id,
            "ASIN": asin,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        return self.make_request(data)

    def get_my_fees_estimate(
        self, marketplace_id, id_type, id_value, is_amazon_fulfilled, identifier, listing_price, listing_price_currency_code
    ):

        """
        Each argument must be a list, up to a length of 20, with id_value (number of ASINs or SellerSKUs) determining how many requests are made.
        Options: 
            A single element list which repeats, or
            A list of equal length as id_value for a one to one relationship

        Example:
            marketplace_id = ['A1F83G8C2ARO7P']
            id_value = ['B082YTKC47', 'B07WGJ9JGP', 'B01LXP5TXI']
            id_type = ['ASIN']
            is_amazon_fulfilled = [True, False, True]
            identifier = ['request1', 'request2', 'request3']
            listing_price = [9, 16.42, 2.99]
            listing_price_currency_code = ['GBP']

        Example 2:
            marketplace_id = ['A1F83G8C2ARO7P', 'ATVPDKIKX0DER', 'A13V1IB3VIYZZH']
            id_value = ['B082YTKC47', 'B07WGJ9JGP', 'B01-LXP-TXI6']
            id_type = ['ASIN', 'ASIN', 'SellerSKU']
            is_amazon_fulfilled = [True]
            identifier = ['Fee requests']
            listing_price = [19]
            listing_price_currency_code = ['GBP', 'USD', 'EUR']
            
            
        Returns Amazon Fees for ASINs and SellerSKUs specified.

        Docs:
        https://docs.developer.amazonservices.com/en_UK/products/Products_GetMyFeesEstimate.html

        """
        
        data = {
            "Action": "GetMyFeesEstimate",
        }

        values = []
        for i in range(len(id_value)):
            values_dict = dict()

            try:
                values_dict['MarketplaceId'] = marketplace_id[i]
            except IndexError:
                values_dict['MarketplaceId'] = marketplace_id[0]
                
            try:
                values_dict['IdType'] = id_type[i]
            except IndexError:
                values_dict['IdType'] = id_type[0]
            
            try:
                values_dict['IdValue'] = id_value[i]
            except IndexError:
                values_dict['IdValue'] = id_value[0]

            try:
                values_dict['IsAmazonFulfilled'] = is_amazon_fulfilled[i]
            except IndexError:
                values_dict['IsAmazonFulfilled'] = is_amazon_fulfilled[0]
            
            try:
                values_dict['Identifier'] = identifier[i]
            except IndexError:
                values_dict['Identifier'] = identifier[0]
            
            try:
                values_dict['PriceToEstimateFees.ListingPrice.Amount'] = listing_price[i]
            except IndexError:
                values_dict['PriceToEstimateFees.ListingPrice.Amount'] = listing_price[0]

            try:
                values_dict['PriceToEstimateFees.ListingPrice.CurrencyCode'] = listing_price_currency_code[i]
            except IndexError:
                values_dict['PriceToEstimateFees.ListingPrice.CurrencyCode'] = listing_price_currency_code[0]
            
            values.append(values_dict)

        data.update(utils.enumerate_keyed_param("FeesEstimateRequestList.FeesEstimateRequest.", values))
        return self.make_request(data)

    def get_my_price_for_sku(self, marketplace_id, skus, condition=None):
        """
        Returns pricing information for your own offer listings, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForSKU.html
        """
        data = {
            "Action": "GetMyPriceForSKU",
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(utils.enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request(data)

    def get_my_price_for_asin(self, marketplace_id, asins, condition=None):
        """
        Returns pricing information for your own offer listings, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForASIN.html
        """
        data = {
            "Action": "GetMyPriceForASIN",
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(utils.enumerate_param("ASINList.ASIN.", asins))
        return self.make_request(data)

    def get_product_categories_for_sku(self, marketplace_id, sku):
        """
        Returns the parent product categories that a product belongs to, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForSKU.html
        """
        data = {
            "Action": "GetProductCategoriesForSKU",
            "MarketplaceId": marketplace_id,
            "SellerSKU": sku,
        }
        return self.make_request(data)

    def get_product_categories_for_asin(self, marketplace_id, asin):
        """
        Returns the parent product categories that a product belongs to, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForASIN.html
        """
        data = {
            "Action": "GetProductCategoriesForASIN",
            "MarketplaceId": marketplace_id,
            "ASIN": asin,
        }
        return self.make_request(data)
