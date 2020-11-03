"""Tests related to kwarg renaming from 0.8 to 1.0dev versions"""

from typing import Callable, List, Optional, Union
import pytest

from mws import apis, MWS
from mws.utils.deprecation import RemovedInPAM11Warning


class MethodRenamedBase:
    """Base class for test cases in this module, defining some shared tooling."""

    @staticmethod
    def run_method(
        method: Callable,
        old: Union[dict, str],
        new: Union[dict, str],
        required: Optional[Union[List[str], str, dict]] = None,
    ):
        """Runs an API method to test for old and new kwarg warnings.
        Defines the testing pattern for renamed kwargs.

        ``method`` is the callable request method to use for this test.

        ``old`` represents the original name for the argument being passed,
        which should raise a warning when used. ``new`` is the same, but uses the
        newer name of that argument, and should raise no warning.

        Both ``old`` and ``new`` may be either a str of the argument name itself,
        or a dict containing that argument and a dummy value, in the case a particular
        value is required for the call to pass.

        ``required``, if provided, can be either a single string argument name;
        a list of strings with argument names; or a dict or argument names and dummy
        values. (If a string or list, dummy string values are supplied)
        """
        if required is None:
            # Set to default empty dict
            required = {}
        if isinstance(required, str):
            # Wrap in a list so the next part is more DRY
            required = [required]
        if isinstance(required, list):
            required = {key: "value" for key in required}

        # Exception: The "new" kwarg may actually be one of the requirements
        # (a renamed positional argument).
        # In that case, we remove it from the `required` dict, so that we can properly
        # test the renaming.
        if new in required:
            del required[new]

        # Check that the old kwarg raises the appropriate warning
        with pytest.warns(RemovedInPAM11Warning):
            if isinstance(old, dict):
                old_kwargs = old
            else:
                old_kwargs = {old: "dummy"}
            old_params = method(**required, **old_kwargs)

        # The new kwarg should raise no warning:
        # record the warnings raised and assert the record is empty.
        with pytest.warns(None) as record:
            if isinstance(new, dict):
                new_kwargs = new
            else:
                new_kwargs = {new: "dummy"}
            new_params = method(**required, **new_kwargs)
        assert len(record) == 0

        # Check that request params in both the old and new names are identical
        # NOTE: The Timestamp and Signature keys may be different, due to race condition
        # between two different requests. We remove those,
        # as they're not necessary for our testing here.
        common_params = [
            "AWSAccessKeyId",
            "MWSAuthToken",
            "Signature",
            "SignatureMethod",
            "SignatureVersion",
            "Timestamp",
        ]
        for key in common_params:
            if key in old_params:
                del old_params[key]
            if key in new_params:
                del new_params[key]
        assert old_params == new_params


class TestFeedsMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in Feeds API."""

    api_class = apis.Feeds

    @pytest.mark.parametrize("old, new", [("marketplaceids", "marketplace_ids")])
    def test_submit_feed_kwargs_renamed(self, api_instance, old, new):
        required = {"feed": b"a", "feed_type": "b"}
        method = api_instance.submit_feed
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("feedids", "feed_ids"),
            ("feedtypes", "feed_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_feed_submission_list_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_feed_submission_list
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("feedtypes", "feed_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_feed_submission_count_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_feed_submission_count
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("feedids", "feed_ids"),
            ("feedtypes", "feed_types"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_cancel_feed_submissions_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.cancel_feed_submissions
        self.run_method(method, old, new)

    @pytest.mark.parametrize("old, new", [("feedid", "feed_id")])
    def test_get_feed_submission_result_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_feed_submission_result
        self.run_method(method, old, new)


class TestInboundShipmentsMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in InboundShipments API."""

    api_class = apis.InboundShipments

    @pytest.mark.parametrize("old, new", [("num_packages", "num_labels")])
    def test_get_package_labels_kwargs_renamed(self, api_instance, old, new):
        required = ["shipment_id"]
        method = api_instance.get_package_labels
        self.run_method(method, old, new, required=required)


class TestOrdersMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in Orders API."""

    api_class = apis.Orders

    @pytest.mark.parametrize(
        "old, new",
        [
            ("marketplaceids", "marketplace_ids"),
            ("lastupdatedafter", "last_updated_after"),
            ("lastupdatedbefore", "last_updated_before"),
            ("orderstatus", "order_statuses"),
            ("seller_orderid", "seller_order_id"),
        ],
    )
    def test_list_orders_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.list_orders
        self.run_method(method, old, new)


class TestProductsMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in Products API."""

    api_class = apis.Products

    @pytest.mark.parametrize(
        "old, new", [("marketplaceid", "marketplace_id"), ("contextid", "context_id")]
    )
    def test_list_matching_products_kwargs_renamed(self, api_instance, old, new):
        required = ["marketplace_id", "query"]
        method = api_instance.list_matching_products
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_matching_product_kwargs_renamed(self, api_instance, old, new):
        required = ["asins"]
        method = api_instance.get_matching_product
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_matching_product_for_id_kwargs_renamed(self, api_instance, old, new):
        required = ["type_", "ids"]
        method = api_instance.get_matching_product_for_id
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_competitive_pricing_for_sku_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["skus"]
        method = api_instance.get_competitive_pricing_for_sku
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_competitive_pricing_for_asin_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["asins"]
        method = api_instance.get_competitive_pricing_for_asin
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new", [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def test_get_lowest_offer_listings_for_sku_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["marketplace_id", "skus"]
        method = api_instance.get_lowest_offer_listings_for_sku
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new", [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def test_get_lowest_offer_listings_for_asin_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["marketplace_id", "asins"]
        method = api_instance.get_lowest_offer_listings_for_asin
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new", [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def test_get_lowest_priced_offers_for_sku_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["marketplace_id", "sku"]
        method = api_instance.get_lowest_priced_offers_for_sku
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new", [("marketplaceid", "marketplace_id"), ("excludeme", "exclude_me")]
    )
    def test_get_lowest_priced_offers_for_asin_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["marketplace_id", "asin"]
        method = api_instance.get_lowest_priced_offers_for_asin
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_my_price_for_sku_kwargs_renamed(self, api_instance, old, new):
        required = ["skus"]
        method = api_instance.get_my_price_for_sku
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_my_price_for_asin_kwargs_renamed(self, api_instance, old, new):
        required = ["asins"]
        method = api_instance.get_my_price_for_asin
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_product_categories_for_sku_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["sku"]
        method = api_instance.get_product_categories_for_sku
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_product_categories_for_asin_kwargs_renamed(
        self, api_instance, old, new
    ):
        required = ["asin"]
        method = api_instance.get_product_categories_for_asin
        self.run_method(method, old, new, required=required)


class TestRecommendationsMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in Recommendations API."""

    api_class = apis.Recommendations

    @pytest.mark.parametrize("old, new", [("marketplaceid", "marketplace_id")])
    def test_get_last_updated_time_for_recommendations_kwargs_renamed(
        self, api_instance, old, new
    ):
        method = api_instance.get_last_updated_time_for_recommendations
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("marketplaceid", "marketplace_id"),
            ("recommendationcategory", "recommendation_category"),
        ],
    )
    def test_list_recommendations_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.list_recommendations
        self.run_method(method, old, new)


class TestReportsMethodKwargRenames(MethodRenamedBase):
    """Cases related to changed kwargs in Reports API."""

    api_class = apis.Reports

    @pytest.mark.parametrize("old, new", [("marketplaceids", "marketplace_ids")])
    def test_request_report_kwargs_renamed(self, api_instance, old, new):
        required = ["report_type"]
        method = api_instance.request_report
        self.run_method(method, old, new, required=required)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("requestids", "request_ids"),
            ("types", "report_types"),
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_report_request_list_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_request_list
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("processingstatuses", "processing_statuses"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_report_request_count_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_request_count
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("requestids", "request_ids"),
            ("types", "report_types"),
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_report_list_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_list
        self.run_method(method, old, new)

    @pytest.mark.parametrize(
        "old, new",
        [
            ("fromdate", "from_date"),
            ("todate", "to_date"),
        ],
    )
    def test_get_report_count_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_count
        self.run_method(method, old, new)

    @pytest.mark.parametrize("old, new", [("types", "report_types")])
    def test_get_report_schedule_list_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_schedule_list
        self.run_method(method, old, new)

    @pytest.mark.parametrize("old, new", [("types", "report_types")])
    def test_get_report_schedule_count_kwargs_renamed(self, api_instance, old, new):
        method = api_instance.get_report_schedule_count
        self.run_method(method, old, new)
