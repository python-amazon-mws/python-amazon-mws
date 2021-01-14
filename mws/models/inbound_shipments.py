"""DataType models for InboundShipments API."""

import datetime
from enum import Enum
from typing import (
    Dict,
    List,
    Optional,
    Union,
)

from mws.models.base import MWSDataType
from mws.utils.collections import DotDict
from mws.utils.params import enumerate_keyed_param

__all__ = [
    "Address",
    "PrepInstruction",
    "PrepDetails",
    "ItemCondition",
    "InboundShipmentPlanRequestItem",
    "InboundShipmentItem",
    "ExtraItemData",
    "shipment_items_from_plan",
]


class Address(MWSDataType):
    """Postal address information.

    `MWS docs: Address Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#Address>`_
    """

    def __init__(
        self,
        name: Optional[str] = None,
        address_line_1: Optional[str] = None,
        address_line_2: Optional[str] = None,
        city: Optional[str] = None,
        district_or_county: Optional[str] = None,
        state_or_province_code: Optional[str] = None,
        country_code: str = "US",
        postal_code: Optional[Union[str, int]] = None,
    ):
        self.name = name
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.district_or_county = district_or_county
        self.state_or_province_code = state_or_province_code
        self.country_code = country_code
        self.postal_code = postal_code

    def params_dict(self) -> dict:
        return {
            "Name": self.name,
            "AddressLine1": self.address_line_1,
            "AddressLine2": self.address_line_2,
            "City": self.city,
            "DistrictOrCounty": self.district_or_county,
            "StateOrProvinceCode": self.state_or_province_code,
            "CountryCode": self.country_code,
            "PostalCode": self.postal_code,
        }

    @classmethod
    def from_legacy_dict(cls, value: dict) -> "Address":
        """Create an Address from a legacy structured dict."""
        legacy_keys = [
            "name",
            "address_1",
            "address_2",
            "city",
            "district_or_county",
            "state_or_province",
            "postal_code",
            "country",
        ]
        conversions = {
            "address_1": "address_line_1",
            "address_2": "address_line_2",
            "state_or_province": "state_or_province_code",
            "country": "country_code",
        }
        addr = {}
        for key, val in value.items():
            if key in legacy_keys:
                # Convert a key to a new version if present,
                # or use the old one
                outkey = conversions.get(key, key)
                addr[outkey] = val
        return cls(**addr)


class PrepInstruction(Enum):
    """Enumeration of preparation instruction types.

    `MWS docs: PrepInstruction Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#PrepInstruction>`_

    Provides constants for each prep type:

    - POLYBAGGING - Indicates that polybagging is required.
    - BUBBLEWRAPPING - Indicates that bubble wrapping is required.
    - TAPING - Indicates that taping is required.
    - BLACKSHRINKWRAPPING - Indicates that black shrink wrapping is required.
    - LABELING - Indicates that the FNSKU label should be applied to the item.
    - HANGGARMENT - Indicates that the item should be placed on a hanger.
    """

    POLYBAGGING = ("Polybagging", "polybagging is required")
    BUBBLEWRAPPING = ("BubbleWrapping", "bubble wrapping is required")
    TAPING = ("Taping", "taping is required")
    BLACKSHRINKWRAPPING = ("BlackShrinkWrapping", "black shrink wrapping is required")
    LABELING = ("Labeling", "the FNSKU label should be applied to the item")
    HANGGARMENT = ("HangGarment", "the item should be placed on a hanger")

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @property
    def value(self):
        return self.code


class PrepDetails(MWSDataType):
    """A preparation instruction, and who is responsible for that preparation.

    `MWS docs: PrepDetails Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#PrepDetails>`_

    ``prep_instruction`` accepts either a string or an instance of the :py:class:`PrepInstruction
    <mws.models.inbound_shipments.PrepInstruction>` enum, detailing the type of prep
    to perform. When using a string, the value should match one of the
    ``PrepInstruction.<PREP>.code`` values.

    ``prep_owner`` (optional) accepts a string, typically "AMAZON" or "SELLER", to
    indicate who is responsible for the prep. You can use ``PrepDetails.AMAZON``
    or ``PrepDetails.SELLER`` to fill in these values. Defaults to "SELLER".
    """

    AMAZON = "AMAZON"
    SELLER = "SELLER"

    def __init__(
        self,
        prep_instruction: Union[PrepInstruction, str],
        prep_owner: str = SELLER,
    ):
        self.prep_instruction = prep_instruction
        self.prep_owner = prep_owner

    def params_dict(self) -> dict:
        return {
            "PrepInstruction": self.prep_instruction,
            "PrepOwner": self.prep_owner,
        }


class ItemCondition(Enum):
    """Condition value for an item included with a CreateInboundShipmentPlan request.

    `MWS docs: InboundShipmentPlanRequestItem Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#InboundShipmentPlanRequestItem>`_

    Values provided:

    - NEW_ITEM
    - NEW_WITH_WARRANTY
    - NEW_OEM
    - NEW_OPEN_BOX
    - USED_LIKE_NEW
    - USED_VERY_GOOD
    - USED_GOOD
    - USED_ACCEPTABLE
    - USED_POOR
    - USED_REFURBISHED
    - COLLECTIBLE_LIKE_NEW
    - COLLECTIBLE_VERY_GOOD
    - COLLECTIBLE_GOOD
    - COLLECTIBLE_ACCEPTABLE
    - COLLECTIBLE_POOR
    - REFURBISHED_WITH_WARRANTY
    - REFURBISHED
    - CLUB
    """

    NEW_ITEM = "NewItem"
    NEW_WITH_WARRANTY = "NewWithWarranty"
    NEW_OEM = "NewOEM"
    NEW_OPEN_BOX = "NewOpenBox"
    USED_LIKE_NEW = "UsedLikeNew"
    USED_VERY_GOOD = "UsedVeryGood"
    USED_GOOD = "UsedGood"
    USED_ACCEPTABLE = "UsedAcceptable"
    USED_POOR = "UsedPoor"
    USED_REFURBISHED = "UsedRefurbished"
    COLLECTIBLE_LIKE_NEW = "CollectibleLikeNew"
    COLLECTIBLE_VERY_GOOD = "CollectibleVeryGood"
    COLLECTIBLE_GOOD = "CollectibleGood"
    COLLECTIBLE_ACCEPTABLE = "CollectibleAcceptable"
    COLLECTIBLE_POOR = "CollectiblePoor"
    REFURBISHED_WITH_WARRANTY = "RefurbishedWithWarranty"
    REFURBISHED = "Refurbished"
    CLUB = "Club"


class BaseInboundShipmentItem(MWSDataType):
    """Base class for Item information for creating an shipments and shipment plans.

    Subclasses of this class may be submitted with a call to the either
    ``create_inbound_shipment_plan`` or ``create_inbound_shipment``,
    depending on the nature of that particular subclass.

    Only ``sku`` and ``quantity`` are required for each item.
    Include ``quantity_in_case`` if your items are case-packed.

    ``prep_details_list`` (optional) expects an iterable of :py:class:`PrepDetails
    <mws.models.inbound_shipments.PrepDetails>` instances.
    """

    quantity_param = ""
    """The key to use for the ``quantity`` arg, when generating parameters.

    The different calls use different names for ``quantity`` parameter,
    so this must be defined in subclasses.
    """

    def __init__(
        self,
        sku: str,
        quantity: int,
        quantity_in_case: Optional[int] = None,
        prep_details_list: Optional[List[PrepDetails]] = None,
    ):
        self.sku = sku
        self.quantity = quantity
        self.quantity_in_case = quantity_in_case
        self.prep_details_list = prep_details_list

    def _base_params_dict(self) -> dict:
        assert (
            self.quantity_param != ""
        ), f"{self.__class__.__name__}.quantity_param must be defined."
        data = {
            "SellerSKU": self.sku,
            self.quantity_param: self.quantity,
            "QuantityInCase": self.quantity_in_case,
        }
        # Each PrepDetails instance will parameterize itself,
        # but we need to enumerate it with "PrepDetailsList.member"
        if self.prep_details_list:
            parameterized_prep_details = [x.to_params() for x in self.prep_details_list]
            data.update(
                enumerate_keyed_param(
                    "PrepDetailsList.member", parameterized_prep_details
                )
            )
        return data


class InboundShipmentPlanRequestItem(BaseInboundShipmentItem):
    """Item information for creating an inbound shipment plan.
    Submitted with a call to the CreateInboundShipmentPlan operation.

    `MWS docs: InboundShipmentPlanRequestItem Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#InboundShipmentPlanRequestItem>`_

    Adds the optional arguments ``asin`` (to include ASIN as needed) and ``condition``
    (to add item condition information).

    ``condition`` may be a string or an instance of :py:class:`ItemCondition
    <mws.models.inbound_shipments.ItemCondition>`.
    """

    operations_permitted = ["CreateInboundShipmentPlan"]
    quantity_param = "Quantity"

    def __init__(
        self,
        *args,
        asin: Optional[str] = None,
        condition: Optional[Union[ItemCondition, str]] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.asin = asin
        self.condition = condition

    def params_dict(self) -> dict:
        data = self._base_params_dict()
        data.update(
            {
                "ASIN": self.asin,
                "Condition": self.condition,
            }
        )
        return data


class InboundShipmentItem(BaseInboundShipmentItem):
    """Item information for an inbound shipment.
    Submitted with a call to the CreateInboundShipment or
    UpdateInboundShipment operation.

    `MWS docs: InboundShipmentItem Datatype
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#InboundShipmentItem>`_
    """

    operations_permitted = ["CreateInboundShipment", "UpdateInboundShipment"]
    quantity_param = "QuantityShipped"

    def __init__(
        self,
        *args,
        release_date: Optional[datetime.datetime] = None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.release_date = release_date
        self.fnsku = None

    def params_dict(self) -> dict:
        data = self._base_params_dict()
        data.update({"ReleaseDate": self.release_date})
        return data

    @classmethod
    def from_plan_item(
        cls,
        item: DotDict,
        quantity_in_case: Optional[int] = None,
        release_date: Optional[datetime.datetime] = None,
    ) -> "InboundShipmentItem":
        """Construct this model from a shipment plan returned from a
        CreateInboundShipmentPlan request.

        Expects a ``DotDict`` instance that can typically be found in the parsed
        response object by:

        1. Iterating ``for plan in resp.parsed.InboundShipmentPlans.member:``; and
        2. Iterating ``for item in plan.Items.member:``.

        Each ``item`` instance in the above example *should* work here [YMMV].

        ``quantity_in_case`` must be passed manually for case-packed shipments,
        even when constructing from a shipment plan response, as this data is not
        typically returned in the plan details.

        ``release_date`` is also not part of a shipment plan response, so this
        must be passed manually in order to add it to the item.
        """
        # Parse prep details from the plan object, if any exist.
        prep_details_list = []
        if "PrepDetailsList" in item:
            for prep_details in item.PrepDetailsList.PrepDetails:
                prep_details_list.append(
                    PrepDetails(
                        prep_instruction=prep_details.PrepInstruction,
                        prep_owner=prep_details.PrepOwner,
                    )
                )
        # Construct the item model instance
        instance = cls(
            sku=item.SellerSKU,
            quantity=item.Quantity,
            quantity_in_case=quantity_in_case,
            prep_details_list=prep_details_list,
            release_date=release_date,
        )
        # Add an FNSKU manually to this instance, if present in the plan data.
        instance.fnsku = item.get("FulfillmentNetworkSKU")

        return instance


class ExtraItemData:
    """Dataclass used for providing overrides to individual SKUs when
    processing items from a planned shipment in bulk using
    :py:func:`shipment_items_from_plan`.

    To utilize, construct a dictionary that maps SellerSKUs to instances of this class,
    then pass that dictionary to the ``overrides`` argument for
    ``shipment_items_from_plan``.
    """

    def __init__(
        self,
        quantity_in_case: Optional[int] = None,
        release_date: Optional[datetime.datetime] = None,
    ):
        self.quantity_in_case = quantity_in_case
        self.release_date = release_date

    def to_dict(self) -> dict:
        output = {
            "quantity_in_case": self.quantity_in_case,
            "release_date": self.release_date,
        }
        return {k: v for k, v in output.items() if v is not None}


def shipment_items_from_plan(
    plan: Union[DotDict, List[DotDict]],
    overrides: Optional[Dict[str, ExtraItemData]] = None,
) -> List[InboundShipmentItem]:
    """Given a shipment plan response, returns a list of InboundShipmentItem models
    constructed from the contents of that plan's ``Items`` set.

    Expects ``plan`` to be a node from a parsed MWS response from the
    ``create_inbound_shipment_plan`` request, typically the
    ``resp.parsed.InboundShipmentPlans.member`` node (which may be a DotDict for a
    single plan or a list of DotDicts for multiple; though both options should be
    natively iterable with the same interface).

    Providing ``overrides`` allows the addition of details that are not returned by
    ``create_inbound_shipment_plan``, such as ``quantity_in_case`` and ``release_date``.
    Expects a dict where SellerSKUs are keys and the values are either instances of
    ``ExtraItemData`` or dictionaries with the keys ``quantity_in_case`` and/or
    ``release_date``. Only items matching a SellerSKU key in ``overrides`` will have
    data overridden this way.
    """
    overrides = overrides or {}

    if "member" in plan:
        # User has likely passed node ``InboundShipmentPlans``, but we need the child
        # node, ``member``. Move down to this node automatically.
        plan = plan.member
    if "Items" not in plan:
        raise ValueError(
            (
                "'Items' node not found in plan. "
                "Requires a parsed response from the CreateInboundShipmentPlan request "
                "using the correct node in that response "
                "(typically `resp.parsed.InboundShipmentPlans.member`) "
            )
        )
    shipment_items = []
    for item in plan.Items.member:
        # Gather override data from our overrides, if present
        override_data = overrides.get(item.SellerSKU, {})
        if isinstance(override_data, ExtraItemData):
            # Convert from the ExtraItemData dataclass to a dict representation
            override_data = override_data.to_dict()

        # Narrow down override data to just the proper keys
        override_data = {
            k: v
            for k, v in override_data.items()
            if k in ("quantity_in_case", "release_date")
        }
        shipment_items.append(InboundShipmentItem.from_plan_item(item, **override_data))
    return shipment_items
