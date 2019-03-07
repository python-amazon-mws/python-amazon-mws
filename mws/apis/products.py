"""
Amazon MWS Products API
"""
from __future__ import absolute_import
# import warnings

from ..mws import MWS
from .. import utils


class Products(MWS):
    """
    Amazon MWS Products API

    Docs:
    http://docs.developer.amazonservices.com/en_US/products/Products_Overview.html
    """
    URI = '/Products/2011-10-01'
    VERSION = '2011-10-01'
    NAMESPACE = '{http://mws.amazonservices.com/schema/Products/2011-10-01}'
    # NEXT_TOKEN_OPERATIONS = []

    def list_matching_products(self, marketplace_id, query, context_id=None):
        """
        Returns a list of products and their attributes, based on a search query.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html
        """
        data = {
            'Action': 'ListMatchingProducts',
            'MarketplaceId': marketplace_id,
            'Query': query,
            'QueryContextId': context_id,
        }
        return self.make_request(data)

    def get_matching_product(self, marketplace_id, asins):
        """
        Returns a list of products and their attributes, based on a list of ASIN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProduct.html
        """
        data = {
            'Action': 'GetMatchingProduct',
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_matching_product_for_id(self, marketplace_id, type_, ids):
        """
        Returns a list of products and their attributes, based on a list of
        ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html
        """
        data = {
            'Action': 'GetMatchingProductForId',
            'MarketplaceId': marketplace_id,
            'IdType': type_,
        }

        data.update(utils.enumerate_param('IdList.Id.', ids))
        return self.make_request(data)

    def get_competitive_pricing_for_sku(self, marketplace_id, skus):
        """
        Returns the current competitive price of a product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForSKU.html
        """
        data = {
            'Action': 'GetCompetitivePricingForSKU',
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_competitive_pricing_for_asin(self, marketplace_id, asins):
        """
        Returns the current competitive price of a product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForASIN.html
        """
        data = {
            'Action': 'GetCompetitivePricingForASIN',
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_lowest_offer_listings_for_sku(self, marketplace_id, skus, condition="Any", exclude_me="false"):
        """
        Returns pricing information for the lowest-price active offer listings for up to 20 products,
        based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForSKU.html
        """
        data = {
            'Action': 'GetLowestOfferListingsForSKU',
            'MarketplaceId': marketplace_id,
            'ItemCondition': condition,
            'ExcludeMe': exclude_me,
        }
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_lowest_offer_listings_for_asin(self, marketplace_id, asins, condition="Any", exclude_me="false"):
        """
        Returns pricing information for the lowest-price active offer listings for up to 20 products, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForASIN.html
        """
        data = {
            'Action': 'GetLowestOfferListingsForASIN',
            'MarketplaceId': marketplace_id,
            'ItemCondition': condition,
            'ExcludeMe': exclude_me,
        }
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_lowest_priced_offers_for_sku(self, marketplace_id, sku, condition="New", exclude_me="false"):
        """
        Returns lowest priced offers for a single product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForSKU.html
        """
        data = {
            'Action': 'GetLowestPricedOffersForSKU',
            'MarketplaceId': marketplace_id,
            'SellerSKU': sku,
            'ItemCondition': condition,
            'ExcludeMe': exclude_me,
        }
        return self.make_request(data)

    def get_lowest_priced_offers_for_asin(self, marketplace_id, asin, condition="New", exclude_me="false"):
        """
        Returns lowest priced offers for a single product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForASIN.html
        """
        data = {
            'Action': 'GetLowestPricedOffersForASIN',
            'MarketplaceId': marketplace_id,
            'ASIN': asin,
            'ItemCondition': condition,
            'ExcludeMe': exclude_me,
        }
        return self.make_request(data)

    # # # TODO add this
    # def get_my_fees_estimate(self):
    #     pass

    def get_my_price_for_sku(self, marketplace_id, skus, condition=None):
        """
        Returns pricing information for your own offer listings, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForSKU.html
        """
        data = {
            'Action': 'GetMyPriceForSKU',
            'MarketplaceId': marketplace_id,
            'ItemCondition': condition,
        }
        data.update(utils.enumerate_param('SellerSKUList.SellerSKU.', skus))
        return self.make_request(data)

    def get_my_price_for_asin(self, marketplace_id, asins, condition=None):
        """
        Returns pricing information for your own offer listings, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForASIN.html
        """
        data = {
            'Action': 'GetMyPriceForASIN',
            'MarketplaceId': marketplace_id,
            'ItemCondition': condition,
        }
        data.update(utils.enumerate_param('ASINList.ASIN.', asins))
        return self.make_request(data)

    def get_product_categories_for_sku(self, marketplace_id, sku):
        """
        Returns the parent product categories that a product belongs to, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForSKU.html
        """
        data = {
            'Action': 'GetProductCategoriesForSKU',
            'MarketplaceId': marketplace_id,
            'SellerSKU': sku,
        }
        return self.make_request(data)

    def get_product_categories_for_asin(self, marketplace_id, asin):
        """
        Returns the parent product categories that a product belongs to, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForASIN.html
        """
        data = {
            'Action': 'GetProductCategoriesForASIN',
            'MarketplaceId': marketplace_id,
            'ASIN': asin,
        }
        return self.make_request(data)
