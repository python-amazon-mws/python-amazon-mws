import pytest


@pytest.fixture
def credentials():
    """Fake set of MWS credentials"""
    return {
        "access_key": "AAAAAAAAAAAAAAAAAAAA",
        "secret_key": "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
        "account_id": "AAAAAAAAAAAAAA",
    }
