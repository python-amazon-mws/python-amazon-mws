"""
Utilities common to request method tests.
"""
import datetime


class CommonRequestTestTools(object):
    CREDENTIAL_ACCESS = 'cred_access'
    CREDENTIAL_SECRET = 'cred_secret'
    CREDENTIAL_ACCOUNT = 'cred_account'
    CREDENTIAL_TOKEN = 'cred_token'

    def assert_common_params(self, params):
        """
        Tests the common parameters expected in every call.
        """
        assert params['AWSAccessKeyId'] == self.CREDENTIAL_ACCESS
        assert params[self.api.ACCOUNT_TYPE] == self.CREDENTIAL_ACCOUNT
        assert params['MWSAuthToken'] == self.CREDENTIAL_TOKEN

        # Signature keys (below) are defined with string literals in MWS.get_params
        # If test fails here, check that method.
        assert params['SignatureMethod'] == 'HmacSHA256'
        assert params['SignatureVersion'] == '2'
        isoformat_str = "%Y-%m-%dT%H:%M:%S"
        try:
            datetime.datetime.strptime(params['Timestamp'], isoformat_str)
        except ValueError:
            self.fail("Timestamp expected an ISO-8601 datetime string with format [YYYY-MM-DDTHH:MM:SS].")

    def test_service_status(self):
        response = self.api.get_service_status()
        # Only key we care about here is GetServiceStatus
        assert response['Action'] == 'GetServiceStatus'
