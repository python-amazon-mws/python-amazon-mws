"""Amazon MWS FulfillmentInboundShipment API."""

# collections.abc.Iterable clashes with typing.Iterable,
# so we rename both to avoid confusion in code
from collections.abc import Iterable as IterableAbc
from typing import Iterable as IterableType

from collections.abc import Mapping
from typing import Dict, List, Optional, Union
import datetime

from mws import MWS, MWSError
from mws.models.inbound_shipments import Address
from mws.utils.params import enumerate_param
from mws.utils.params import flat_param_dict
from mws.utils.params import enumerate_keyed_param
from mws.utils.collections import unique_list_order_preserved
from mws.decorators import next_token_action

# TODO Add label type enumeration
# TODO Add helper method for extracting PDF file object from label requests


# TODO replace with datatype class pattern
def parse_item_args(item_args: List[Dict], operation: str) -> List[dict]:
    """Parses item arguments sent to ``create_inbound_shipment_plan``,
    ``create_inbound_shipment``, and ``update_inbound_shipment`` methods.

    :param item_args: A list of dicts containing data for items to be parsed.
        Each dict must contain the keys ``'sku'`` and ``'quantity'``.
        Optionally, ``'quantity_in_case'`` can be included for case-packed items.

        For operations besides ``create_inbound_shipment``,
        ``'asin'`` and ``'condition'`` are also supported as optional keys.

        If any required key is missing, ``MWSError`` is thrown.
        Any keys besides the required or optional keys for a given operation
        will be discarded.

        These input keys are mapped to the appropriate parameter name for the chosen
        operation. For instance, ``'quantity'`` is converted to ``'Quantity'``
        for the ``CreateInboundShipmentPlan`` operation, and to ``'QuantityShipped'``
        for all other operations.
    :type item_args: List[Dict]
    :param operation: The name of the MWS operation being performed, changing how
        ``item_args`` are converted to MWS parameters.

        Specifically checks to see if the operation is ``"CreateInboundShipmentPlan"``,
        which is a special case: different logic applies for all other
        relevant operations.
    :type operation: str
    """
    if not item_args:
        raise MWSError("One or more `item` dict arguments required.")

    if operation == "CreateInboundShipmentPlan":
        # `key_config` composed of list of tuples, each tuple compose of:
        # (input_key, output_key, is_required, default_value)
        key_config = [
            ("sku", "SellerSKU", True, None),
            ("quantity", "Quantity", True, None),
            ("quantity_in_case", "QuantityInCase", False, None),
            ("asin", "ASIN", False, None),
            ("condition", "Condition", False, None),
        ]
        # The expected MWS key for quantity is different for this operation.
        # This ensures we use the right key later on.
        quantity_key = "Quantity"
    else:
        key_config = [
            ("sku", "SellerSKU", True, None),
            ("quantity", "QuantityShipped", True, None),
            ("quantity_in_case", "QuantityInCase", False, None),
        ]
        quantity_key = "QuantityShipped"

    items = []
    for item in item_args:
        if not isinstance(item, Mapping):
            raise MWSError("`item` argument must be a dict.")
        if not all(k in item for k in [c[0] for c in key_config if c[2]]):
            # Required keys of an item line missing
            raise MWSError(
                (
                    "`item` dict missing required keys: {required}."
                    "\n- Optional keys: {optional}."
                ).format(
                    required=", ".join([c[0] for c in key_config if c[2]]),
                    optional=", ".join([c[0] for c in key_config if not c[2]]),
                )
            )

        item_dict = {
            "SellerSKU": item.get("sku"),
            quantity_key: item.get("quantity"),
            "QuantityInCase": item.get("quantity_in_case"),
        }
        item_dict.update(
            {
                c[1]: item.get(c[0], c[3])
                for c in key_config
                if c[0] not in ["sku", "quantity", "quantity_in_case"]
            }
        )
        items.append(item_dict)

    return items


class InboundShipments(MWS):
    """Amazon MWS FulfillmentInboundShipment API

    Docs:
    http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html
    """

    URI = "/FulfillmentInboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/}"
    NEXT_TOKEN_OPERATIONS = [
        "ListInboundShipments",
        "ListInboundShipmentItems",
    ]

    def __init__(self, *args, **kwargs):
        """Allow the addition of a from_address dict during object initialization.
        kwarg "from_address" is caught and popped here,
        then calls set_ship_from_address.
        If empty or left out, empty dict is set by default.
        """
        self._from_address = {}
        addr = kwargs.pop("from_address", None)
        if addr is not None:
            self.from_address = addr
        super(InboundShipments, self).__init__(*args, **kwargs)

    @property
    def from_address(self):
        if self._from_address is None:
            return None
        return self._from_address

    @from_address.setter
    def from_address(self, value: Union[Address, dict]):
        """Verifies the structure of an address dictionary.
        Once verified against the KEY_CONFIG, saves a parsed version
        of that dictionary, ready to send to requests.
        """
        if value is None:
            self._from_address = None
            return
        if isinstance(value, Address):
            # Shortcut by using the Address model's to_dict method.
            self._from_address = value
            return
        if not isinstance(value, Mapping):
            raise MWSError("value must be a dict or other Mapping type")

        self._from_address = Address.from_legacy_dict(value)

    def set_ship_from_address(self, address: Union[Address, dict]):
        self.from_address = address

    def from_address_dict(self, prefix: str = "") -> dict:
        """Flattens the from_address object to a dict with prefix before each key.

        Additionally, checks that ``from_address`` was set properly,
        raising MWSError if it is not.
        """
        if not self.from_address:
            raise MWSError("'from_address' must be set before calling this operation.")
        return self.from_address.to_params(prefix=prefix)

    ### REQUEST METHODS ###
    def get_inbound_guidance_for_sku(self, skus: IterableType, marketplace_id: str):
        """Returns inbound guidance for a list of items by Seller SKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForSKU.html
        """
        if not isinstance(skus, IterableAbc):
            skus = [skus]

        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("SellerSKUList.Id", skus))
        return self.make_request("GetInboundGuidanceForSKU", data)

    def get_inbound_guidance_for_asin(self, asins: IterableType, marketplace_id: str):
        """Returns inbound guidance for a list of items by ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForASIN.html
        """
        if not isinstance(asins, IterableAbc):
            asins = [asins]

        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.Id", asins))
        return self.make_request("GetInboundGuidanceForASIN", data)

    def create_inbound_shipment_plan(
        self,
        items: IterableType[dict],
        country_code: str = "US",
        subdivision_code: str = "",
        label_preference: str = "",
        from_address: Optional[Address] = None,
    ):
        """Returns one or more inbound shipment plans, which provide the
        information you need to create inbound shipments.

        At least one dictionary must be passed as `args`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'asin', 'condition', 'quantity_in_case'

        ``InboundShipments.from_address`` must be set before using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipmentPlan.html
        """
        if not items:
            raise MWSError("One or more `item` dict arguments required.")
        subdivision_code = subdivision_code or None
        label_preference = label_preference or None

        data = {
            "ShipToCountryCode": country_code,
            "ShipToCountrySubdivisionCode": subdivision_code,
            "LabelPrepPreference": label_preference,
        }

        # Ship-from address handling
        from_addr_prefix = "ShipFromAddress"
        # The method `from_address_dict` matches signature with that of
        # `Address.to_params`, so we'll conditionally assign the function.
        func = self.from_address_dict
        if from_address:
            if not isinstance(from_address, Address):
                raise MWSError(
                    "from_address argument must be an instance of Address datatype model."
                )
            func = from_address.to_params
        from_address = func(prefix=from_addr_prefix)

        data.update(from_address)
        data.update(
            enumerate_keyed_param(
                "InboundShipmentPlanRequestItems.member",
                parse_item_args(items, "CreateInboundShipmentPlan"),
            )
        )
        return self.make_request("CreateInboundShipmentPlan", data, method="POST")

    def create_inbound_shipment(
        self,
        shipment_id: str,
        shipment_name: str,
        destination: str,
        items: IterableType[dict],
        shipment_status: str = "",
        label_preference: str = "",
        case_required: bool = False,
        box_contents_source: Optional[str] = None,
        from_address: Optional[Address] = None,
    ):
        """Creates an inbound shipment to Amazon's fulfillment network.

        At least one dictionary must be passed as `items`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'quantity_in_case'

        ``InboundShipments.from_address`` must be set before using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipment.html
        """
        if not items:
            raise MWSError("One or more `item` dict arguments required.")

        data = {
            "ShipmentId": shipment_id,
            "InboundShipmentHeader.ShipmentName": shipment_name,
            "InboundShipmentHeader.DestinationFulfillmentCenterId": destination,
            "InboundShipmentHeader.LabelPrepPreference": label_preference,
            "InboundShipmentHeader.AreCasesRequired": case_required,
            "InboundShipmentHeader.ShipmentStatus": shipment_status,
            "InboundShipmentHeader.IntendedBoxContentsSource": box_contents_source,
        }

        # Ship-from address handling
        from_addr_prefix = "InboundShipmentHeader.ShipFromAddress"
        func = self.from_address_dict
        if from_address:
            if not isinstance(from_address, Address):
                raise MWSError(
                    "from_address argument must be an instance of Address datatype model."
                )
            func = from_address.to_params
        from_address = func(prefix=from_addr_prefix)
        data.update(from_address)

        data.update(
            enumerate_keyed_param(
                "InboundShipmentItems.member",
                parse_item_args(items, "CreateInboundShipment"),
            )
        )
        return self.make_request("CreateInboundShipment", data, method="POST")

    def update_inbound_shipment(
        self,
        shipment_id: str,
        shipment_name: str,
        destination: str,
        items: Optional[IterableType[dict]] = None,
        shipment_status: str = "",
        label_preference: str = "",
        case_required: Optional[bool] = False,
        box_contents_source: Optional[str] = None,
        from_address: Optional[Address] = None,
    ):
        """Updates an existing inbound shipment in Amazon FBA.

        ``InboundShipments.from_address`` must be set before using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_UpdateInboundShipment.html
        """
        # Assert these are strings, error out if not.
        data = {
            "ShipmentId": shipment_id,
            "InboundShipmentHeader.ShipmentName": shipment_name,
            "InboundShipmentHeader.DestinationFulfillmentCenterId": destination,
            "InboundShipmentHeader.LabelPrepPreference": label_preference,
            "InboundShipmentHeader.AreCasesRequired": case_required,
            "InboundShipmentHeader.ShipmentStatus": shipment_status,
            "InboundShipmentHeader.IntendedBoxContentsSource": box_contents_source,
        }

        # Ship-from address handling
        from_addr_prefix = "InboundShipmentHeader.ShipFromAddress"
        func = self.from_address_dict
        if from_address:
            if not isinstance(from_address, Address):
                raise MWSError(
                    "from_address argument must be an instance of Address datatype model."
                )
            func = from_address.to_params
        from_address = func(prefix=from_addr_prefix)
        data.update(from_address)

        if items:
            # Update with an items paramater only if they exist.
            data.update(
                enumerate_keyed_param(
                    "InboundShipmentItems.member",
                    parse_item_args(items, "UpdateInboundShipment"),
                )
            )
        return self.make_request("UpdateInboundShipment", data, method="POST")

    def get_preorder_info(self, shipment_id: str):
        """Returns pre-order information, including dates, that a seller needs
        before confirming a shipment for pre-order. Also indicates if a shipment has
        already been confirmed for pre-order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPreorderInfo.html
        """
        return self.make_request("GetPreorderInfo", {"ShipmentId": shipment_id})

    def confirm_preorder(self, shipment_id: str, need_by_date: datetime.datetime):
        """Confirms a shipment for pre-order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmPreorder.html
        """
        return self.make_request(
            "ConfirmPreorder", {"ShipmentId": shipment_id, "NeedByDate": need_by_date}
        )

    def get_prep_instructions_for_sku(
        self, skus: IterableType = None, country_code: str = None
    ):
        """Returns labeling requirements and item preparation instructions
        to help you prepare items for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForSKU.html
        """
        country_code = country_code or "US"
        skus = skus or []

        # 'skus' should be a unique list, or there may be an error returned.
        skus = unique_list_order_preserved(skus)

        data = {"ShipToCountryCode": country_code}
        data.update(enumerate_param("SellerSKUList.ID.", skus))
        return self.make_request("GetPrepInstructionsForSKU", data, method="POST")

    def get_prep_instructions_for_asin(
        self, asins: IterableType = None, country_code: str = None
    ):
        """Returns item preparation instructions to help with item sourcing decisions.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForASIN.html
        """
        country_code = country_code or "US"
        asins = asins or []

        # 'asins' should be a unique list, or there may be an error returned.
        asins = unique_list_order_preserved(asins)

        data = {"ShipToCountryCode": country_code}
        data.update(enumerate_param("ASINList.ID.", asins))
        return self.make_request("GetPrepInstructionsForASIN", data, method="POST")

    # # TODO this method is incomplete: it should be able to account for all TransportDetailInput types
    # def put_transport_content(self, shipment_id, is_partnered, shipment_type, carrier_name, tracking_id):
    #     """
    #     Sends transportation information to Amazon about an inbound shipment.

    #     Docs:
    #     http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#TransportDetailInput
    #     """
    #     data = {
    #         'ShipmentId': shipment_id,
    #         'IsPartnered': is_partnered,
    #         'ShipmentType': shipment_type,
    #     }
    #     data['TransportDetails.NonPartneredSmallParcelData.CarrierName'] = carrier_name
    #     if isinstance(tracking_id, IterableAbc):
    #         count = 0
    #         for track in tracking_id:
    #             data[
    #                 'TransportDetails.NonPartneredSmallParcelData.PackageList.member.{}.TrackingId'.format(count + 1)
    #             ] = track
    #     return self.make_request("PutTransportContent", data)

    def estimate_transport_request(self, shipment_id: str):
        """Requests an estimate of the shipping cost for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_EstimateTransportRequest.html
        """
        return self.make_request(
            "EstimateTransportRequest", {"ShipmentId": shipment_id}, method="POST"
        )

    def get_transport_content(self, shipment_id: str):
        """Returns current transportation information about an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetTransportContent.html
        """
        return self.make_request(
            "GetTransportContent", {"ShipmentId": shipment_id}, method="POST"
        )

    def confirm_transport_request(self, shipment_id: str):
        """Confirms that you accept the Amazon-partnered shipping estimate and
        you request that the Amazon-partnered carrier ship your inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmTransportRequest.html
        """
        return self.make_request("ConfirmTransportRequest", {"ShipmentId": shipment_id})

    def void_transport_request(self, shipment_id: str):
        """Voids a previously-confirmed request to ship your inbound shipment
        using an Amazon-partnered carrier.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_VoidTransportRequest.html
        """
        return self.make_request(
            "VoidTransportRequest", {"ShipmentId": shipment_id}, method="POST"
        )

    def get_package_labels(
        self, shipment_id: str, num_labels: int, page_type: Optional[str] = None
    ):
        """Returns PDF document data for printing package labels for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPackageLabels.html
        """
        return self.make_request(
            "GetPackageLabels",
            {
                "ShipmentId": shipment_id,
                "PageType": page_type,
                "NumberOfPackages": num_labels,
            },
            method="POST",
        )

    def get_unique_package_labels(
        self, shipment_id: str, page_type: str, package_ids: IterableType
    ):
        """Returns unique package labels for faster and more accurate shipment
        processing at the Amazon fulfillment center.

        `shipment_id` must match a valid, current shipment.

        `page_type` expected to be string matching one of following
        (not checked, in case Amazon requirements change):

        - "PackageLabel_Letter_2"
        - "PackageLabel_Letter_6"
        - "PackageLabel_A4_2"
        - "PackageLabel_A4_4"
        - "PackageLabel_Plain_Paper"

        `package_ids` a single package identifier, or a list/tuple/set of identifiers,
        specifying for which package(s) you want package labels printed.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetUniquePackageLabels.html
        """
        data = {
            "ShipmentId": shipment_id,
            "PageType": page_type,
        }
        if not isinstance(package_ids, IterableAbc):
            package_ids = [package_ids]
        data.update(enumerate_param("PackageLabelsToPrint.member.", package_ids))
        return self.make_request("GetUniquePackageLabels", data)

    def get_pallet_labels(self, shipment_id: str, page_type: str, num_labels: int):
        """Returns pallet labels.

        `shipment_id` must match a valid, current shipment.

        `page_type` expected to be string matching one of following
        (not checked, in case Amazon requirements change):

        - "PackageLabel_Letter_2"
        - "PackageLabel_Letter_6"
        - "PackageLabel_A4_2"
        - "PackageLabel_A4_4"
        - "PackageLabel_Plain_Paper"

        `num_labels` is integer, number of labels to create.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPalletLabels.html
        """
        data = {
            "ShipmentId": shipment_id,
            "PageType": page_type,
            "NumberOfPallets": num_labels,
        }
        return self.make_request("GetPalletLabels", data)

    def get_bill_of_lading(self, shipment_id: str):
        """Returns PDF document data for printing a bill of lading for an
        inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetBillOfLading.html
        """
        return self.make_request(
            "GetBillOfLading", {"ShipmentId": shipment_id}, method="POST"
        )

    @next_token_action("ListInboundShipments")
    def list_inbound_shipments(
        self,
        shipment_ids: Optional[IterableType[str]] = None,
        shipment_statuses: Optional[IterableType[str]] = None,
        last_updated_after: Optional[datetime.datetime] = None,
        last_updated_before: Optional[datetime.datetime] = None,
        next_token: str = None,
    ):
        """Returns list of shipments based on statuses, IDs, and/or before/after datetimes.

        Pass `next_token` to call "ListInboundShipmentsByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipments.html
        """
        data = {
            "LastUpdatedAfter": last_updated_after,
            "LastUpdatedBefore": last_updated_before,
        }
        data.update(enumerate_param("ShipmentStatusList.member.", shipment_statuses))
        data.update(enumerate_param("ShipmentIdList.member.", shipment_ids))
        return self.make_request("ListInboundShipments", data, method="POST")

    def list_inbound_shipments_by_next_token(self, token: str):
        """Alias for `list_inbound_shipments(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentsByNextToken.html
        """
        return self.list_inbound_shipments(next_token=token)

    @next_token_action("ListInboundShipmentItems")
    def list_inbound_shipment_items(
        self,
        shipment_id: Optional[str] = None,
        last_updated_after: Optional[datetime.datetime] = None,
        last_updated_before: Optional[datetime.datetime] = None,
        next_token: Optional[str] = None,
    ):
        """Returns list of items within inbound shipments and/or before/after datetimes.

        Pass `next_token` to call "ListInboundShipmentItemsByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItems.html
        """
        return self.make_request(
            "ListInboundShipmentItems",
            {
                "ShipmentId": shipment_id,
                "LastUpdatedAfter": last_updated_after,
                "LastUpdatedBefore": last_updated_before,
            },
            method="POST",
        )

    def list_inbound_shipment_items_by_next_token(self, token: str):
        """Alias for `list_inbound_shipment_items(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItemsByNextToken.html
        """
        return self.list_inbound_shipment_items(next_token=token)
