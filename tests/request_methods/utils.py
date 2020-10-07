"""
Utilities common to request method tests.
"""
import datetime
import mws

from urllib.parse import quote

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
        """Tests the common params expected in every call."""
        if action:
            assert params["Action"] == clean_string(action)

        assert params["AWSAccessKeyId"] == self.CREDENTIAL_ACCESS
        assert params[self.api.ACCOUNT_TYPE] == self.CREDENTIAL_ACCOUNT
        assert params["MWSAuthToken"] == self.CREDENTIAL_TOKEN

        # Signature keys (below) are defined with string literals in MWS.get_params
        # If test fails here, check that method.
        assert params["SignatureMethod"] == "HmacSHA256"
        assert params["SignatureVersion"] == "2"
        isoformat_str = "%Y-%m-%dT%H%%3A%M%%3A%S"
        try:
            datetime.datetime.strptime(params["Timestamp"], isoformat_str)
        except ValueError:
            pytest.fail(
                "Timestamp expected an ISO-8601 datetime string url encoded"
                " with format [YYYY-MM-DDTHH%3AMM%3ASS]."
            )

    def test_service_status(self):
        """Test the `GetServiceStatus` common request."""
        response = self.api.get_service_status()
        # Only key we care about here is GetServiceStatus
        assert response["Action"] == "GetServiceStatus"

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
        """If the API's `.uri` attr is an incorrect value, should raise `ValueError`."""
        action = "GenericRequestURIException"
        params = {"DoesNotMatter": "foobar"}

        # First assert that the API's real URI (unchanged up to here) works.
        # This will indicate that the API class's `URI` class attribute is not set.
        assert self.api.generic_request(action=action, params=params)

        # Next we check what should be a known value.
        self.api.uri = "/Something/that/should/work"
        assert self.api.generic_request(action=action, params=params)

        # Finally we check that values known to fail will raise `ValueError` correctly.
        uri_values = [None, False, "", "/"]
        for val in uri_values:
            self.api.uri = val
            with pytest.raises(ValueError):
                assert self.api.generic_request(action=action, params=params)

    def test_generic_request_correct_params_type(self):
        """Generic requests with a non-dict value for `params`
        should raise `ValueError`.
        """
        action = "GenericRequestBadParamsException"

        # Any dict should pass (including an empty one)
        assert self.api.generic_request(action=action, params={})

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
                assert self.api.generic_request(action, params=val)

    def test_basic_generic_request(self):
        """Test an arbitrary generic request with a series of simple data elements."""
        action = "BasicGenericRequest"
        test_datetime = datetime.datetime.utcnow()

        # Send a basic payload.
        params = {
            "ADateTime": test_datetime,
            "ATrueBool": True,
            "AFalseBool": False,
            "NoneShouldNotExist": None,
        }

        request_params = self.api.generic_request(action=action, params=params)
        self.assert_common_params(request_params, action="BasicGenericRequest")
        assert request_params["ADateTime"] == clean_date(test_datetime)
        assert request_params["ATrueBool"] == clean_bool(True)
        assert request_params["AFalseBool"] == clean_bool(False)
        assert "NoneShouldNotExist" not in request_params

    def test_complex_generic_request(self):
        """Test generic request with nested data structures in its params."""
        action = "ComplexGenericRequest"
        params = {
            "Enumerated": ["A", "B", "C"],
            "Keyed": {"Foo": "bar", "Bar": 4, "Baz": False},
            "Multi": {
                "A": [
                    {"Foo": "baz", "Bar": 12},
                    {"Foo": "what", "Bar": "ever", "Something": [4, 6, 7, 9]},
                ],
                "B": [1, 2, 3],
            },
        }

        request_params = self.api.generic_request(action=action, params=params)

        self.assert_common_params(request_params, action=action)

        expected = {
            "Enumerated.1": "A",
            "Enumerated.2": "B",
            "Enumerated.3": "C",
            "Keyed.Foo": "bar",
            "Keyed.Bar": "4",
            "Keyed.Baz": "false",
            "Multi.A.1.Foo": "baz",
            "Multi.A.1.Bar": "12",
            "Multi.A.1.Bar": "12",
            "Multi.A.2.Foo": "what",
            "Multi.A.2.Bar": "ever",
            "Multi.A.2.Something.1": "4",
            "Multi.A.2.Something.2": "6",
            "Multi.A.2.Something.3": "7",
            "Multi.A.2.Something.4": "9",
            "Multi.B.1": "1",
            "Multi.B.2": "2",
            "Multi.B.3": "3",
        }
        for key, val in expected.items():
            assert request_params[key] == val


def clean_string(s):
    return quote(s, safe="-_.~")


def clean_bool(b):
    return str(b).lower()


def clean_date(date):
    return quote(date.isoformat(), safe="-_.~")


def get_api_instance(api_class):
    """Return an testing instance of `api_class`.

    Uses `CommonAPIRequestTools`, performs `setUp` using `api_class`,
    then returns an instance of that class, ready to send requests.
    """
    tools = CommonAPIRequestTools()
    tools.api_class = api_class
    tools.setUp()
    return tools.api
