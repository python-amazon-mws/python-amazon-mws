"""Datatype models for Products API."""

from typing import Optional

from .base import MWSDataType


class MoneyType(MWSDataType):
    """An amount of money in a specified currency.

    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#MoneyType
    """

    def __init__(self, amount: float, currency_code: str):
        self.amount = amount
        self.currency_code = currency_code

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.amount)}, "
            f"{repr(self.currency_code)}"
            ")"
        )

    def to_dict(self) -> dict:
        return {
            "Amount": self.amount,
            "CurrencyCode": self.currency_code,
        }


class Points(MWSDataType):
    """The number of Amazon Points offered with the purchase of an item.
    The Amazon Points program is only available in Japan.

    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#Points
    """

    def __init__(self, points_number: int, monetary_value: MoneyType):
        self.points_number = points_number
        assert isinstance(
            monetary_value, MoneyType
        ), "monetary_value must be a MoneyType model instance."
        self.monetary_value = monetary_value

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.points_number)}, "
            f"{repr(self.monetary_value)}"
            ")"
        )

    def to_dict(self) -> dict:
        data = {"PointsNumber": self.points_number}
        data.update(
            self._flatten(self.monetary_value.to_dict(), prefix="PointsMonetaryValue")
        )
        return data


class PriceToEstimateFees(MWSDataType):
    """Price information for a product, used to estimate fees.

    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#PriceToEstimateFees
    """

    def __init__(
        self,
        listing_price: MoneyType,
        shipping: MoneyType,
        points: Optional[Points] = None,
    ):
        assert isinstance(
            listing_price, MoneyType
        ), "listing_price must be a MoneyType model instance."
        assert isinstance(
            shipping, MoneyType
        ), "shipping must be a MoneyType model instance."
        self.listing_price = listing_price
        self.shipping = shipping
        if points is not None:
            assert isinstance(points, Points), "points must be a Points model instance."
        self.points = points

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.listing_price)}, "
            f"{repr(self.shipping)}, "
            f"points={repr(self.points)}"
            ")"
        )

    def to_dict(self) -> dict:
        data = {}
        data.update(self._flatten(self.listing_price.to_dict(), prefix="ListingPrice"))
        data.update(self._flatten(self.shipping.to_dict(), prefix="Shipping"))
        if self.points is not None:
            data.update(self._flatten(self.points.to_dict(), prefix="Points"))
        return data


class FeesEstimateRequest(MWSDataType):
    """A product, marketplace, and proposed price used to request estimated fees.

    https://docs.developer.amazonservices.com/en_US/products/Products_Datatypes.html#FeesEstimateRequest
    """

    def __init__(
        self,
        marketplace_id: str,
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
        assert isinstance(
            price_to_estimate_fees, PriceToEstimateFees
        ), "price_to_estimate_fees must be a PriceToEstimateFees model instance"
        self.price_to_estimate_fees = price_to_estimate_fees

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"{repr(self.marketplace_id)}, "
            f"{repr(self.id_type)}, "
            f"{repr(self.id_value)}, "
            f"{repr(self.price_to_estimate_fees)}, "
            f"{repr(self.is_amazon_fulfilled)}, "
            f"{repr(self.identifier)}"
            ")"
        )

    def to_dict(self) -> dict:
        data = {
            "MarketplaceId": self.marketplace_id,
            "IdType": self.id_type,
            "IdValue": self.id_value,
            "Identifier": self.identifier,
            "IsAmazonFulfilled": self.is_amazon_fulfilled,
        }
        data.update(
            self._flatten(
                self.price_to_estimate_fees.to_dict(), prefix="PriceToEstimateFees"
            )
        )
        return data
