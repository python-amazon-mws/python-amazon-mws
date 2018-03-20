# -*- coding: utf-8 -*-
from __future__ import absolute_import

from .mws import MWS, MWSError
from .apis import Feeds, Finances, InboundShipments, Inventory, MerchantFulfillment,\
                  OffAmazonPayments, Orders, OutboundShipments, Products, Recommendations,\
                  Reports, Sellers, Subscriptions
__all__ = [
    'Feeds',
    'Finances',
    'InboundShipments',
    'Inventory',
    'MerchantFulfillment',
    'MWS',
    'MWSError',
    'OffAmazonPayments',
    'Orders',
    'OutboundShipments',
    'Products',
    'Recommendations',
    'Reports',
    'Sellers',
    'Subscriptions',
]
