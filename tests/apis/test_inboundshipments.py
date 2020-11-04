"""Tests for the InboundShipments API class."""
import datetime

import pytest

from mws import InboundShipments
from mws import MWSError
from mws.apis.inbound_shipments import parse_legacy_item, parse_shipment_items
from mws.utils.xml import mws_xml_to_dotdict
from mws.models.inbound_shipments import (
    Address,
    ExtraItemData,
    InboundShipmentItem,
    InboundShipmentPlanRequestItem,
    shipment_items_from_plan,
)

from .common import APITestCase


class InboundShipmentsAPITestCase(APITestCase):
    api_class = InboundShipments


@pytest.fixture
def inbound_from_address():
    """A dummy address known to pass testing."""
    return Address(
        name="Roland Deschain",
        address_line_1="500 Summat Cully Lane",
        city="Gilead",
        country_code="US",
    )


@pytest.fixture
def from_address_params_expected():
    """The expected output when using inbound_from_address fixture."""
    return {
        "Name": "Roland Deschain",
        "AddressLine1": "500 Summat Cully Lane",
        "AddressLine2": None,
        "City": "Gilead",
        "DistrictOrCounty": None,
        "StateOrProvinceCode": None,
        "PostalCode": None,
        "CountryCode": "US",
    }


@pytest.fixture
def api_instance_stored_from_address(api_instance, inbound_from_address):
    """Instance of InboundShipments ready for request testing
    that includes a ``from_address``.
    """
    api = api_instance
    api.from_address = inbound_from_address
    return api


class TestLegacySetShipFromAddressCases(InboundShipmentsAPITestCase):
    """Test case covering ``from_address`` storage using the legacy dict."""

    def test_legacy_address_built_properly(self, api_instance):
        """An address with all fields covered should be constructed properly."""
        address = {
            "name": "Roland Deschain",
            "address_1": "500 Summat Cully Lane",
            "address_2": "Apartment 19",
            "city": "Gilead",
            "district_or_county": "West-Town",
            "state_or_province": "New Canaan",
            "postal_code": "13019",
            "country": "Mid-World",
        }
        api_instance.from_address = address
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": "Apartment 19",
            "City": "Gilead",
            "DistrictOrCounty": "West-Town",
            "StateOrProvinceCode": "New Canaan",
            "PostalCode": "13019",
            "CountryCode": "Mid-World",
        }
        assert output == expected

    def test_legacy_partial_address_built_properly(self, api_instance):
        """An address with only required fields covered should be constructed properly,
        with omitted keys filled in with defaults.
        """
        address = {
            "name": "Roland Deschain",
            "address_1": "500 Summat Cully Lane",
            "city": "Gilead",
        }
        api_instance.from_address = address
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert output == expected

    def test_set_legacy_address_with_constructor(self, mws_credentials):
        """An address passed to the InboundShipments constructor as a
        `from_address` kwarg should automatically set the `from_address` attribute
        (ignoring the self.inbound attribute in this case).
        """
        address = {
            "name": "Roland Deschain",
            "address_1": "500 Summat Cully Lane",
            "city": "Gilead",
        }
        inbound_constructed = InboundShipments(**mws_credentials, from_address=address)
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert inbound_constructed.from_address.to_params() == expected

    def test_set_legacy_address_with_legacy_setter(self, api_instance):
        """Using the (deprecated) ``set_ship_from_address`` should work similar to
        ``from_address`` property assignment.
        """
        address = {
            "name": "Roland Deschain",
            "address_1": "500 Summat Cully Lane",
            "city": "Gilead",
        }
        api_instance.set_ship_from_address(address)
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert output == expected


class TestSetShipFromAddressCases(InboundShipmentsAPITestCase):
    """Test case covering ``from_address`` storage using the ``Address`` model."""

    def test_ship_from_address_none(self, api_instance):
        """The from_address property does some complicated stuff, but it
        should behave normally if `None` is passed.
        """
        # Assignment through the property should set None for the underlying attr
        api_instance.from_address = None
        assert api_instance._from_address is None
        # And the return value for the property should also be None
        assert api_instance.from_address is None

        # Assignment of anything other than an Address model or Mapping raises MWSError
        with pytest.raises(MWSError):
            api_instance.from_address = "Not a mapping!"

    @pytest.mark.parametrize(
        "override_obj",
        (
            "String doesn't work",
            1,
            ("tuple?", "no way"),
            ["not", "a", "list"],
            {"not": "a", "dict": "either"},
        ),
    )
    def test_from_address_params_errors(self, override_obj, api_instance):
        """The from_address_params method is used as a shorthand for several actions,
        including using the stored from_address, supplying an override address,
        and/or providing a prefix.

        This tests those various cases.
        """
        # Override address must be an Address model
        with pytest.raises(MWSError):
            api_instance.from_address_params(from_address=override_obj)

    def test_from_address_params_override(
        self, from_address_params_expected, api_instance_stored_from_address
    ):
        """Using from_address_params, overriding the from_address with a new Address
        model should result in that address being used.
        """
        # First off, the default should return our expected values
        assert (
            api_instance_stored_from_address.from_address_params()
            == from_address_params_expected
        )

        # Using a new address with the same method should return the new params,
        # not the original.
        new_address = Address(
            name="Not The Original",
            address_line_1="45 Blabbity Rd",
            city="Chicago",
            country_code="NZ",
        )
        override_params = api_instance_stored_from_address.from_address_params(
            from_address=new_address
        )
        assert override_params == {
            "Name": "Not The Original",
            "AddressLine1": "45 Blabbity Rd",
            "AddressLine2": None,
            "City": "Chicago",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "NZ",
        }

        # Same as the expected overrides, with a prefix added.
        override_with_prefix = api_instance_stored_from_address.from_address_params(
            from_address=new_address, prefix="whatever"
        )
        assert override_with_prefix == {
            "whatever.Name": "Not The Original",
            "whatever.AddressLine1": "45 Blabbity Rd",
            "whatever.AddressLine2": None,
            "whatever.City": "Chicago",
            "whatever.DistrictOrCounty": None,
            "whatever.StateOrProvinceCode": None,
            "whatever.PostalCode": None,
            "whatever.CountryCode": "NZ",
        }

    def test_address_built_properly(self, api_instance):
        """An address with all fields covered should be constructed properly."""
        address = Address(
            name="Roland Deschain",
            address_line_1="500 Summat Cully Lane",
            address_line_2="Apartment 19",
            city="Gilead",
            district_or_county="West-Town",
            state_or_province_code="New Canaan",
            postal_code="13019",
            country_code="Mid-World",
        )
        api_instance.from_address = address
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": "Apartment 19",
            "City": "Gilead",
            "DistrictOrCounty": "West-Town",
            "StateOrProvinceCode": "New Canaan",
            "PostalCode": "13019",
            "CountryCode": "Mid-World",
        }
        assert output == expected

    def test_partial_address_built_properly(self, api_instance):
        """An address with only required fields covered should be constructed properly,
        with omitted keys filled in with defaults.
        """
        address = Address(
            name="Roland Deschain",
            address_line_1="500 Summat Cully Lane",
            city="Gilead",
        )
        api_instance.from_address = address
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert output == expected

    def test_set_address_with_constructor(self, mws_credentials):
        """An address passed to the InboundShipments constructor as a
        `from_address` kwarg should automatically set the `from_address` attribute
        (ignoring the self.inbound attribute in this case).
        """
        address = Address(
            name="Roland Deschain",
            address_line_1="500 Summat Cully Lane",
            city="Gilead",
        )
        inbound_constructed = InboundShipments(**mws_credentials, from_address=address)
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert inbound_constructed.from_address.to_params() == expected

    def test_set_address_with_legacy_setter(self, api_instance):
        """Using the (deprecated) ``set_ship_from_address`` should work similar to
        ``from_address`` property assignment.
        """
        address = Address(
            name="Roland Deschain",
            address_line_1="500 Summat Cully Lane",
            city="Gilead",
        )
        api_instance.set_ship_from_address(address)
        output = api_instance.from_address.to_params()
        expected = {
            "Name": "Roland Deschain",
            "AddressLine1": "500 Summat Cully Lane",
            "AddressLine2": None,
            "City": "Gilead",
            "DistrictOrCounty": None,
            "StateOrProvinceCode": None,
            "PostalCode": None,
            "CountryCode": "US",
        }
        assert output == expected


class TestCreateInboundShipmentPlan(InboundShipmentsAPITestCase):
    """Test cases for InboundShipments involving CreateInboundShipmentPlan operation."""

    api_class = InboundShipments

    def test_create_inbound_shipment_plan_no_items(
        self, api_instance_stored_from_address
    ):
        """`create_inbound_shipment_plan` should raise exception for no items."""
        items = []
        with pytest.raises(MWSError):
            api_instance_stored_from_address.create_inbound_shipment_plan(items)

    def test_create_inbound_shipment_plan_no_address(self, api_instance):
        """`create_inbound_shipment_plan` should raise exception for no from_address."""
        assert api_instance.from_address == {}
        items = [{"sku": "something", "quantity": 6}]
        # api_instance.from_address = None
        with pytest.raises(MWSError):
            api_instance.create_inbound_shipment_plan(items)

    def test_create_inbound_shipment_plan_item_models(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `create_inbound_shipment_plan`
        using item models.
        """
        items = [
            InboundShipmentPlanRequestItem("mySku1", 6),
            InboundShipmentPlanRequestItem("mySku2", 26),
        ]
        country_code = "Risa"
        subdivision_code = "Hotel California"
        label_preference = "SELLER"
        params = api_instance_stored_from_address.create_inbound_shipment_plan(
            items=items,
            country_code=country_code,
            subdivision_code=subdivision_code,
            label_preference=label_preference,
        )
        self.assert_common_params(params, action="CreateInboundShipmentPlan")

        expected = {
            "ShipToCountryCode": "Risa",
            "ShipToCountrySubdivisionCode": "Hotel%20California",
            "LabelPrepPreference": "SELLER",
            "InboundShipmentPlanRequestItems.member.1.SellerSKU": "mySku1",
            "InboundShipmentPlanRequestItems.member.1.Quantity": "6",
            "InboundShipmentPlanRequestItems.member.2.SellerSKU": "mySku2",
            "InboundShipmentPlanRequestItems.member.2.Quantity": "26",
        }

        for key, val in expected.items():
            assert params[key] == val

    def test_create_inbound_shipment_plan_wrong_model(
        self, api_instance_stored_from_address
    ):
        """Supplying the wrong item model class to `create_inbound_shipment_plan`
        should raise MWSError.
        """
        items = [
            InboundShipmentItem("mySku1", 6),
            InboundShipmentItem("mySku2", 26),
        ]
        country_code = "Risa"
        subdivision_code = "Hotel California"
        label_preference = "SELLER"
        with pytest.raises(MWSError):
            api_instance_stored_from_address.create_inbound_shipment_plan(
                items=items,
                country_code=country_code,
                subdivision_code=subdivision_code,
                label_preference=label_preference,
            )

    def test_create_inbound_shipment_plan_legacy_items(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `create_inbound_shipment_plan` using
        legacy item dicts.
        """
        items = [
            {"sku": "ievEKnILd3", "quantity": 6},
            {"sku": "9IfTM1aJVG", "quantity": 26},
        ]
        country_code = "Risa"
        subdivision_code = "Hotel California"
        label_preference = "SELLER"
        params = api_instance_stored_from_address.create_inbound_shipment_plan(
            items=items,
            country_code=country_code,
            subdivision_code=subdivision_code,
            label_preference=label_preference,
        )
        self.assert_common_params(params, action="CreateInboundShipmentPlan")

        expected = {
            "ShipToCountryCode": "Risa",
            "ShipToCountrySubdivisionCode": "Hotel%20California",
            "LabelPrepPreference": "SELLER",
            "InboundShipmentPlanRequestItems.member.1.SellerSKU": "ievEKnILd3",
            "InboundShipmentPlanRequestItems.member.1.Quantity": "6",
            "InboundShipmentPlanRequestItems.member.2.SellerSKU": "9IfTM1aJVG",
            "InboundShipmentPlanRequestItems.member.2.Quantity": "26",
        }

        for key, val in expected.items():
            assert params[key] == val


class TestCreateInboundShipment(InboundShipmentsAPITestCase):
    """Test cases for InboundShipments involving CreateInboundShipmentPlan operation."""

    api_class = InboundShipments

    def test_create_inbound_shipment_no_items(self, api_instance_stored_from_address):
        """Covers cases that should raise exceptions for the
        `create_inbound_shipment` method.
        """
        # Proper inputs (initial setup)
        shipment_id = "is_a_string"
        shipment_name = "is_a_string"
        destination = "is_a_string"
        items = []
        with pytest.raises(MWSError):
            api_instance_stored_from_address.create_inbound_shipment(
                shipment_id, shipment_name, destination, items
            )

    def test_create_inbound_shipment_no_address(self, api_instance):
        """Covers cases that should raise exceptions for the
        `create_inbound_shipment` method.
        """
        assert api_instance.from_address == {}
        # Proper inputs (initial setup)
        shipment_id = "is_a_string"
        shipment_name = "is_a_string"
        destination = "is_a_string"
        items = [{"sku": "something", "quantity": 6}]  # reset

        # 5: wipe out the `from_address` for the API class before calling: raises MWSError
        with pytest.raises(MWSError):
            api_instance.create_inbound_shipment(
                shipment_id, shipment_name, destination, items
            )

    def test_create_inbound_shipment_legacy_items(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `create_inbound_shipment`
        using legacy item dicts.
        """
        shipment_id = "b46sEL7sYX"
        shipment_name = "Stuff Going Places"
        destination = "MyDestination"
        items = [
            {"sku": "mySku1", "quantity": 12},
            {"sku": "mySku2", "quantity": 35},
        ]
        shipment_status = "RECEIVED"
        label_preference = "AMAZON"
        case_required = True
        box_contents_source = "Boxes"
        params = api_instance_stored_from_address.create_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params, action="CreateInboundShipment")
        expected = {
            "ShipmentId": "b46sEL7sYX",
            "InboundShipmentHeader.ShipmentName": "Stuff%20Going%20Places",
            "InboundShipmentHeader.DestinationFulfillmentCenterId": "MyDestination",
            "InboundShipmentHeader.LabelPrepPreference": "AMAZON",
            "InboundShipmentHeader.AreCasesRequired": "true",
            "InboundShipmentHeader.ShipmentStatus": "RECEIVED",
            "InboundShipmentHeader.IntendedBoxContentsSource": "Boxes",
            # item data
            "InboundShipmentItems.member.1.SellerSKU": "mySku1",
            "InboundShipmentItems.member.1.QuantityShipped": "12",
            "InboundShipmentItems.member.2.SellerSKU": "mySku2",
            "InboundShipmentItems.member.2.QuantityShipped": "35",
        }
        for key, val in expected.items():
            assert params[key] == val

    def test_create_inbound_shipment_item_models(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `create_inbound_shipment`
        using item models.
        """
        shipment_id = "b46sEL7sYX"
        shipment_name = "Stuff Going Places"
        destination = "MyDestination"
        items = [
            InboundShipmentItem("mySku1", 12),
            InboundShipmentItem("mySku2", 35),
        ]
        shipment_status = "RECEIVED"
        label_preference = "AMAZON"
        case_required = True
        box_contents_source = "Boxes"
        params = api_instance_stored_from_address.create_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params, action="CreateInboundShipment")
        expected = {
            "ShipmentId": "b46sEL7sYX",
            "InboundShipmentHeader.ShipmentName": "Stuff%20Going%20Places",
            "InboundShipmentHeader.DestinationFulfillmentCenterId": "MyDestination",
            "InboundShipmentHeader.LabelPrepPreference": "AMAZON",
            "InboundShipmentHeader.AreCasesRequired": "true",
            "InboundShipmentHeader.ShipmentStatus": "RECEIVED",
            "InboundShipmentHeader.IntendedBoxContentsSource": "Boxes",
            # item data
            "InboundShipmentItems.member.1.SellerSKU": "mySku1",
            "InboundShipmentItems.member.1.QuantityShipped": "12",
            "InboundShipmentItems.member.2.SellerSKU": "mySku2",
            "InboundShipmentItems.member.2.QuantityShipped": "35",
        }
        for key, val in expected.items():
            assert params[key] == val

    def test_create_inbound_shipment_wrong_model(
        self, api_instance_stored_from_address
    ):
        """Using CreateInboundShipment with the incorrect item model should
        raise MWSError.
        """
        shipment_id = "b46sEL7sYX"
        shipment_name = "Stuff Going Places"
        destination = "MyDestination"
        items = [
            InboundShipmentPlanRequestItem("mySku1", 12),
            InboundShipmentPlanRequestItem("mySku2", 35),
        ]
        shipment_status = "RECEIVED"
        label_preference = "AMAZON"
        case_required = True
        box_contents_source = "Boxes"
        with pytest.raises(MWSError):
            api_instance_stored_from_address.create_inbound_shipment(
                shipment_id=shipment_id,
                shipment_name=shipment_name,
                destination=destination,
                items=items,
                shipment_status=shipment_status,
                label_preference=label_preference,
                case_required=case_required,
                box_contents_source=box_contents_source,
            )


class TestUpdateInboundShipment(InboundShipmentsAPITestCase):
    """Test cases for InboundShipments involving CreateInboundShipmentPlan operation."""

    api_class = InboundShipments

    def test_update_inbound_shipment_legacy_items(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `update_inbound_shipment`
        using legacy item dicts.
        """
        shipment_id = "7DzXpBVxRR"
        shipment_name = "Stuff Going Places"
        destination = "Vulcan"
        items = [
            {"sku": "mySku1", "quantity": 98},
            {"sku": "mySku2", "quantity": 65},
        ]
        shipment_status = "WORKING"
        label_preference = "SELLER_LABEL"
        case_required = True
        box_contents_source = "Boxes"

        params = api_instance_stored_from_address.update_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params)

        expected = {
            "Action": "UpdateInboundShipment",
            "ShipmentId": "7DzXpBVxRR",
            "InboundShipmentHeader.ShipmentName": "Stuff%20Going%20Places",
            "InboundShipmentHeader.DestinationFulfillmentCenterId": "Vulcan",
            "InboundShipmentHeader.LabelPrepPreference": "SELLER_LABEL",
            "InboundShipmentHeader.AreCasesRequired": "true",
            "InboundShipmentHeader.ShipmentStatus": "WORKING",
            "InboundShipmentHeader.IntendedBoxContentsSource": "Boxes",
            "InboundShipmentItems.member.1.SellerSKU": "mySku1",
            "InboundShipmentItems.member.1.QuantityShipped": "98",
            "InboundShipmentItems.member.2.SellerSKU": "mySku2",
            "InboundShipmentItems.member.2.QuantityShipped": "65",
        }
        for key, val in expected.items():
            assert params[key] == val

    def test_update_inbound_shipment_item_models(
        self, api_instance_stored_from_address
    ):
        """Covers successful data entry for `update_inbound_shipment`
        using item models.
        """
        shipment_id = "7DzXpBVxRR"
        shipment_name = "Stuff Going Places"
        destination = "Vulcan"
        items = [
            InboundShipmentItem("mySku1", 98),
            InboundShipmentItem("mySku2", 65),
        ]
        shipment_status = "WORKING"
        label_preference = "SELLER_LABEL"
        case_required = True
        box_contents_source = "Boxes"

        params = api_instance_stored_from_address.update_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            items=items,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params)

        expected = {
            "Action": "UpdateInboundShipment",
            "ShipmentId": "7DzXpBVxRR",
            "InboundShipmentHeader.ShipmentName": "Stuff%20Going%20Places",
            "InboundShipmentHeader.DestinationFulfillmentCenterId": "Vulcan",
            "InboundShipmentHeader.LabelPrepPreference": "SELLER_LABEL",
            "InboundShipmentHeader.AreCasesRequired": "true",
            "InboundShipmentHeader.ShipmentStatus": "WORKING",
            "InboundShipmentHeader.IntendedBoxContentsSource": "Boxes",
            "InboundShipmentItems.member.1.SellerSKU": "mySku1",
            "InboundShipmentItems.member.1.QuantityShipped": "98",
            "InboundShipmentItems.member.2.SellerSKU": "mySku2",
            "InboundShipmentItems.member.2.QuantityShipped": "65",
        }
        for key, val in expected.items():
            assert params[key] == val

    def test_update_inbound_shipment_wrong_model(
        self, api_instance_stored_from_address
    ):
        """Giving the wrong Item model type to UpdateInboundShipment should
        raise MWSError.
        """
        shipment_id = "7DzXpBVxRR"
        shipment_name = "Stuff Going Places"
        destination = "Vulcan"
        items = [
            InboundShipmentPlanRequestItem("mySku1", 98),
            InboundShipmentPlanRequestItem("mySku2", 65),
        ]
        shipment_status = "WORKING"
        label_preference = "SELLER_LABEL"
        case_required = True
        box_contents_source = "Boxes"

        with pytest.raises(MWSError):
            api_instance_stored_from_address.update_inbound_shipment(
                shipment_id=shipment_id,
                shipment_name=shipment_name,
                destination=destination,
                items=items,
                shipment_status=shipment_status,
                label_preference=label_preference,
                case_required=case_required,
                box_contents_source=box_contents_source,
            )

    def test_update_inbound_shipment_no_items(self, api_instance_stored_from_address):
        """Additional case: no items required.
        Params should have no Items keys if not provided
        """
        shipment_id = "7DzXpBVxRR"
        shipment_name = "Stuff Going Places"
        destination = "Vulcan"
        shipment_status = "WORKING"
        label_preference = "SELLER_LABEL"
        case_required = True
        box_contents_source = "Boxes"

        params = api_instance_stored_from_address.update_inbound_shipment(
            shipment_id=shipment_id,
            shipment_name=shipment_name,
            destination=destination,
            shipment_status=shipment_status,
            label_preference=label_preference,
            case_required=case_required,
            box_contents_source=box_contents_source,
        )
        self.assert_common_params(params)

        expected = {
            "Action": "UpdateInboundShipment",
            "ShipmentId": "7DzXpBVxRR",
            "InboundShipmentHeader.ShipmentName": "Stuff%20Going%20Places",
            "InboundShipmentHeader.DestinationFulfillmentCenterId": "Vulcan",
            "InboundShipmentHeader.LabelPrepPreference": "SELLER_LABEL",
            "InboundShipmentHeader.AreCasesRequired": "true",
            "InboundShipmentHeader.ShipmentStatus": "WORKING",
            "InboundShipmentHeader.IntendedBoxContentsSource": "Boxes",
        }
        for key, val in expected.items():
            assert params[key] == val

        # items keys should not be present
        param_item_keys = [
            x for x in params.keys() if x.startswith("InboundShipmentItems")
        ]
        # list should be empty, because no keys should be present
        assert not param_item_keys

    def test_update_inbound_shipment_no_address(self, api_instance):
        """UpdateInboundShipment with no from address should raise exception."""
        assert api_instance.from_address == {}
        shipment_id = "7DzXpBVxRR"
        shipment_name = "Stuff Going Places"
        destination = "Vulcan"
        shipment_status = "WORKING"
        label_preference = "SELLER_LABEL"
        case_required = True
        box_contents_source = "Boxes"

        with pytest.raises(MWSError):
            api_instance.update_inbound_shipment(
                shipment_id=shipment_id,
                shipment_name=shipment_name,
                destination=destination,
                shipment_status=shipment_status,
                label_preference=label_preference,
                case_required=case_required,
                box_contents_source=box_contents_source,
            )


class TestInboundShipmentsRequests(InboundShipmentsAPITestCase):
    """Test cases for InboundShipments requests that do not involve
    FBA shipment handling and do not require `from_address` to be set.
    """

    api_class = InboundShipments

    def test_get_inbound_guidance_for_sku(self, api_instance):
        """GetInboundGuidanceForSKU operation."""
        # Case 1: list of SKUs
        sku_list_1 = [
            "mySku1",
            "mySku2",
        ]
        params_1 = api_instance.get_inbound_guidance_for_sku(
            skus=sku_list_1,
            marketplace_id="myMarketplaceId",
        )
        self.assert_common_params(params_1, action="GetInboundGuidanceForSKU")
        assert params_1["MarketplaceId"] == "myMarketplaceId"
        assert params_1["SellerSKUList.Id.1"] == "mySku1"
        assert params_1["SellerSKUList.Id.2"] == "mySku2"
        # Case 2: single SKU
        params_2 = api_instance.get_inbound_guidance_for_sku(
            skus="mySku3",
            marketplace_id="myMarketplaceId",
        )
        self.assert_common_params(params_2)
        assert params_2["SellerSKUList.Id.1"] == "mySku3"
        assert "SellerSKUList.Id.2" not in params_2

    def test_get_inbound_guidance_for_asin(self, api_instance):
        """GetInboundGuidanceForASIN operation."""
        # Case 1: list of ASINs
        params_1 = api_instance.get_inbound_guidance_for_asin(
            asins=["myAsin1", "myAsin2"],
            marketplace_id="myMarketplaceId",
        )
        self.assert_common_params(params_1, action="GetInboundGuidanceForASIN")
        assert params_1["MarketplaceId"] == "myMarketplaceId"
        assert params_1["ASINList.Id.1"] == "myAsin1"
        assert params_1["ASINList.Id.2"] == "myAsin2"

        # Case 2: single SKU
        params_2 = api_instance.get_inbound_guidance_for_asin(
            asins="myAsin3",
            marketplace_id="myMarketplaceId",
        )
        self.assert_common_params(params_2)
        assert params_2["ASINList.Id.1"] == "myAsin3"
        assert "ASINList.Id.2" not in params_2

    def test_get_preorder_info(self, api_instance):
        """GetPreorderInfo operation."""
        params = api_instance.get_preorder_info("oYRjQbGLL6")
        self.assert_common_params(params, action="GetPreorderInfo")
        assert params["ShipmentId"] == "oYRjQbGLL6"

    def test_confirm_preorder(self, api_instance):
        """ConfirmPreorder operation."""
        params = api_instance.confirm_preorder(
            shipment_id="H4UiUjY7Fr",
            need_by_date=datetime.datetime(2020, 10, 12),
        )
        self.assert_common_params(params, action="ConfirmPreorder")
        assert params["ShipmentId"] == "H4UiUjY7Fr"
        assert params["NeedByDate"] == "2020-10-12T00%3A00%3A00"

    def test_get_prep_instructions_for_sku(self, api_instance):
        """GetPrepInstructionsForSKU operation."""
        # Case 1: simple list
        params_1 = api_instance.get_prep_instructions_for_sku(
            skus=["mySku1", "mySku2"],
            country_code="MyCountryCode",
        )
        self.assert_common_params(params_1, action="GetPrepInstructionsForSKU")
        assert params_1["ShipToCountryCode"] == "MyCountryCode"
        assert params_1["SellerSKUList.ID.1"] == "mySku1"
        assert params_1["SellerSKUList.ID.2"] == "mySku2"

        # Case 2: duplicates should be removed before creating params,
        # with their ordering preserved.
        # mySkuDupe1 is the duplicate, in pos 0 and 2 (the second one should be ignored)
        params_2 = api_instance.get_prep_instructions_for_sku(
            skus=["mySkuDupe1", "mySkuDupe2", "mySkuDupe1", "mySkuDupe3", "mySkuDupe4"],
            country_code="MyCountryCode",
        )
        assert params_2["SellerSKUList.ID.1"] == "mySkuDupe1"
        assert params_2["SellerSKUList.ID.2"] == "mySkuDupe2"
        assert params_2["SellerSKUList.ID.3"] == "mySkuDupe3"
        assert params_2["SellerSKUList.ID.4"] == "mySkuDupe4"
        # The second instance of `mySkuDupe` is ignored, and the ordering is preserved.

    def test_get_prep_instructions_for_asin(self, api_instance):
        """GetPrepInstructionsForASIN operation."""
        # Case 1: simple list
        params_1 = api_instance.get_prep_instructions_for_asin(
            asins=["myAsin1", "myAsin2"],
            country_code="MyCountryCode",
        )
        self.assert_common_params(params_1, action="GetPrepInstructionsForASIN")
        assert params_1["ShipToCountryCode"] == "MyCountryCode"
        assert params_1["ASINList.ID.1"] == "myAsin1"
        assert params_1["ASINList.ID.2"] == "myAsin2"
        # Case 2: duplicates should be removed before creating params,
        # with their ordering preserved.
        # "myDupeAsin3" should only appear once
        params_2 = api_instance.get_prep_instructions_for_asin(
            asins=[
                "myDupeAsin1",
                "myDupeAsin2",
                "myDupeAsin3",
                "myDupeAsin3",
                "myDupeAsin4",
            ],
            country_code="MyCountryCode",
        )
        self.assert_common_params(params_2)
        assert params_2["ASINList.ID.1"] == "myDupeAsin1"
        assert params_2["ASINList.ID.2"] == "myDupeAsin2"
        assert params_2["ASINList.ID.3"] == "myDupeAsin3"
        assert params_2["ASINList.ID.4"] == "myDupeAsin4"

    @pytest.mark.parametrize(
        "method_name, action",
        (
            ("estimate_transport_request", "EstimateTransportRequest"),
            ("get_transport_content", "GetTransportContent"),
            ("confirm_transport_request", "ConfirmTransportRequest"),
            ("void_transport_request", "VoidTransportRequest"),
            ("get_bill_of_lading", "GetBillOfLading"),
        ),
    )
    def test_shipment_id_only_requests(self, api_instance, method_name, action):
        """Test the output of methods that only require the shipment ID argument."""
        method = getattr(api_instance, method_name)
        params = method("myShipmentId")
        self.assert_common_params(params, action=action)
        assert params["ShipmentId"] == "myShipmentId"

    def test_get_package_labels(self, api_instance):
        """GetPackageLabels operation."""
        params = api_instance.get_package_labels(
            shipment_id="myShipmentId",
            num_labels=53,
            page_type="PackageLabel_Letter_6",
        )
        self.assert_common_params(params, action="GetPackageLabels")
        assert params["ShipmentId"] == "myShipmentId"
        assert params["PageType"] == "PackageLabel_Letter_6"
        assert params["NumberOfPackages"] == "53"

    def test_get_unique_package_labels(self, api_instance):
        """GetUniquePackageLabels operation."""
        # Case 1: list of package_ids
        params_1 = api_instance.get_unique_package_labels(
            shipment_id="myShipmentId",
            page_type="PackageLabel_Plain_Paper",
            package_ids=["myPackage1", "myPackage2"],
        )
        self.assert_common_params(params_1, action="GetUniquePackageLabels")
        assert params_1["ShipmentId"] == "myShipmentId"
        assert params_1["PageType"] == "PackageLabel_Plain_Paper"
        assert params_1["PackageLabelsToPrint.member.1"] == "myPackage1"
        assert params_1["PackageLabelsToPrint.member.2"] == "myPackage2"

        # Case 2: single string package_id (should still work)
        params_2 = api_instance.get_unique_package_labels(
            shipment_id="myShipmentId",
            page_type="PackageLabel_Plain_Paper",
            package_ids="myShipment3",
        )
        assert params_2["PackageLabelsToPrint.member.1"] == "myShipment3"
        assert "PackageLabelsToPrint.member.2" not in params_2

    def test_get_pallet_labels(self, api_instance):
        """GetPalletLabels operation."""
        params = api_instance.get_pallet_labels(
            shipment_id="myShipmentId",
            page_type="PackageLabel_A4_4",
            num_labels=69,
        )
        self.assert_common_params(params, action="GetPalletLabels")
        assert params["ShipmentId"] == "myShipmentId"
        assert params["PageType"] == "PackageLabel_A4_4"
        assert params["NumberOfPallets"] == "69"

    def test_list_inbound_shipments(self, api_instance):
        """ListInboundShipments operation."""
        params = api_instance.list_inbound_shipments(
            shipment_ids=["myShipment1", "myShipment2"],
            shipment_statuses=["CANCELLED", "IN_TRANSIT"],
            last_updated_before=datetime.datetime(2020, 10, 12),
            last_updated_after=datetime.datetime(2020, 10, 12)
            + datetime.timedelta(hours=1),
        )
        self.assert_common_params(params, action="ListInboundShipments")
        assert params["LastUpdatedBefore"] == "2020-10-12T00%3A00%3A00"
        assert params["LastUpdatedAfter"] == "2020-10-12T01%3A00%3A00"
        assert params["ShipmentStatusList.member.1"] == "CANCELLED"
        assert params["ShipmentStatusList.member.2"] == "IN_TRANSIT"
        assert params["ShipmentIdList.member.1"] == "myShipment1"
        assert params["ShipmentIdList.member.2"] == "myShipment2"

    def test_list_inbound_shipment_items(self, api_instance):
        """ListInboundShipmentItems operation."""
        params = api_instance.list_inbound_shipment_items(
            shipment_id="P9NLpC2Afi",
            last_updated_before=datetime.datetime(2020, 10, 12),
            last_updated_after=datetime.datetime(2020, 10, 12)
            + datetime.timedelta(hours=1),
        )
        self.assert_common_params(params, action="ListInboundShipmentItems")
        assert params["ShipmentId"] == "P9NLpC2Afi"
        assert params["LastUpdatedBefore"] == "2020-10-12T00%3A00%3A00"
        assert params["LastUpdatedAfter"] == "2020-10-12T01%3A00%3A00"

    def test_next_token_methods(self, api_instance):
        """Check content of methods that can use next_tokens"""
        mapping = (
            (
                "list_inbound_shipments",
                "ListInboundShipmentsByNextToken",
            ),
            (
                "list_inbound_shipment_items",
                "ListInboundShipmentItemsByNextToken",
            ),
        )
        for methodname, action in mapping:
            method = getattr(api_instance, methodname)
            params = method(next_token="my_next_token")
            self.assert_common_params(params, action=action)
            assert params["NextToken"] == "my_next_token"

    def test_next_token_alias_methods(self, api_instance):
        """Check content of alias method that can use next_tokens."""
        mapping = (
            (
                "list_inbound_shipments_by_next_token",
                "ListInboundShipmentsByNextToken",
            ),
            (
                "list_inbound_shipment_items_by_next_token",
                "ListInboundShipmentItemsByNextToken",
            ),
        )
        for methodname, action in mapping:
            method = getattr(api_instance, methodname)
            params = method("my_next_token")
            self.assert_common_params(params, action=action)
            assert params["NextToken"] == "my_next_token"

    @pytest.mark.parametrize(
        "statuses",
        [
            "STATUS1",
            ["STATUS1", "STATUS2"],  # list
            ("STATUS1", "STATUS2"),  # tuple
            {"STATUS1", "STATUS2"},  # set
            list(),  # empty list
            tuple(),  # empty tuple
            set(),  # empty set
            None,
        ],
    )
    @pytest.mark.parametrize(
        "ids",
        [
            "ID1",
            ["ID1", "ID2"],  # list
            ("ID1", "ID2"),  # tuple
            {"ID1", "ID2"},  # set
            list(),  # empty list
            tuple(),  # empty tuple
            set(),  # empty set
            None,
        ],
    )
    def test_list_inbound_shipments_status_and_id(
        self, api_instance_stored_from_address, statuses, ids
    ):
        """Check that a mixture of different argument types for `shipment_statuses`
        and `shipment_ids` will work in `InboundShipments.list_inbound_shipments`.

        Should cover scenarios like ticket #199.
        """
        api = api_instance_stored_from_address
        params = api.list_inbound_shipments(
            shipment_statuses=statuses, shipment_ids=ids
        )

        # Check statuses:
        if statuses is None:
            # Explicitly `None`, should output nothing
            assert "ShipmentStatusList.member.1" not in params
        if not statuses:
            # Evaluates "falsey", should output nothing
            assert "ShipmentStatusList.member.1" not in params
        if isinstance(statuses, str):
            # Single entry string should have one member only.
            assert params["ShipmentStatusList.member.1"] == statuses
            assert "ShipmentStatusList.member.2" not in params
        if isinstance(statuses, (list, tuple, set)):
            for idx, status in enumerate(statuses, start=1):
                key = "ShipmentStatusList.member.{}".format(idx)
                assert params[key] == status

        # Check IDs:
        if ids is None:
            # Explicitly `None`, should output nothing
            assert "ShipmentIdList.member.1" not in params
        if not ids:
            # Evaluates "falsey", should output nothing
            assert "ShipmentIdList.member.1" not in params
        if isinstance(ids, str):
            # Single entry string should have one member only.
            assert params["ShipmentIdList.member.1"] == ids
            assert "ShipmentIdList.member.2" not in params
        if isinstance(ids, (list, tuple, set)):
            for idx, id_ in enumerate(ids, start=1):
                key = "ShipmentIdList.member.{}".format(idx)
                assert params[key] == id_


@pytest.mark.parametrize(
    "item",
    (
        "Not a mapping object",
        {"sku": "missing quantity key"},
        {"quantity": "missing sku key"},
    ),
)
def test_legacy_item_dict_errors(item):
    """Specific instances using parse_legacy_item should raise MWSError"""
    with pytest.raises(MWSError):
        parse_legacy_item(item, "OperationIrrelevant")


@pytest.mark.parametrize(
    "items",
    (
        list(),
        tuple(),
        set(),
    ),
)
def test_parse_shipment_items_errors(items):
    """Cases where the items collection passed to parse_shipment_items
    are empty should raise MWSError.
    """
    with pytest.raises(MWSError):
        parse_shipment_items(items)


def test_inbound_shipment_item_from_plan_constructor(
    create_inbound_shipment_plan_dummy_response,
):
    """Check the output of the `from_plan_item` alternate constructor
    for the InboundShipmentItem model.
    """
    resp_parsed = create_inbound_shipment_plan_dummy_response.parsed
    # Pull out the single item from this dummy plan
    item = resp_parsed.InboundShipmentPlans.member.Items.member
    item_model_1 = InboundShipmentItem.from_plan_item(item)
    assert item_model_1.sku == "SKU00001"
    assert item_model_1.quantity == "1"
    assert item_model_1.quantity_in_case is None
    assert item_model_1.release_date is None
    assert item_model_1.prep_details_list[0].prep_instruction == "Taping"
    assert item_model_1.prep_details_list[0].prep_owner == "AMAZON"

    # FNSKU injection is a special case of this constructor.
    assert item_model_1.fnsku == "FNSKU00001"

    # Do the same, but add quantity_in_case and release_date
    item_model_2 = InboundShipmentItem.from_plan_item(
        item, quantity_in_case=4, release_date=datetime.datetime(2020, 11, 3)
    )
    assert item_model_2.quantity_in_case == 4
    assert item_model_2.release_date == datetime.datetime(2020, 11, 3)


def test_inbound_shipment_items_in_bulk(
    create_inbound_shipment_plan_dummy_response,
):
    """Check the output of the `shipment_items_from_plan` bulk processor."""
    resp_parsed = create_inbound_shipment_plan_dummy_response.parsed
    items_1 = shipment_items_from_plan(resp_parsed.InboundShipmentPlans.member)
    # Pull out the single item from this dummy plan
    assert items_1[0].sku == "SKU00001"
    assert items_1[0].quantity == "1"
    assert items_1[0].quantity_in_case is None
    assert items_1[0].release_date is None
    assert items_1[0].prep_details_list[0].prep_instruction == "Taping"
    assert items_1[0].prep_details_list[0].prep_owner == "AMAZON"

    # FNSKU injection is a special case of this constructor.
    assert items_1[0].fnsku == "FNSKU00001"

    # provide overrides via dictionary
    items_2 = shipment_items_from_plan(
        resp_parsed.InboundShipmentPlans.member,
        overrides={
            "SKU00001": {
                "quantity_in_case": 4,
                "release_date": datetime.datetime(2020, 11, 3),
            }
        },
    )
    assert items_2[0].quantity_in_case == 4
    assert items_2[0].release_date == datetime.datetime(2020, 11, 3)

    # provide overrides via ExtraItemData dataclass
    items_3 = shipment_items_from_plan(
        resp_parsed.InboundShipmentPlans.member,
        overrides={
            "SKU00001": ExtraItemData(
                quantity_in_case=12,
                release_date=datetime.datetime(2020, 12, 25),
            )
        },
    )
    assert items_3[0].quantity_in_case == 12
    assert items_3[0].release_date == datetime.datetime(2020, 12, 25)


def test_inbound_shipment_items_in_bulk_parent_key(
    create_inbound_shipment_plan_dummy_response,
):
    """Check the output of the `shipment_items_from_plan` bulk processor
    when using the parent node, InboundShipmentPlans, instead of the member node.
    """
    resp_parsed = create_inbound_shipment_plan_dummy_response.parsed
    items_1 = shipment_items_from_plan(resp_parsed.InboundShipmentPlans)
    # Pull out the single item from this dummy plan
    assert items_1[0].sku == "SKU00001"
    assert items_1[0].quantity == "1"
    assert items_1[0].quantity_in_case is None
    assert items_1[0].release_date is None
    assert items_1[0].prep_details_list[0].prep_instruction == "Taping"
    assert items_1[0].prep_details_list[0].prep_owner == "AMAZON"


def test_inbound_shipment_items_in_bulk_error(simple_mwsresponse_with_resultkey):
    """Bulk processor `shipment_items_from_plan` should raise ValueError
    if an incorrect node has been provided.

    Use an incorrect response type to test this, as it won't have the "Items"
    or "member" keys we need.
    """
    resp_parsed = simple_mwsresponse_with_resultkey.parsed
    with pytest.raises(ValueError):
        shipment_items_from_plan(resp_parsed.Products)
