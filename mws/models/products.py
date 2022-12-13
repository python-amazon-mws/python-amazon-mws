"""Datatype models for Products API."""

from enum import Enum
from typing import Union

from mws.utils.types import MarketplaceEnumOrStr

from .base import MWSDataType

# NOTE: objects listed in __all__ will be attached to the Products API by the same name.
# Maintain this list, please!
__all__ = [
    "CurrencyCode",
    "MoneyType",
    "Points",
    "PriceToEstimateFees",
    "FeesEstimateRequest",
]


class CurrencyCode(str, Enum):
    """Constants for currency codes supported by Amazon."""

    USD = "USD"
    """United States dollar"""

    EUR = "EUR"
    """European euro"""

    GBP = "GBP"
    """Great Britain pounds"""

    RMB = "RMB"
    """Chinese yuan"""

    INR = "INR"
    """Indian rupee"""

    JPY = "JPY"
    """Japanese yen"""

    CAD = "CAD"
    """Canadian dollar"""

    MXN = "MXN"
    """Mexican peso"""


class MoneyType(MWSDataType):
    """An amount of money in a specified currency.

    `MWS Docs: MoneyType
    <https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#MoneyType>`_
    """

    def __init__(self, amount: float, currency_code: Union[CurrencyCode, str]):
        self.amount = amount
        self.currency_code = currency_code

    def params_dict(self) -> dict:
        return {
            "Amount": self.amount,
            "CurrencyCode": self.currency_code,
        }


class Points(MWSDataType):
    """The number of Amazon Points offered with the purchase of an item.
    The Amazon Points program is only available in Japan.

    `MWS Docs: Points
    <https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#Points>`_
    """

    def __init__(self, points_number: int, monetary_value: MoneyType):
        self.points_number = points_number
        if not isinstance(monetary_value, MoneyType):
            raise ValueError("monetary_value must be a MoneyType model instance.")
        self.monetary_value = monetary_value

    def params_dict(self) -> dict:
        data = {"PointsNumber": self.points_number}
        data.update(self.monetary_value.to_params(prefix="PointsMonetaryValue"))
        return data


class PriceToEstimateFees(MWSDataType):
    """Price information for a product, used to estimate fees.

    `MWS Docs: PriceToEstimateFees
    <https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#PriceToEstimateFees>`_
    """

    def __init__(
        self,
        listing_price: MoneyType,
        shipping: MoneyType,
        points: Points = None,
    ):
        if not isinstance(listing_price, MoneyType):
            raise ValueError("listing_price must be a MoneyType model instance.")
        if not isinstance(shipping, MoneyType):
            raise ValueError("shipping must be a MoneyType model instance.")
        self.listing_price = listing_price
        self.shipping = shipping
        if points is not None:
            if not isinstance(points, Points):
                raise ValueError("points must be a Points model instance.")
        self.points = points

    def params_dict(self) -> dict:
        data = {}
        data.update(self.listing_price.to_params(prefix="ListingPrice"))
        data.update(self.shipping.to_params(prefix="Shipping"))
        if self.points is not None:
            data.update(self.points.to_params(prefix="Points"))
        return data


class FeesEstimateRequest(MWSDataType):
    """A product, marketplace, and proposed price used to request estimated fees.

    `MWS Docs: FeesEstimateRequest
    <https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#FeesEstimateRequest>`_
    """

    def __init__(
        self,
        marketplace_id: MarketplaceEnumOrStr,
        id_type: str,
        id_value: str,
        price_to_estimate_fees: PriceToEstimateFees,
        is_amazon_fulfilled: bool,
        identifier: str,
    ):
        self.marketplace_id = marketplace_id
        self.id_type = id_type
        self.id_value = id_value
        self.identifier = identifier
        self.is_amazon_fulfilled = is_amazon_fulfilled
        if not isinstance(price_to_estimate_fees, PriceToEstimateFees):
            raise ValueError(
                "price_to_estimate_fees must be a PriceToEstimateFees model instance"
            )
        self.price_to_estimate_fees = price_to_estimate_fees

    def params_dict(self) -> dict:
        data = {
            "MarketplaceId": self.marketplace_id,
            "IdType": self.id_type,
            "IdValue": self.id_value,
            "Identifier": self.identifier,
            "IsAmazonFulfilled": self.is_amazon_fulfilled,
        }
        data.update(self.price_to_estimate_fees.to_params(prefix="PriceToEstimateFees"))
        return data
