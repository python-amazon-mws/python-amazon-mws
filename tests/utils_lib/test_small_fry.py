"""Tests covering miscellaneous utility functions found throughout project."""

from mws.models.products import FeesEstimateRequest, MoneyType, PriceToEstimateFees
from mws.mws import canonicalized_query_string
from mws.utils import calc_md5


def test_calc_md5():
    assert calc_md5(b"mws") == b"mA5nPbh1CSx9M3dbkr3Cyg=="


def test_canonicalized_query_string():
    canonical_query = canonicalized_query_string(
        {
            "AWSAccessKeyId": "MY_ACCESS_KEY",
            "Markets": "MY_ACCOUNT_ID",
            "SignatureVersion": "2",
            "Timestamp": "2017-08-12T19:40:35Z",
            "Version": "2017-01-01",
            "SignatureMethod": "HmacSHA256",
        }
    )
    assert not canonical_query.startswith("&")
    assert canonical_query == (
        "AWSAccessKeyId=MY_ACCESS_KEY"
        "&Markets=MY_ACCOUNT_ID"
        "&SignatureMethod=HmacSHA256"
        "&SignatureVersion=2"
        "&Timestamp=2017-08-12T19%3A40%3A35Z"
        "&Version=2017-01-01"
    )


def test_fees_estimates_data_classes():
    marketplace_id = "ATVPDKIKX0DER"
    sku = "cool-product"
    fees = PriceToEstimateFees(
        listing_price=MoneyType(amount=15.14, currency_code="USD"),
        shipping=MoneyType(amount=0, currency_code="USD"),
    )

    estimate_req = FeesEstimateRequest(
        marketplace_id,
        "SellerSKU",
        sku,
        is_amazon_fulfilled=True,
        identifier=sku,
        price_to_estimate_fees=fees,
    )
    assert estimate_req.to_params() == {
        "MarketplaceId": "ATVPDKIKX0DER",
        "IdType": "SellerSKU",
        "IdValue": "cool-product",
        "IsAmazonFulfilled": True,
        "Identifier": "cool-product",
        "PriceToEstimateFees.ListingPrice.CurrencyCode": "USD",
        "PriceToEstimateFees.ListingPrice.Amount": 15.14,
        "PriceToEstimateFees.Shipping.CurrencyCode": "USD",
        "PriceToEstimateFees.Shipping.Amount": 0,
    }
