import pytest


@pytest.fixture
def access_key():
    return "AAAAAAAAAAAAAAAAAAAA"


@pytest.fixture
def secret_key():
    return "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"


@pytest.fixture
def account_id():
    return "AAAAAAAAAAAAAA"


@pytest.fixture
def timestamp():
    return "2017-08-12T19:40:35Z"


@pytest.fixture
def credentials(access_key, secret_key, account_id):
    """Fake set of MWS credentials"""
    return {
        "access_key": access_key,
        "secret_key": secret_key,
        "account_id": account_id,
    }
