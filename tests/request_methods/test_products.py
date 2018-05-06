"""
Tests for the Products API class.
"""
import unittest
import mws
from .utils import CommonRequestTestTools, transform_bool, transform_string


class ProductsTestCase(unittest.TestCase, CommonRequestTestTools):
    """
    Test cases for Products.
    """
    # TODO: Add remaining methods for Products

    def setUp(self):
        self.api = mws.Products(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN
        )
        self.api._test_request_params = True

    def test_list_matching_products(self):
        """
        ListMatchingProducts operation.
        """
        marketplace_id = 'ALDERAAN'
        query = 'hokey religions and ancient weapons'
        context_id = 'ArtsAndCrafts'
        params = self.api.list_matching_products(
            marketplace_id=marketplace_id,
            query=query,
            context_id=context_id
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'ListMatchingProducts')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['Query'], transform_string(query))
        self.assertEqual(params['QueryContextId'], context_id)

    def test_get_matching_product(self):
        """
        GetMatchingProduct operation.
        """
        marketplace_id = 'TATOOINE'
        asins = [
            'pibMZnNRoS',
            'nTuCCevqaZ',
        ]
        params = self.api.get_matching_product(
            marketplace_id=marketplace_id,
            asins=asins,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetMatchingProduct')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ASINList.ASIN.1'], asins[0])
        self.assertEqual(params['ASINList.ASIN.2'], asins[1])

    def test_get_matching_product_for_id(self):
        """
        GetMatchingProductForId operation.
        """
        marketplace_id = 'AGAMAR'
        type_ = 'GCID'
        ids = [
            'uwE7IoswAb',
            '3LslgSP3xN',
        ]
        params = self.api.get_matching_product_for_id(
            marketplace_id=marketplace_id,
            type_=type_,
            ids=ids,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetMatchingProductForId')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['IdType'], type_)
        self.assertEqual(params['IdList.Id.1'], ids[0])
        self.assertEqual(params['IdList.Id.2'], ids[1])

    def test_get_competitive_pricing_for_sku(self):
        """
        GetCompetitivePricingForSKU operation.
        """
        marketplace_id = 'MOONUS MANDEL'
        skus = [
            'diHXW9Y1h1',
            'IVnJJtgQ4n',
        ]
        params = self.api.get_competitive_pricing_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetCompetitivePricingForSKU')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['SellerSKUList.SellerSKU.1'], skus[0])
        self.assertEqual(params['SellerSKUList.SellerSKU.2'], skus[1])

    def test_get_competitive_pricing_for_asin(self):
        """
        GetCompetitivePricingForASIN operation.
        """
        marketplace_id = 'DAXAN BETA'
        asins = [
            '5RD1pXAd4U',
            'HXfSfZimui',
        ]
        params = self.api.get_competitive_pricing_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetCompetitivePricingForASIN')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ASINList.ASIN.1'], asins[0])
        self.assertEqual(params['ASINList.ASIN.2'], asins[1])

    def test_get_lowest_offer_listings_for_sku(self):
        """
        GetLowestOfferListingsForSKU operation.
        """
        marketplace_id = 'ENDOR'
        skus = [
            'XhPpwZTI3T',
            'JcaTGvCr4f',
        ]
        condition = "Beat up"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_offer_listings_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
            condition=condition,
            exclude_me=exclude_me
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetLowestOfferListingsForSKU')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], transform_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params['ExcludeMe'], 'true')
        self.assertEqual(params['SellerSKUList.SellerSKU.1'], skus[0])
        self.assertEqual(params['SellerSKUList.SellerSKU.2'], skus[1])

    def test_get_lowest_offer_listings_for_asin(self):
        """
        GetLowestOfferListingsForASIN operation.
        """
        marketplace_id = 'TANGENINE'
        asins = [
            'UkqjCE2qZG',
            'f7MTgxKIhk',
        ]
        condition = "Not too shabby"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_offer_listings_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
            condition=condition,
            exclude_me=exclude_me
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetLowestOfferListingsForASIN')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], transform_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params['ExcludeMe'], transform_bool(exclude_me))
        self.assertEqual(params['ASINList.ASIN.1'], asins[0])
        self.assertEqual(params['ASINList.ASIN.2'], asins[1])

    def test_get_lowest_priced_offers_for_sku(self):
        """
        GetLowestPricedOffersForSKU operation.
        """
        marketplace_id = 'TROIKEN'
        sku = 'r4IHCMtJXr'
        condition = "God-awful"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_priced_offers_for_sku(
            marketplace_id=marketplace_id,
            sku=sku,
            condition=condition,
            exclude_me=exclude_me
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetLowestPricedOffersForSKU')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], condition)
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params['ExcludeMe'], transform_bool(exclude_me))
        self.assertEqual(params['SellerSKU'], sku)

    def test_get_lowest_priced_offers_for_asin(self):
        """
        GetLowestPricedOffersForASIN operation.
        """
        marketplace_id = 'UMBARA'
        asin = 'krYUsW7loa'
        condition = "Acceptable"
        exclude_me = True
        # exclude_me_str = str(exclude_me)
        params = self.api.get_lowest_priced_offers_for_asin(
            marketplace_id=marketplace_id,
            asin=asin,
            condition=condition,
            exclude_me=exclude_me
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetLowestPricedOffersForASIN')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], transform_string(condition))
        # TODO when this fails later after "clean" implemented, test against str conversion instead
        # (use commented `exclude_me_str` above)
        self.assertEqual(params['ExcludeMe'], 'true')
        self.assertEqual(params['ASIN'], asin)

    # def test_get_my_fees_estimate(self):
    #     """
    #     GetMyFeesEstimate operation.
    #     """
    #     pass

    def test_get_my_price_for_sku(self):
        """
        GetMyPriceForSKU operation.
        """
        marketplace_id = 'ISOBE'
        skus = [
            'SjvAgfePtI',
            'oV0NG55kf2',
        ]
        condition = "Near-Mint Chocolate Chip"
        params = self.api.get_my_price_for_sku(
            marketplace_id=marketplace_id,
            skus=skus,
            condition=condition,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetMyPriceForSKU')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], transform_string(condition))
        self.assertEqual(params['SellerSKUList.SellerSKU.1'], skus[0])
        self.assertEqual(params['SellerSKUList.SellerSKU.2'], skus[1])

    def test_get_my_price_for_asin(self):
        """
        GetMyPriceForASIN operation.
        """
        marketplace_id = 'HEAP NINE'
        asins = [
            'NDILA3FP8d',
            'dI3VuY5p1P',
        ]
        condition = "Generally Specific"
        params = self.api.get_my_price_for_asin(
            marketplace_id=marketplace_id,
            asins=asins,
            condition=condition,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetMyPriceForASIN')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ItemCondition'], transform_string(condition))
        self.assertEqual(params['ASINList.ASIN.1'], asins[0])
        self.assertEqual(params['ASINList.ASIN.2'], asins[1])

    def test_get_product_categories_for_sku(self):
        """
        GetProductCategoriesForSKU operation.
        """
        marketplace_id = 'WEIRD STAR WARS PLANET 87'
        sku = "B3KpfAmBK8"
        params = self.api.get_product_categories_for_sku(
            marketplace_id=marketplace_id,
            sku=sku,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetProductCategoriesForSKU')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['SellerSKU'], sku)

    def test_get_product_categories_for_asin(self):
        """
        GetProductCategoriesForASIN operation.
        """
        marketplace_id = 'THAT WAS THE JOKE DOT JPEG'
        asin = "k1UOfaOWfa"
        params = self.api.get_product_categories_for_asin(
            marketplace_id=marketplace_id,
            asin=asin,
        )
        self.assert_common_params(params)
        self.assertEqual(params['Action'], 'GetProductCategoriesForASIN')
        self.assertEqual(params['MarketplaceId'], transform_string(marketplace_id))
        self.assertEqual(params['ASIN'], asin)
