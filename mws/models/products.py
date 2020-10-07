from typing import Optional


class ListingPrice:
    def __init__(self, currency_code: str, amount: float):
        self.currency_code = currency_code
        self.amount = amount


class ShippingPrice:
    def __init__(self, currency_code: str, amount: float):
        self.currency_code = currency_code
        self.amount = amount


class Points:
    def __init__(self, points_number: int):
        self.points_number = points_number


class PriceToEstimateFees:
    def __init__(
        self,
        listing_price: ListingPrice,
        shipping_price: ShippingPrice,
        points: Optional[Points] = None,
    ):
        self.listing_price = listing_price
        self.shipping_price = shipping_price
        self.points = points


class FeesEstimateRequestItem:
    def __init__(
        self,
        marketplace_id: str,
        id_type: str,
        id_value: str,
        is_amazon_fulfilled: bool,
        identifier: str,
        price_to_estimate_fees: PriceToEstimateFees,
    ):
        self.marketplace_id = marketplace_id
        self.id_type = id_type
        self.id_value = id_value
        self.is_amazon_fulfilled = is_amazon_fulfilled
        self.identifier = identifier
        self.price_to_estimate_fees = price_to_estimate_fees

    def serialize(self):
        data = {
            "MarketplaceId": self.marketplace_id,
            "IdType": self.id_type,
            "IdValue": self.id_value,
            "IsAmazonFulfilled": self.is_amazon_fulfilled,
            "Identifier": self.identifier,
            "PriceToEstimateFees.ListingPrice.CurrencyCode": self.price_to_estimate_fees.listing_price.currency_code,
            "PriceToEstimateFees.ListingPrice.Amount": self.price_to_estimate_fees.listing_price.amount,
            "PriceToEstimateFees.Shipping.CurrencyCode": self.price_to_estimate_fees.shipping_price.currency_code,
            "PriceToEstimateFees.Shipping.Amount": self.price_to_estimate_fees.shipping_price.amount,
        }
        if self.price_to_estimate_fees.points is not None:
            data[
                "PriceToEstimateFees.Points.PointsNumber"
            ] = self.price_to_estimate_fees.points.points_number
        return data
