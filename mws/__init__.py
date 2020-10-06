# -*- coding: utf-8 -*-
import warnings

from .mws import Marketplaces, MWS
from .errors import MWSError
from .apis import (
    Feeds,
    Finances,
    InboundShipments,
    Inventory,
    MerchantFulfillment,
    OffAmazonPayments,
    Orders,
    OutboundShipments,
    Products,
    Recommendations,
    Reports,
    Sellers,
    Subscriptions,
    EasyShip,
)
from .response import MWSResponse

__all__ = [
    "EasyShip",
    "Feeds",
    "Finances",
    "InboundShipments",
    "Inventory",
    "Marketplaces",
    "MerchantFulfillment",
    "MWS",
    "MWSError",
    "MWSResponse",
    "OffAmazonPayments",
    "Orders",
    "OutboundShipments",
    "Products",
    "Recommendations",
    "Reports",
    "Sellers",
    "Subscriptions",
]

warnings.simplefilter("default")
