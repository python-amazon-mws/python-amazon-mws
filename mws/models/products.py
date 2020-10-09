"""Datatype models for Products API."""

from typing import Optional

from mws.utils import flat_param_dict

from .base import MWSDataType


class MoneyType(MWSDataType):
    def __init__(self, amount: float, currency_code: str):
        self.amount = amount
        self.currency_code = currency_code

    def to_dict(self) -> dict:
        return {
            "Amount": self.amount,
            "CurrencyCode": self.currency_code,
        }


class Points(MWSDataType):
    def __init__(self, points_number: int, monetary_value: MoneyType):
        self.points_number = points_number
        assert isinstance(
            monetary_value, MoneyType
        ), "monetary_value must be a MoneyType model instance."
        self.monetary_value = monetary_value

    def to_dict(self) -> dict:
        data = {"PointsNumber": self.points_number}
        data.update(
            flat_param_dict(self.monetary_value.to_dict(), prefix="PointsMonetaryValue")
        )
        return data


class PriceToEstimateFees(MWSDataType):
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

    def to_dict(self) -> dict:
        data = {}
        data.update(
            flat_param_dict(self.listing_price.to_dict(), prefix="ListingPrice")
        )
        data.update(flat_param_dict(self.shipping.to_dict(), prefix="Shipping"))
        if self.points is not None:
            data.update(flat_param_dict(self.points.to_dict(), prefix="Points"))
        return data


class FeesEstimateRequest(MWSDataType):
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

    def to_dict(self) -> dict:
        data = {
            "MarketplaceId": self.marketplace_id,
            "IdType": self.id_type,
            "IdValue": self.id_value,
            "Identifier": self.identifier,
            "IsAmazonFulfilled": self.is_amazon_fulfilled,
        }
        data.update(
            flat_param_dict(
                self.price_to_estimate_fees.to_dict(), prefix="PriceToEstimateFees"
            )
        )
        return data
