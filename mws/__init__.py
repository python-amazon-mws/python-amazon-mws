# -*- coding: utf-8 -*-
import warnings

# This import must go first!
# API modules also import MWS, so it must be available before attempting
# those .api imports later
from mws.mws import MWS, Marketplaces

from .apis import (
    EasyShip,
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
)
from .errors import MWSError
from .response import MWSResponse
from .utils import DotDict, types

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
    "types",
    "DotDict",
]

warnings.simplefilter("default")
