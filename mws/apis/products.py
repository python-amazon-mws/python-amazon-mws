"""Amazon MWS Products API."""
from typing import List

from mws import MWS
from mws.models.products import FeesEstimateRequest
from mws.utils import enumerate_keyed_param
from mws.utils.params import coerce_to_bool
from mws.utils.params import enumerate_param

# DEPRECATION
from mws.utils.deprecation import kwargs_renamed_for_v11


class Products(MWS):
    """Amazon MWS Products API

    Docs:
    http://docs.developer.amazonservices.com/en_US/products/Products_Overview.html
    """

    URI = "/Products/2011-10-01"
    VERSION = "2011-10-01"
    NAMESPACE = "{http://mws.amazonservices.com/schema/Products/2011-10-01}"
    # NEXT_TOKEN_OPERATIONS = []

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("contextid", "context_id")]
    )
    def list_matching_products(self, marketplace_id, query, context_id=None):
        """Returns a list of products and their attributes, based on a search query.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html
        """
        return self.make_request(
            "ListMatchingProducts",
            {
                "MarketplaceId": marketplace_id,
                "Query": query,
                "QueryContextId": context_id,
            },
        )

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_matching_product(self, marketplace_id, asins):
        """Returns a list of products and their attributes, based on a list of ASIN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProduct.html
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetMatchingProduct", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_matching_product_for_id(self, marketplace_id, type_, ids):
        """Returns a list of products and their attributes, based on a list of
        ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html
        """
        data = {
            "MarketplaceId": marketplace_id,
            "IdType": type_,
        }
        data.update(enumerate_param("IdList.Id.", ids))
        return self.make_request("GetMatchingProductForId", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_competitive_pricing_for_sku(self, marketplace_id, skus):
        """Returns the current competitive price of a product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForSKU.html
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request("GetCompetitivePricingForSKU", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_competitive_pricing_for_asin(self, marketplace_id, asins):
        """Returns the current competitive price of a product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForASIN.html
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetCompetitivePricingForASIN", data)

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def get_lowest_offer_listings_for_sku(
        self, marketplace_id, skus, condition="Any", exclude_me=False
    ):
        """Returns pricing information for the lowest-price active offer listings for up to 20 products,
        based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForSKU.html
        """
        if exclude_me is not None:
            exclude_me = coerce_to_bool(exclude_me)
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        data.update(enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request("GetLowestOfferListingsForSKU", data)

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def get_lowest_offer_listings_for_asin(
        self, marketplace_id, asins, condition="Any", exclude_me=False
    ):
        """Returns pricing information for the lowest-price active offer listings for up to 20 products, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForASIN.html
        """
        if exclude_me is not None:
            exclude_me = coerce_to_bool(exclude_me)
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
            "ExcludeMe": exclude_me,
        }
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetLowestOfferListingsForASIN", data)

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def get_lowest_priced_offers_for_sku(
        self, marketplace_id, sku, condition="New", exclude_me=False
    ):
        """Returns lowest priced offers for a single product, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForSKU.html
        """
        if exclude_me is not None:
            exclude_me = coerce_to_bool(exclude_me)
        return self.make_request(
            "GetLowestPricedOffersForSKU",
            {
                "MarketplaceId": marketplace_id,
                "SellerSKU": sku,
                "ItemCondition": condition,
                "ExcludeMe": exclude_me,
            },
        )

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def get_lowest_priced_offers_for_asin(
        self, marketplace_id, asin, condition="New", exclude_me=False
    ):
        """Returns lowest priced offers for a single product, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForASIN.html
        """
        if exclude_me is not None:
            exclude_me = coerce_to_bool(exclude_me)
        return self.make_request(
            "GetLowestPricedOffersForASIN",
            {
                "MarketplaceId": marketplace_id,
                "ASIN": asin,
                "ItemCondition": condition,
                "ExcludeMe": exclude_me,
            },
        )

    def get_my_fees_estimate(
        self, fees_estimate: FeesEstimateRequest, *fees_estimates: FeesEstimateRequest
    ):
        """Returns the estimated fees for a list of products.

        Docs:
        https://docs.developer.amazonservices.com/en_US/products/Products_GetMyFeesEstimate.html
        """
        estimates = [fees_estimate.to_dict()] + [fe.to_dict() for fe in fees_estimates]
        data = enumerate_keyed_param(
            "FeesEstimateRequestList.FeesEstimateRequest.", estimates
        )
        return self.make_request("GetMyFeesEstimate", data, method="POST")

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_my_price_for_sku(self, marketplace_id, skus, condition=None):
        """Returns pricing information for your own offer listings, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForSKU.html
        """
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request("GetMyPriceForSKU", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_my_price_for_asin(self, marketplace_id, asins, condition=None):
        """Returns pricing information for your own offer listings, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForASIN.html
        """
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetMyPriceForASIN", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_product_categories_for_sku(self, marketplace_id, sku):
        """Returns the parent product categories that a product belongs to, based on SellerSKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForSKU.html
        """
        return self.make_request(
            "GetProductCategoriesForSKU",
            {"MarketplaceId": marketplace_id, "SellerSKU": sku},
        )

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_product_categories_for_asin(self, marketplace_id, asin):
        """Returns the parent product categories that a product belongs to, based on ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForASIN.html
        """
        return self.make_request(
            "GetProductCategoriesForASIN",
            {"MarketplaceId": marketplace_id, "ASIN": asin},
        )
