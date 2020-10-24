"""Tests for the mws.MWS class and Marketplaces."""

import datetime

import pytest

from mws import MWS, MWSError, Marketplaces


def test_invalid_region(mws_credentials):
    with pytest.raises(MWSError):
        MWS(region="DOESN'T EXIST", **mws_credentials)


@pytest.mark.parametrize("region, alias", (("UK", "GB"),))  # GB aliases UK
def test_region_aliases(region, alias, mws_credentials):
    region_api = MWS(region=region, **mws_credentials)
    alias_api = MWS(region=alias, **mws_credentials)
    assert region_api.domain == alias_api.domain


@pytest.mark.parametrize(
    "region, endpoint, marketplace_id",
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
        ("SE", "https://mws-eu.amazonservices.com", "A2NODRKZP88ZB9"),
        ("SG", "https://mws-fe.amazonservices.com", "A19VAU5U5O7RUS"),
        ("TR", "https://mws-eu.amazonservices.com", "A33AVAJ2PDY3EV"),
        ("UK", "https://mws-eu.amazonservices.com", "A1F83G8C2ARO7P"),
        ("US", "https://mws.amazonservices.com", "ATVPDKIKX0DER"),
    ),
)
def test_marketplaces_enum(region, endpoint, marketplace_id):
    """Test that attrs of marketplace enumerations work as expected."""
    market = getattr(Marketplaces, region)
    assert market.endpoint == endpoint
    assert market.marketplace_id == marketplace_id


@pytest.mark.parametrize(
    "region, domain",
    (
        ("AE", "https://mws.amazonservices.ae"),
        ("AU", "https://mws.amazonservices.com.au"),
        ("BR", "https://mws.amazonservices.com"),
        ("CA", "https://mws.amazonservices.ca"),
        ("DE", "https://mws-eu.amazonservices.com"),
        ("EG", "https://mws-eu.amazonservices.com"),
        ("ES", "https://mws-eu.amazonservices.com"),
        ("FR", "https://mws-eu.amazonservices.com"),
        ("GB", "https://mws-eu.amazonservices.com"),
        ("IN", "https://mws.amazonservices.in"),
        ("IT", "https://mws-eu.amazonservices.com"),
        ("JP", "https://mws.amazonservices.jp"),
        ("MX", "https://mws.amazonservices.com.mx"),
        ("NL", "https://mws-eu.amazonservices.com"),
        ("SA", "https://mws-eu.amazonservices.com"),
        ("SE", "https://mws-eu.amazonservices.com"),
        ("SG", "https://mws-fe.amazonservices.com"),
        ("TR", "https://mws-eu.amazonservices.com"),
        ("UK", "https://mws-eu.amazonservices.com"),
        ("US", "https://mws.amazonservices.com"),
    ),
)
def test_region_domains(region, domain, mws_credentials):
    assert MWS(region=region, **mws_credentials).domain == domain


def test_no_authtoken_included_default_params(mws_credentials):
    credentials = {k: v for k, v in mws_credentials.items() if k != "auth_token"}
    mws = MWS(**credentials)
    mws._test_request_params = True
    timestamp = datetime.datetime(2020, 8, 24, 16, 30)
    default_params = mws.get_default_params(action="Something", timestamp=timestamp)
    assert "MWSAuthToken" not in default_params

    # While we're here, check the other params
    assert default_params == {
        "Action": "Something",
        "AWSAccessKeyId": credentials["access_key"],
        "SellerId": credentials["account_id"],
        "SignatureVersion": "2",
        "Timestamp": timestamp,
        "Version": MWS.VERSION,
        "SignatureMethod": "HmacSHA256",
    }


def test_mws_with_proxies(mws_credentials):
    mws = MWS(**mws_credentials, proxy="example.com")
    proxies = mws.get_proxies()
    assert proxies["http"] == "http://example.com"
    assert proxies["https"] == "https://example.com"


def test_mws_without_proxies(mws_credentials):
    mws = MWS(**mws_credentials)
    proxies = mws.get_proxies()
    assert proxies["http"] is None
    assert proxies["https"] is None


def test_mws_action_not_in_nexttokenops_raises_exception(mws_credentials):
    mws = MWS(**mws_credentials)
    action = "DefinitelyNotIntheNextTokenOperations"
    token = "token"
    with pytest.raises(MWSError):
        mws.action_by_next_token(action, token)


### DEPRECATED - CHANGE IN 1.0 ###
def test_mws_get_service_status(mws_credentials):
    """Send a real ``get_service_status`` call to MWS.
    No real credentials are required for this type of call, in fact.
    """
    # TODO Tests the pathway that uses `MWSResponse`. Change test in 1.0 to default
    mws = MWS(**mws_credentials)
    mws._use_feature_mwsresponse = True
    resp = mws.get_service_status()
    assert resp.parsed.Status in ("GREEN", "GREEN_I", "YELLOW", "RED")
    utc_now_date_str = datetime.datetime.utcnow().date().isoformat()
    assert resp.parsed.Timestamp[:10] == utc_now_date_str


### DEPRECATED - REMOVE IN 1.0 ###
def test_mws_get_service_status_deprecated(mws_credentials):
    """Send a real ``get_service_status`` call to MWS.
    No real credentials are required for this type of call, in fact.
    """
    # TODO Tests the pathway that uses `DictWrapper`. Remove test in 1.0
    mws = MWS(**mws_credentials)
    resp = mws.get_service_status()
    assert resp.parsed.Status in ("GREEN", "GREEN_I", "YELLOW", "RED")
    utc_now_date_str = datetime.datetime.utcnow().date().isoformat()
    assert resp.parsed.Timestamp[:10] == utc_now_date_str
