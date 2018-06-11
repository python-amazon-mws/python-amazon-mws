"""
Tests for the mws.MWS class and MARKETPLACES.
"""
import pytest
from mws.mws import MWSError, MWS, MARKETPLACES

mwscred = ['a', 'b', 'c']


def test_notvalid_region():
    with pytest.raises(MWSError):
        MWS(region='ERROR', *mwscred)


def test_regionparameter():
    api = MWS(region='CA', *mwscred)
    assert api.domain == 'https://mws.amazonservices.ca'


def test_marketplaces_enum():
    """
    The way to access the values.
    """
    assert MARKETPLACES.CA.Endpoint == 'https://mws.amazonservices.ca'
    assert MARKETPLACES.CA.MarketplaceId == 'A2EUQ1WTGCTBG2'
