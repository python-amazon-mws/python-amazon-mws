"""
Utilities common to request method tests.
"""
import datetime
import mws

try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

import pytest


class CommonAPIRequestTools(object):
    """A set of common tools to use with MWS API request method tests.

    Should be subclassed by a test case class for an API as:

        class APITestCase(CommonAPIRequestTools, unittest.TestCase):
            test_class = mws.APIClass

    `test_class` must point the API class intended for the TestCase.
    The class will be instantiated on the TestCase as `self.api`
    with fake credentials and the flag `_test_request_params` set to True
    (see `setUp` method for details).
    """

    CREDENTIAL_ACCESS = "cred_access"
    CREDENTIAL_SECRET = "cred_secret"
    CREDENTIAL_ACCOUNT = "cred_account"
    CREDENTIAL_TOKEN = "cred_token"

    api_class = mws.mws.MWS
    """Define within a subclassing API TestCase with the class to be tested."""

    def setUp(self):
        """Set up the API class with fake credentials,
        and set `_test_request_params` to prevent sending a live request.
        """
        self.api = self.api_class(
            self.CREDENTIAL_ACCESS,
            self.CREDENTIAL_SECRET,
            self.CREDENTIAL_ACCOUNT,
            auth_token=self.CREDENTIAL_TOKEN,
        )
        self.api._test_request_params = True

    def assert_common_params(self, params, action=None):
        """Tests the common parameters expected in every call."""
        if action:
            self.assertEqual(params["Action"], transform_string(action))

        self.assertEqual(params["AWSAccessKeyId"], self.CREDENTIAL_ACCESS)
        self.assertEqual(params[self.api.ACCOUNT_TYPE], self.CREDENTIAL_ACCOUNT)
        self.assertEqual(params["MWSAuthToken"], self.CREDENTIAL_TOKEN)

        # Signature keys (below) are defined with string literals in MWS.get_params
        # If test fails here, check that method.
        self.assertEqual(params["SignatureMethod"], "HmacSHA256")
        self.assertEqual(params["SignatureVersion"], "2")
        isoformat_str = "%Y-%m-%dT%H%%3A%M%%3A%S"
        try:
            datetime.datetime.strptime(params["Timestamp"], isoformat_str)
        except ValueError:
            self.fail(
                "Timestamp expected an ISO-8601 datetime string url encoded"
                " with format [YYYY-MM-DDTHH%3AMM%3ASS]."
            )

    def test_service_status(self):
        """Test the `GetServiceStatus` common request."""
        response = self.api.get_service_status()
        # Only key we care about here is GetServiceStatus
        self.assertEqual(response["Action"], "GetServiceStatus")

    def test_generic_request_uri_correct_value(self):
        """If the API's `.uri` attr is an incorrect value, should raise `ValueError`.

        This test includes (crude) setup and teardown logic to change `self.api.uri`,
        which may be needed for other tests.

        The real work of this test happens in `_generic_request_uri_correct_value`.
        """
        # URI exception test will change the api's URI.
        api_orig_uri = self.api.uri
        try:
            # This is a crude way of ensuring teardown logic.
            # TODO: fix up with a pytest fixture?
            self._generic_request_uri_correct_value()
        except Exception:
            raise
        finally:
            # Reset the URI so that other tests are unaffected.
            self.api.uri = api_orig_uri

    def _generic_request_uri_correct_value(self):
        """If the API's `.uri` attr is an incorrect value, should raise `ValueError`.
        """
        action = "GenericRequestURIException"
        parameters = {"DoesNotMatter": "foobar"}

        # First assert that the API's real URI (unchanged up to here) works.
        # This will indicate that the API class's `URI` class attribute is not set.
        assert self.api.generic_request(action=action, parameters=parameters)

        # Next we check what should be a known value.
        self.api.uri = "/Something/that/should/work"
        assert self.api.generic_request(action=action, parameters=parameters)

        # Finally we check that values known to fail will raise `ValueError` correctly.
        uri_values = [None, False, "", "/"]
        for val in uri_values:
            self.api.uri = val
            with pytest.raises(ValueError):
                assert self.api.generic_request(action=action, parameters=parameters)

    def test_basic_generic_request(self):
        """Test an arbitrary generic request within a given API class."""
        action = "BasicGenericRequest"
        test_datetime = datetime.datetime.utcnow()

        # Send a basic payload.
        parameters = {
            "ADateTime": test_datetime,
            "ATrueBool": True,
            "AFalseBool": False,
            "NoneShouldNotExist": None,
        }

        request_params = self.api.generic_request(action=action, parameters=parameters)
        self.assert_common_params(request_params, action="BasicGenericRequest")
        self.assertEqual(request_params["ADateTime"], transform_date(test_datetime))
        self.assertEqual(request_params["ATrueBool"], transform_bool(True))
        self.assertEqual(request_params["AFalseBool"], transform_bool(False))

    def test_generic_request_correct_parameters_type(self):
        """Generic requests with a non-dict value for `parameters`
        should raise `ValueError`.
        """
        action = "GenericRequestBadParameterssException"

        # Any dict should pass (including an empty one)
        assert self.api.generic_request(action=action, parameters={})

        # Non-dict values should NOT pass
        param_values = [
            ["Lists", "don't", "work"],
            ("Tuples", "don't", "ether"),
            3,  # Integer? No thank you.
            "No to a string!",
            {"You", "made", "a", "set,", "silly!"},
        ]
        for val in param_values:
            with pytest.raises(ValueError):
                assert self.api.generic_request(action, parameters=val)

    # TODO test complex request paramter with nested lists and dicts.


def transform_string(s):
    return quote(s, safe="-_.~")


def transform_bool(b):
    return str(b).lower()


def transform_date(date):
    return quote(date.isoformat(), safe="-_.~")
