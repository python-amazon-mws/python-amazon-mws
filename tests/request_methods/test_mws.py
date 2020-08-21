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


@pytest.mark.parametrize(
    "market_shortname, endpoint, marketplace_id",
    (
        ("AE", "https://mws.amazonservices.ae", "A2VIGQ35RCS4UG"),
        ("AU", "https://mws.amazonservices.com.au", "A39IBJ37TRP1C6"),
        ("BR", "https://mws.amazonservices.com", "A2Q3Y263D00KWC"),
        ("CA", "https://mws.amazonservices.ca", "A2EUQ1WTGCTBG2"),
        ("DE", "https://mws-eu.amazonservices.com", "A1PA6795UKMFR9"),
        ("EG", "https://mws-eu.amazonservices.com", "ARBP9OOSHTCHU"),
        ("ES", "https://mws-eu.amazonservices.com", "A1RKKUPIHCS9HS"),
        ("FR", "https://mws-eu.amazonservices.com", "A13V1IB3VIYZZH"),
        ("GB", "https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P"),
        ("IN", "https://mws.amazonservices.in", "A21TJRUUN4KGV"),
        ("IT", "https://mws-eu.amazonservices.com", "APJ6JRA9NG5V4"),
        ("JP", "https://mws.amazonservices.jp", "A1VC38T7YXB528"),
        ("MX", "https://mws.amazonservices.com.mx", "A1AM78C64UM0Y8"),
        ("NL", "https://mws-eu.amazonservices.com", "A1805IZSGTT6HS"),
        ("SA", "https://mws-eu.amazonservices.com", "A17E79C6D8DWNP"),
        ("SE", "https://mws-fe.amazonservices.com", "A2NODRKZP88ZB9"),
        ("SG", "https://mws-fe.amazonservices.com", "A19VAU5U5O7RUS"),
        ("TR", "https://mws-eu.amazonservices.com", "A33AVAJ2PDY3EV"),
        ("UK", "https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P"),
        ("US", "https://mws.amazonservices.com", "ATVPDKIKX0DER"),
    ),
)
def test_marketplaces_enum(market_shortname, endpoint, marketplace_id):
    """Test that attrs of marketplace enumerations work as expected."""
    market = getattr(Marketplaces, market_shortname)
    assert market.endpoint == endpoint
    assert market.marketplace_id == marketplace_id
