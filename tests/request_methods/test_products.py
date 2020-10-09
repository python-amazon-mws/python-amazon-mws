"""Tests for the Products API class."""

import unittest
import mws
from mws.utils import clean_bool, clean_string

from .utils import CommonAPIRequestTools
from mws.models.products import (
    MoneyType,
    PriceToEstimateFees,
    FeesEstimateRequest,
)


class ProductsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Products."""

    api_class = mws.Products

    # TODO: Add remaining methods for Products

    def test_list_matching_products(self):
        """ListMatchingProducts operation."""
        marketplace_id = "ALDERAAN"
        query = "hokey religions and ancient weapons"
        context_id = "ArtsAndCrafts"
        params = self.api.list_matching_products(
            marketplace_id=marketplace_id, query=query, context_id=context_id
        )
        self.assert_common_params(params, action="ListMatchingProducts")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["Query"], clean_string(query))
        self.assertEqual(params["QueryContextId"], context_id)

    def test_get_matching_product(self):
        """GetMatchingProduct operation."""
        marketplace_id = "TATOOINE"
        asins = [
            "pibMZnNRoS",
            "nTuCCevqaZ",
        ]
        params = self.api.get_matching_product(
            marketplace_id=marketplace_id,
            asins=asins,
        )
        self.assert_common_params(params, action="GetMatchingProduct")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ASINList.ASIN.1"], asins[0])
        self.assertEqual(params["ASINList.ASIN.2"], asins[1])

    def test_get_matching_product_for_id(self):
        """GetMatchingProductForId operation."""
        marketplace_id = "AGAMAR"
        type_ = "GCID"
        ids = [
            "uwE7IoswAb",
            "3LslgSP3xN",
        ]
        params = self.api.get_matching_product_for_id(
            marketplace_id=marketplace_id,
            type_=type_,
            ids=ids,
        )
        self.assert_common_params(params, action="GetMatchingProductForId")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["IdType"], type_)
        self.assertEqual(params["IdList.Id.1"], ids[0])
        self.assertEqual(params["IdList.Id.2"], ids[1])

    def test_get_competitive_pricing_for_sku(self):
        """GetCompetitivePricingForSKU operation."""
        marketplace_id = "MOONUS MANDEL"
        skus = [
            "diHXW9Y1h1",
            "IVnJJtgQ4n",
        ]
        params = self.api.get_competitive_pricing_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
        )
        self.assert_common_params(params, action="GetCompetitivePricingForSKU")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["SellerSKUList.SellerSKU.1"], skus[0])
        self.assertEqual(params["SellerSKUList.SellerSKU.2"], skus[1])

    def test_get_competitive_pricing_for_asin(self):
        """GetCompetitivePricingForASIN operation."""
        marketplace_id = "DAXAN BETA"
        asins = [
            "5RD1pXAd4U",
            "HXfSfZimui",
        ]
        params = self.api.get_competitive_pricing_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
        )
        self.assert_common_params(params, action="GetCompetitivePricingForASIN")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ASINList.ASIN.1"], asins[0])
        self.assertEqual(params["ASINList.ASIN.2"], asins[1])

    def test_get_lowest_offer_listings_for_sku(self):
        """GetLowestOfferListingsForSKU operation."""
        marketplace_id = "ENDOR"
        skus = [
            "XhPpwZTI3T",
            "JcaTGvCr4f",
        ]
        condition = "Beat up"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_offer_listings_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
            condition=condition,
            exclude_me=exclude_me,
        )
        self.assert_common_params(params, action="GetLowestOfferListingsForSKU")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], clean_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params["ExcludeMe"], "true")
        self.assertEqual(params["SellerSKUList.SellerSKU.1"], skus[0])
        self.assertEqual(params["SellerSKUList.SellerSKU.2"], skus[1])

    def test_get_lowest_offer_listings_for_asin(self):
        """GetLowestOfferListingsForASIN operation."""
        marketplace_id = "TANGENINE"
        asins = [
            "UkqjCE2qZG",
            "f7MTgxKIhk",
        ]
        condition = "Not too shabby"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_offer_listings_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
            condition=condition,
            exclude_me=exclude_me,
        )
        self.assert_common_params(params, action="GetLowestOfferListingsForASIN")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], clean_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params["ExcludeMe"], clean_bool(exclude_me))
        self.assertEqual(params["ASINList.ASIN.1"], asins[0])
        self.assertEqual(params["ASINList.ASIN.2"], asins[1])

    def test_get_lowest_priced_offers_for_sku(self):
        """GetLowestPricedOffersForSKU operation."""
        marketplace_id = "TROIKEN"
        sku = "r4IHCMtJXr"
        condition = "God-awful"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_priced_offers_for_sku(
            marketplace_id=marketplace_id,
            sku=sku,
            condition=condition,
            exclude_me=exclude_me,
        )
        self.assert_common_params(params, action="GetLowestPricedOffersForSKU")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], condition)
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params["ExcludeMe"], clean_bool(exclude_me))
        self.assertEqual(params["SellerSKU"], sku)

    def test_get_lowest_priced_offers_for_asin(self):
        """GetLowestPricedOffersForASIN operation."""
        marketplace_id = "UMBARA"
        asin = "krYUsW7loa"
        condition = "Acceptable"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_priced_offers_for_asin(
            marketplace_id=marketplace_id,
            asin=asin,
            condition=condition,
            exclude_me=exclude_me,
        )
        self.assert_common_params(params, action="GetLowestPricedOffersForASIN")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], clean_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params["ExcludeMe"], "true")
        self.assertEqual(params["ASIN"], asin)

    def test_get_my_price_for_sku(self):
        """GetMyPriceForSKU operation."""
        marketplace_id = "ISOBE"
        skus = [
            "SjvAgfePtI",
            "oV0NG55kf2",
        ]
        condition = "Near-Mint Chocolate Chip"
        params = self.api.get_my_price_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
            condition=condition,
        )
        self.assert_common_params(params, action="GetMyPriceForSKU")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], clean_string(condition))
        self.assertEqual(params["SellerSKUList.SellerSKU.1"], skus[0])
        self.assertEqual(params["SellerSKUList.SellerSKU.2"], skus[1])

    def test_get_my_price_for_asin(self):
        """GetMyPriceForASIN operation."""
        marketplace_id = "HEAP NINE"
        asins = [
            "NDILA3FP8d",
            "dI3VuY5p1P",
        ]
        condition = "Generally Specific"
        params = self.api.get_my_price_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
            condition=condition,
        )
        self.assert_common_params(params, action="GetMyPriceForASIN")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ItemCondition"], clean_string(condition))
        self.assertEqual(params["ASINList.ASIN.1"], asins[0])
        self.assertEqual(params["ASINList.ASIN.2"], asins[1])

    def test_get_product_categories_for_sku(self):
        """GetProductCategoriesForSKU operation."""
        marketplace_id = "WEIRD STAR WARS PLANET 87"
        sku = "B3KpfAmBK8"
        params = self.api.get_product_categories_for_sku(
            marketplace_id=marketplace_id,
            sku=sku,
        )
        self.assert_common_params(params, action="GetProductCategoriesForSKU")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["SellerSKU"], sku)

    def test_get_product_categories_for_asin(self):
        """GetProductCategoriesForASIN operation."""
        marketplace_id = "THAT WAS THE JOKE DOT JPEG"
        asin = "k1UOfaOWfa"
        params = self.api.get_product_categories_for_asin(
            marketplace_id=marketplace_id,
            asin=asin,
        )
        self.assert_common_params(params, action="GetProductCategoriesForASIN")
        self.assertEqual(params["MarketplaceId"], clean_string(marketplace_id))
        self.assertEqual(params["ASIN"], asin)

    def test_get_my_fees_estimate(self):
        """GetMyFeesEstimate operation."""
        marketplace_id = "ATVPDKIKX0DER"

        sku1 = "cool-product"
        fees1 = PriceToEstimateFees(
            listing_price=MoneyType(amount=15.14, currency_code="USD"),
            shipping=MoneyType(amount=0, currency_code="USD"),
        )
        estimate1 = FeesEstimateRequest(
            marketplace_id=marketplace_id,
            id_type="SellerSKU",
            id_value=sku1,
            is_amazon_fulfilled=True,
            identifier=sku1,
            price_to_estimate_fees=fees1,
        )

        sku2 = "cool-product-2"
        fees2 = PriceToEstimateFees(
            listing_price=MoneyType(amount=2.2, currency_code="USD"),
            shipping=MoneyType(currency_code="USD", amount=2),
        )
        estimate2 = FeesEstimateRequest(
            marketplace_id=marketplace_id,
            id_type="SellerSKU",
            id_value=sku2,
            is_amazon_fulfilled=False,
            identifier=sku2,
            price_to_estimate_fees=fees2,
        )

        params = self.api.get_my_fees_estimate(estimate1, estimate2)
        self.assert_common_params(params, action="GetMyFeesEstimate")

        # These keys are long and unreadable, so split them up.
        # All of them start like so, so break that part off.
        partial = "FeesEstimateRequestList.FeesEstimateRequest."
        expected = {
            "1.MarketplaceId": marketplace_id,
            "1.IdType": "SellerSKU",
            "1.IdValue": sku1,
            "1.IsAmazonFulfilled": "true",
            "1.Identifier": sku1,
            "1.PriceToEstimateFees.ListingPrice.CurrencyCode": "USD",
            "1.PriceToEstimateFees.ListingPrice.Amount": "15.14",
            "1.PriceToEstimateFees.Shipping.CurrencyCode": "USD",
            "1.PriceToEstimateFees.Shipping.Amount": "0",
            "2.MarketplaceId": marketplace_id,
            "2.IdType": "SellerSKU",
            "2.IdValue": sku2,
            "2.IsAmazonFulfilled": "false",
            "2.Identifier": sku2,
            "2.PriceToEstimateFees.ListingPrice.CurrencyCode": "USD",
            "2.PriceToEstimateFees.ListingPrice.Amount": "2.2",
            "2.PriceToEstimateFees.Shipping.CurrencyCode": "USD",
            "2.PriceToEstimateFees.Shipping.Amount": "2",
        }

        for key, val in expected.items():
            # join the partial with the "key" of expected to get the full key.
            full_key = partial + key
            assert params[full_key] == val
