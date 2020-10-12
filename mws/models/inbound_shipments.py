"""DataType models for InboundShipments API."""

from mws.utils.params import enumerate_keyed_param, enumerate_param
from typing import List, Optional, Union
from enum import Enum

from .base import MWSDataType


class Address(MWSDataType):
    """Postal address information.

    https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#Address
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

    def __repr__(self):
        output = f"{self.__class__.__name__}"
        order = [
            "name",
            "address_line_1",
            "city",
            "address_line_2",
            "district_or_county",
            "state_or_province_code",
            "country_code",
            "postal_code",
        ]
        attrs = []
        for attr in order:
            val = getattr(self, attr)
            if val is not None:
                attrs.append(f"{attr}={repr(val)}")
        attr_str = ", ".join(attrs)
        output += f"({attr_str})"
        return output

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

    https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#PrepInstruction

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

    https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#PrepDetails

    :param prep_instructions: The instruction for this prep.
        Can accept a ``PrepInstruction`` enumeration, which will be converted to its
        string value when parameterized for a request.
    """

    OWNER_AMAZON = "AMAZON"
    OWNER_SELLER = "SELLER"

    def __init__(
        self,
        prep_instruction: Union[PrepInstruction, str],
        prep_owner: str = OWNER_SELLER,
    ):
        self.prep_instruction = prep_instruction
        self.prep_owner = prep_owner

    def params_dict(self) -> dict:
        return {
            "PrepInstruction": self.clean_enum_val(self.prep_instruction),
            "PrepOwner": self.prep_owner,
        }


class ItemCondition(Enum):
    """Condition value for an item included with a CreateInboundShipmentPlan request.

    Values can be found in MWS documentation for the ``Condition`` parameter of a
    ``InboundShipmentPlanRequestItem`` Datatype:
    https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#InboundShipmentPlanRequestItem
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


class InboundShipmentPlanRequestItem(MWSDataType):
    """An item to add to a Create Inbound Shipment Plan call [WIP]"""

    def __init__(
        self,
        sku: str,
        quantity: int,
        quantity_in_case: Optional[int] = None,
        asin: Optional[str] = None,
        condition: Optional[Union[ItemCondition, str]] = None,
        prep_details_list: Optional[List[PrepDetails]] = None,
    ):
        self.sku = sku
        self.quantity = quantity
        self.quantity_in_case = quantity_in_case
        self.asin = asin
        self.condition = condition
        self.prep_details_list = prep_details_list

    def params_dict(self) -> dict:
        data = {
            "SellerSKU": self.sku,
            "ASIN": self.asin,
            "Condition": self.clean_enum_val(self.condition),
            "Quantity": self.quantity,
            "QuantityInCase": self.quantity_in_case,
        }
        # Each PrepDetails instance will param itself,
        # but we need to enumerate it with "PrepDetailsList.member"
        if self.prep_details_list:
            data.update(
                enumerate_keyed_param("PrepDetailsList.member", self.prep_details_list)
            )
        return data
