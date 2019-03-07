"""
Utilities common to request method tests.
"""
import datetime

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote


class CommonRequestTestTools(object):
    CREDENTIAL_ACCESS = 'cred_access'
    CREDENTIAL_SECRET = 'cred_secret'
    CREDENTIAL_ACCOUNT = 'cred_account'
    CREDENTIAL_TOKEN = 'cred_token'

    def assert_common_params(self, params):
        """
        Tests the common parameters expected in every call.
        """
        self.assertEqual(params['AWSAccessKeyId'], self.CREDENTIAL_ACCESS)
        self.assertEqual(params[self.api.ACCOUNT_TYPE], self.CREDENTIAL_ACCOUNT)
        self.assertEqual(params['MWSAuthToken'], self.CREDENTIAL_TOKEN)

        # Signature keys (below) are defined with string literals in MWS.get_params
        # If test fails here, check that method.
        self.assertEqual(params['SignatureMethod'], 'HmacSHA256')
        self.assertEqual(params['SignatureVersion'], '2')
        isoformat_str = "%Y-%m-%dT%H%%3A%M%%3A%S"
        try:
            datetime.datetime.strptime(params['Timestamp'], isoformat_str)
        except ValueError:
            self.fail(
                "Timestamp expected an ISO-8601 datetime string url encoded"
                " with format [YYYY-MM-DDTHH%3AMM%3ASS].")

    def test_service_status(self):
        response = self.api.get_service_status()
        # Only key we care about here is GetServiceStatus
        self.assertEqual(response['Action'], 'GetServiceStatus')


def transform_string(s):
    return quote(s, safe='-_.~')


def transform_bool(b):
    return str(b).lower()


def transform_date(date):
    return quote(date.isoformat(), safe='-_.~')
