import pytest


@pytest.fixture
def cred_access_key():
    return "cred_access_key"


@pytest.fixture
def cred_secret_key():
    return "cred_secret_key"


@pytest.fixture
def cred_account_id():
    return "cred_account_id"


@pytest.fixture
def cred_auth_token():
    return "cred_auth_token"


@pytest.fixture
def mws_credentials(cred_access_key, cred_secret_key, cred_account_id, cred_auth_token):
    """Fake set of MWS credentials"""
    return {
        "access_key": cred_access_key,
        "secret_key": cred_secret_key,
        "account_id": cred_account_id,
        "auth_token": cred_auth_token,
    }
