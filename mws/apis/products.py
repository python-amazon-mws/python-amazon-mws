"""Amazon MWS Products API."""
from typing import List, Optional, Union

from mws import MWS
from mws.models.products import FeesEstimateRequest
from mws.utils import enumerate_keyed_param
from mws.utils.params import coerce_to_bool
from mws.utils.params import enumerate_param
from mws.utils.types import StrOrListStr, MarketplaceEnumOrStr

# DEPRECATION
from mws.utils.deprecation import kwargs_renamed_for_v11


class Products(MWS):
    """Amazon MWS Products API

    `MWS Docs: Products API Overview
    <https://docs.developer.amazonservices.com/en_US/products/Products_Overview.html>`_
    """

    URI = "/Products/2011-10-01"
    VERSION = "2011-10-01"
    NAMESPACE = "{http://mws.amazonservices.com/schema/Products/2011-10-01}"
    # NEXT_TOKEN_OPERATIONS = []

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("contextid", "context_id")]
    )
    def list_matching_products(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        query: str,
        context_id: Optional[str] = None,
    ):
        """Returns a list of products and their attributes, based on a search query.

        `MWS Docs: ListMatchingProducts
        <https://docs.developer.amazonservices.com/en_US/products/Products_ListMatchingProducts.html>`_
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
    def get_matching_product(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asins: StrOrListStr,
    ):
        """Returns a list of products and their attributes, based on a list of ASIN values.

        `MWS Docs: GetMatchingProduct
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProduct.html>`_
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetMatchingProduct", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_matching_product_for_id(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        type_: str,
        ids: StrOrListStr,
    ):
        """Returns a list of products and their attributes, based on a list of
        ASIN, GCID, SellerSKU, UPC, EAN, ISBN, and JAN values.

        `MWS Docs: GetMatchingProductForId
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetMatchingProductForId.html>`_
        """
        data = {
            "MarketplaceId": marketplace_id,
            "IdType": type_,
        }
        data.update(enumerate_param("IdList.Id.", ids))
        return self.make_request("GetMatchingProductForId", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_competitive_pricing_for_sku(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        skus: StrOrListStr,
    ):
        """Returns the current competitive price of a product, based on SellerSKU.

        `MWS Docs: GetCompetitivePricingForSKU
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForSKU.html>`_
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request("GetCompetitivePricingForSKU", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_competitive_pricing_for_asin(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asins: StrOrListStr,
    ):
        """Returns the current competitive price of a product, based on ASIN.

        `MWS Docs: GetCompetitivePricingForASIN
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetCompetitivePricingForASIN.html>`_
        """
        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetCompetitivePricingForASIN", data)

    @kwargs_renamed_for_v11(
        [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def get_lowest_offer_listings_for_sku(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        skus: StrOrListStr,
        condition: str = "Any",
        exclude_me: bool = False,
    ):
        """Returns pricing information for the lowest-price active offer listings for up to 20 products,
        based on SellerSKU.

        `MWS Docs: GetLowestOfferListingsForSKU
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForSKU.html>`_
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
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asins: StrOrListStr,
        condition: str = "Any",
        exclude_me: bool = False,
    ):
        """Returns pricing information for the lowest-price active offer listings for up to 20 products, based on ASIN.

        `MWS Docs: GetLowestOfferListingsForASIN
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestOfferListingsForASIN.html>`_
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
        self,
        marketplace_id: MarketplaceEnumOrStr,
        sku: str,
        condition: str = "New",
        exclude_me: bool = False,
    ):
        """Returns lowest priced offers for a single product, based on SellerSKU.

        `MWS Docs: GetLowestPricedOffersForSKU
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForSKU.html>`_
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
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asin: str,
        condition: str = "New",
        exclude_me: bool = False,
    ):
        """Returns lowest priced offers for a single product, based on ASIN.

        `MWS Docs: GetLowestPricedOffersForASIN
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetLowestPricedOffersForASIN.html>`_
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
        self,
        fees_estimate: FeesEstimateRequest,
        *fees_estimates: FeesEstimateRequest,
    ):
        """Returns the estimated fees for a list of products.

        `MWS Docs: GetMyFeesEstimate
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyFeesEstimate.html>`_
        """
        estimates = [fees_estimate.to_params()] + [
            fe.to_params() for fe in fees_estimates
        ]
        data = enumerate_keyed_param(
            "FeesEstimateRequestList.FeesEstimateRequest.", estimates
        )
        return self.make_request("GetMyFeesEstimate", data, method="POST")

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_my_price_for_sku(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        skus: StrOrListStr,
        condition: Optional[str] = None,
    ):
        """Returns pricing information for your own offer listings, based on SellerSKU.

        `MWS Docs: GetMyPriceForSKU
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForSKU.html>`_
        """
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(enumerate_param("SellerSKUList.SellerSKU.", skus))
        return self.make_request("GetMyPriceForSKU", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_my_price_for_asin(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asins: StrOrListStr,
        condition: Optional[str] = None,
    ):
        """Returns pricing information for your own offer listings, based on ASIN.

        `MWS Docs: GetMyPriceForASIN
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetMyPriceForASIN.html>`_
        """
        data = {
            "MarketplaceId": marketplace_id,
            "ItemCondition": condition,
        }
        data.update(enumerate_param("ASINList.ASIN.", asins))
        return self.make_request("GetMyPriceForASIN", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_product_categories_for_sku(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        sku: str,
    ):
        """Returns the parent product categories that a product belongs to, based on SellerSKU.

        `MWS Docs: GetProductCategoriesForSKU
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForSKU.html>`_
        """
        data = {
            "MarketplaceId": marketplace_id,
            "SellerSKU": sku,
        }
        return self.make_request("GetProductCategoriesForSKU", data)

    @kwargs_renamed_for_v11([("marketplaceid", "marketplace_id")])
    def get_product_categories_for_asin(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        asin: str,
    ):
        """Returns the parent product categories that a product belongs to, based on ASIN.

        `MWS Docs: GetProductCategoriesForASIN
        <https://docs.developer.amazonservices.com/en_US/products/Products_GetProductCategoriesForASIN.html>`_
        """
        data = {
            "MarketplaceId": marketplace_id,
            "ASIN": asin,
        }
        return self.make_request("GetProductCategoriesForASIN", data)
