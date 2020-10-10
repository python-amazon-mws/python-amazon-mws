"""DataType models for InboundShipments API."""

from typing import Optional, Union
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
