"""Tests covering miscellaneous utility functions found throughout project."""

from mws.mws import calc_request_description
from mws.utils import calc_md5
from mws.models.products import ListingPrice, ShippingPrice, \
    PriceToEstimateFees, FeesEstimateRequestItem


def test_calc_md5():
    assert calc_md5(b"mws") == b"mA5nPbh1CSx9M3dbkr3Cyg=="


def test_calc_request_description(cred_access_key, cred_account_id):
    request_description = calc_request_description(
        {
            "AWSAccessKeyId": cred_access_key,
            "Markets": cred_account_id,
            "SignatureVersion": "2",
            "Timestamp": "2017-08-12T19%3A40%3A35Z",
            "Version": "2017-01-01",
            "SignatureMethod": "HmacSHA256",
        }
    )
    assert not request_description.startswith("&")
    assert (
        request_description
        == "AWSAccessKeyId="
        + cred_access_key
        + "&Markets="
        + cred_account_id
        + "&SignatureMethod=HmacSHA256"
        "&SignatureVersion=2"
        "&Timestamp=2017-08-12T19%3A40%3A35Z"
        "&Version=2017-01-01"
    )


def test_fees_estimates_data_classes():
    marketplace_id = 'ATVPDKIKX0DER'
    sku = 'cool-product'
    sp = ShippingPrice(currency_code='USD', amount=0)

    lp = ListingPrice(currency_code='USD', amount=15.14)

    pte = PriceToEstimateFees(lp, sp)

    feri = FeesEstimateRequestItem(
        marketplace_id, 'SellerSKU', sku, is_amazon_fulfilled=True,
        identifier=sku, price_to_estimate_fees=pte)
    assert feri.serialize() == {
        'MarketplaceId': 'ATVPDKIKX0DER',
        'IdType': 'SellerSKU',
        'IdValue': 'cool-product',
        'IsAmazonFulfilled': True,
        'Identifier': 'cool-product',
        'PriceToEstimateFees.ListingPrice.CurrencyCode': 'USD',
        'PriceToEstimateFees.ListingPrice.Amount': 15.14,
        'PriceToEstimateFees.Shipping.CurrencyCode': 'USD',
        'PriceToEstimateFees.Shipping.Amount': 0,
    }
