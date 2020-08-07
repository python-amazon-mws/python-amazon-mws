"""Tests for the mws.MWS class and Marketplaces."""

import pytest
from mws import MWS, MWSError, Marketplaces

FAKE_CREDS = ["a", "b", "c"]


def test_invalid_region():
    with pytest.raises(MWSError):
        MWS(region="ERROR", *FAKE_CREDS)


def test_region_domains():
    assert MWS(region="AE", *FAKE_CREDS).domain == "https://mws.amazonservices.ae"
    assert MWS(region="AU", *FAKE_CREDS).domain == "https://mws.amazonservices.com.au"
    assert MWS(region="BR", *FAKE_CREDS).domain == "https://mws.amazonservices.com"
    assert MWS(region="CA", *FAKE_CREDS).domain == "https://mws.amazonservices.ca"
    assert MWS(region="DE", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="EG", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="ES", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="FR", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="GB", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="GB", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="IN", *FAKE_CREDS).domain == "https://mws.amazonservices.in"
    assert MWS(region="IT", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="JP", *FAKE_CREDS).domain == "https://mws.amazonservices.jp"
    assert MWS(region="MX", *FAKE_CREDS).domain == "https://mws.amazonservices.com.mx"
    assert MWS(region="NL", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="SA", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="SG", *FAKE_CREDS).domain == "https://mws-fe.amazonservices.com"
    assert MWS(region="TR", *FAKE_CREDS).domain == "https://mws-eu.amazonservices.com"
    assert MWS(region="US", *FAKE_CREDS).domain == "https://mws.amazonservices.com"


def test_region_aliases():
    # GB alias
    uk_api = MWS(region="UK", *FAKE_CREDS)
    gb_api = MWS(region="GB", *FAKE_CREDS)
    assert uk_api.domain == gb_api.domain


def test_marketplaces_enum():
    """Test that attrs of marketplace enumerations work as expected."""
    assert Marketplaces.CA.endpoint == "https://mws.amazonservices.ca"
    assert Marketplaces.CA.marketplace_id == "A2EUQ1WTGCTBG2"
