import datetime

import pytest

from ..conftest import TEST_MWS_ACCESS_KEY, TEST_MWS_ACCOUNT_ID, TEST_MWS_AUTH_TOKEN

from mws.mws import MWS
from mws.utils.params import clean_string


class APITestCase:
    """Common test cases and tools for all MWS API sections."""

    api_class = MWS

    def assert_common_params(self, params, action=None):
        """Tests the common params expected in every call."""
        if action:
            assert params["Action"] == clean_string(action)

        assert params["AWSAccessKeyId"] == TEST_MWS_ACCESS_KEY
        assert params[self.api_class.ACCOUNT_TYPE] == TEST_MWS_ACCOUNT_ID
        if "MWSAuthToken" in params:
            assert params["MWSAuthToken"] == TEST_MWS_AUTH_TOKEN

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

    def test_service_status(self, api_instance):
        """Test the `GetServiceStatus` common request."""
        params = api_instance.get_service_status()
        # Only key we care about here is GetServiceStatus
        assert params["Action"] == "GetServiceStatus"

    def test_generic_request_uri_correct_value(self, api_instance):
        """If the API's `.uri` attr is an incorrect value, should raise `ValueError`.

        This test includes (crude) setup and teardown logic to change `api_instance.uri`,
        which may be needed for other tests.

        The real work of this test happens in `_generic_request_uri_correct_value`.
        """
        # URI exception test will change the api's URI.
        api_orig_uri = api_instance.uri
        try:
            # This is a crude way of ensuring teardown logic.
            # TODO: fix up with a pytest fixture?
            self._generic_request_uri_correct_value(api_instance)
        except Exception:
            raise
        finally:
            # Reset the URI so that other tests are unaffected.
            api_instance.uri = api_orig_uri

    def _generic_request_uri_correct_value(self, api_instance):
        """If the API's `.uri` attr is an incorrect value, should raise `ValueError`."""
        action = "GenericRequestURIException"
        params = {"DoesNotMatter": "foobar"}

        # First assert that the API's real URI (unchanged up to here) works.
        # This will indicate that the API class's `URI` class attribute is not set.
        assert api_instance.generic_request(action=action, params=params)

        # Next we check what should be a known value.
        api_instance.uri = "/Something/that/should/work"
        assert api_instance.generic_request(action=action, params=params)

        # Finally we check that values known to fail will raise `ValueError` correctly.
        uri_values = [None, False, "", "/"]
        for val in uri_values:
            api_instance.uri = val
            with pytest.raises(ValueError):
                assert api_instance.generic_request(action=action, params=params)

    def test_generic_request_correct_params_type(self, api_instance):
        """Generic requests with a non-dict value for `params`
        should raise `ValueError`.
        """
        action = "GenericRequestBadParamsException"

        # Any dict should pass (including an empty one)
        assert api_instance.generic_request(action=action, params={})

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
                assert api_instance.generic_request(action, params=val)

    def test_basic_generic_request(self, api_instance):
        """Test an arbitrary generic request with a series of simple data elements."""
        action = "BasicGenericRequest"

        # Send a basic payload.
        params = {
            "ADateTime": datetime.datetime(2020, 10, 12),
            "ATrueBool": True,
            "AFalseBool": False,
            "NoneShouldNotExist": None,
        }

        request_params = api_instance.generic_request(action=action, params=params)
        self.assert_common_params(request_params, action="BasicGenericRequest")
        assert request_params["ADateTime"] == "2020-10-12T00%3A00%3A00"
        assert request_params["ATrueBool"] == "true"
        assert request_params["AFalseBool"] == "false"
        assert "NoneShouldNotExist" not in request_params

    def test_complex_generic_request(self, api_instance):
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

        request_params = api_instance.generic_request(action=action, params=params)

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
