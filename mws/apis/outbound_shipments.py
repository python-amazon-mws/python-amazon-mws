"""
Amazon MWS Fulfillment Outbound Shipments API
"""
from __future__ import absolute_import
# import warnings

from ..mws import MWS
# from .. import utils


class OutboundShipments(MWS):
    """
    Amazon MWS Fulfillment Outbound Shipments API
    """
    URI = "/FulfillmentOutboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NEXT_TOKEN_OPERATIONS = [
        'ListAllFulfillmentOrders',
    ]
    # TODO: Complete this class section
