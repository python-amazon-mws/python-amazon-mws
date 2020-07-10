"""
Tests for the mws.MWS class and Marketplaces.
"""
import pytest
from mws.mws import MWSError, MWS, Marketplaces

mwscred = ['a', 'b', 'c']


def test_notvalid_region():
    with pytest.raises(MWSError):
        MWS(region='ERROR', *mwscred)


def test_regionparameter():
    api = MWS(region='AE', *mwscred)
    assert api.domain == 'https://mws.amazonservices.ae'
    api = MWS(region='AU', *mwscred)
    assert api.domain == 'https://mws.amazonservices.com.au'
    api = MWS(region='BR', *mwscred)
    assert api.domain == 'https://mws.amazonservices.com'
    api = MWS(region='CA', *mwscred)
    assert api.domain == 'https://mws.amazonservices.ca'
    api = MWS(region='DE', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='EG', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='ES', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='FR', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='GB', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='IN', *mwscred)
    assert api.domain == 'https://mws.amazonservices.in'
    api = MWS(region='IT', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='JP', *mwscred)
    assert api.domain == 'https://mws.amazonservices.jp'
    api = MWS(region='MX', *mwscred)
    assert api.domain == 'https://mws.amazonservices.com.mx'
    api = MWS(region='NL', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='SA', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='SG', *mwscred)
    assert api.domain == 'https://mws-fe.amazonservices.com'
    api = MWS(region='TR', *mwscred)
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='UK', *mwscred)  # alias for GB
    assert api.domain == 'https://mws-eu.amazonservices.com'
    api = MWS(region='US', *mwscred)
    assert api.domain == 'https://mws.amazonservices.com'
    uk_api = MWS(region='UK', *mwscred)
    gb_api = MWS(region='GB', *mwscred)
    assert uk_api.domain == gb_api.domain


def test_marketplaces_enum():
    """
    The way to access the values.
    """
    assert Marketplaces.CA.endpoint == 'https://mws.amazonservices.ca'
    assert Marketplaces.CA.marketplace_id == 'A2EUQ1WTGCTBG2'
