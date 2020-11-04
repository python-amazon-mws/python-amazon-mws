"""Amazon MWS FulfillmentInboundShipment API."""

from typing import Iterable
import typing

from collections.abc import Mapping
from typing import Dict, List, Optional, Union
import datetime

from mws import MWS
from mws import MWSError
from mws.decorators import next_token_action
from mws.models.inbound_shipments import Address
from mws.models.inbound_shipments import InboundShipmentItem
from mws.models.inbound_shipments import InboundShipmentPlanRequestItem
from mws.utils.collections import unique_list_order_preserved
from mws.utils.deprecation import kwargs_renamed_for_v11
from mws.utils.params import enumerate_keyed_param
from mws.utils.params import enumerate_param

# TODO Add label type enumeration
# TODO Add helper method for extracting PDF file object from label requests

# TODO `Literal` not available pre-3.8.
#      This check and import are a slight hack as we continue to support 3.6+
#      When support drops for 3.7, remove these and replace with a more direct import
#      an real type annotation for objects that use it (removing type comments)
if typing.TYPE_CHECKING:  # pragma: no cover
    from typing import Literal


def parse_legacy_item(
    item: dict,
    operation,  # type: 'Literal["CreateInboundShipmentPlan", "CreateInboundShipment", "UpdateInboundShipment"]'
) -> dict:
    """Parses a legacy item dict sent to ``CreateInboundShipmentPlan``,
    ``CreateInboundShipment``, and ``UpdateInboundShipment`` operations.

    ``item`` must contain keys ``"sku"`` and ``"quantity"``; if either is missing,
    ``MWSError`` is raised. Optionally, ``"quantity_in_case"`` is accepted for
    case-packed items. For ``create_inbound_shipment_plan`` requests, also accepts
    optional keys for ``"asin"`` and ``"condition"``.

    Any keys besides the required or optional keys for the given operation
    will be ignored.

    ``operation`` expects the "Action" name of the operation being performed.
    Expects "CreateInboundShipmentPlan", "CreateInboundShipment", or
    "UpdateInboundShipment".
    """
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
    return item_dict


def parse_shipment_items(
    items: List[Union[InboundShipmentPlanRequestItem, InboundShipmentItem, dict]],
    operation=None,  # type: 'Optional[Literal["CreateInboundShipmentPlan", "CreateInboundShipment", "UpdateInboundShipment"]]'
) -> List[dict]:
    """Parses item arguments sent to ``create_inbound_shipment_plan`` request.

    Accepts instances of ``InboundShipmentPlanRequestItem`` and ``InboundShipmentItem``
    models, as well as dicts using "legacy" mode, which are then passed to
    ``parse_legacy_item``

    ```operation`` expects the "Action" name of the operation being performed.
    Expects "CreateInboundShipmentPlan", "CreateInboundShipment", or
    "UpdateInboundShipment".

    - When using legacy item dicts, this changes how the dict is prepared for output.
    - When using item models, checks that the operation matches using
      the model's ``raise_for_operation_mismatch`` method (passes silently when
      permitted or raises MWSError).
    """
    if not items:
        raise MWSError("One or more `item` arguments required.")

    item_params = []
    for item in items:
        if isinstance(item, (InboundShipmentPlanRequestItem, InboundShipmentItem)):
            item.raise_for_operation_mismatch(operation)
            item_params.append(item.to_params())
        else:
            item_params.append(parse_legacy_item(item, operation))
    return item_params


class InboundShipments(MWS):
    """Amazon MWS FulfillmentInboundShipment API

    `MWS docs: FulfillmentInboundShipment Overview
    <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html>`_
    """

    URI = "/FulfillmentInboundShipment/2010-10-01"
    VERSION = "2010-10-01"
    NAMESPACE = "{http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/}"
    NEXT_TOKEN_OPERATIONS = [
        "ListInboundShipments",
        "ListInboundShipmentItems",
    ]

    STATUS_WORKING = "WORKING"
    STATUS_SHIPPED = "SHIPPED"
    STATUS_CANCELLED = "CANCELLED"
    # Alias, for those who spell it with one L
    STATUS_CANCELED = "CANCELLED"

    def __init__(self, *args, **kwargs):
        """Allow the addition of a ``from_address`` kwarg, storing the address
        on this API instance.
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
        """Stores the ship-from address on this API instance.

        Accepts instances of ``Address`` model natively, while dict values
        are passed to ``Address.from_legacy_dict()`` for further processing.
        """
        if value is None:
            self._from_address = None
            return
        if isinstance(value, Address):
            # Shortcut by using the Address model's to_dict method.
            self._from_address = value
            return
        if not isinstance(value, Mapping):
            raise MWSError("value must be an instance of Address model or a dict")

        self._from_address = Address.from_legacy_dict(value)

    def set_ship_from_address(self, address: Union[Address, dict]):
        """DEPRECATED, remove later.
        Now an alias to assigning ``from_address`` property directly.
        """
        self.from_address = address

    def from_address_params(
        self, from_address: Address = None, prefix: str = ""
    ) -> dict:
        """Converts a from address, either stored or passed as an argument, to params.

        If provided as an argument, checks first that the arg is the correct type,
        raising MWSError if it's not an instance of the Address model.

        Providing a from_address as an argument will override any address stored
        on this API instance.
        """
        if from_address and not isinstance(from_address, Address):
            raise MWSError(
                "from_address must be an instance of Address datatype model."
            )
        from_address = from_address or self.from_address
        if not from_address:
            raise MWSError("from_address must be set before calling this operation.")
        return from_address.to_params(prefix=prefix)

    ### REQUEST METHODS ###
    def get_inbound_guidance_for_sku(self, skus: Iterable, marketplace_id: str):
        """Returns inbound guidance for a list of items by Seller SKU.

        ``skus`` expects a list, set or tuple. If it is any other type of object,
        it will be treated as a single instance, similar to passing ``[skus]``.

        `MWS docs: GetInboundGuidanceForSKU
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForSKU.html>`_
        """
        if not isinstance(skus, (list, set, tuple)):
            skus = [skus]

        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("SellerSKUList.Id", skus))
        return self.make_request("GetInboundGuidanceForSKU", data)

    def get_inbound_guidance_for_asin(self, asins: Iterable, marketplace_id: str):
        """Returns inbound guidance for a list of items by ASIN.

        ``asins`` expects a list, set or tuple. If it is any other type of object,
        it will be treated as a single instance, similar to passing ``[asins]``.

        `MWS docs: GetInboundGuidanceForASIN
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForASIN.html>`_
        """
        if not isinstance(asins, (list, set, tuple)):
            asins = [asins]

        data = {"MarketplaceId": marketplace_id}
        data.update(enumerate_param("ASINList.Id", asins))
        return self.make_request("GetInboundGuidanceForASIN", data)

    def create_inbound_shipment_plan(
        self,
        items: Iterable[Union[InboundShipmentPlanRequestItem, dict]],
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

        `MWS docs: CreateInboundShipmentPlan
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipmentPlan.html>`_
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
        data.update(self.from_address_params(from_address, "ShipFromAddress"))
        data.update(
            enumerate_keyed_param(
                "InboundShipmentPlanRequestItems.member",
                parse_shipment_items(items, "CreateInboundShipmentPlan"),
            )
        )
        return self.make_request("CreateInboundShipmentPlan", data, method="POST")

    def create_inbound_shipment(
        self,
        shipment_id: str,
        shipment_name: str,
        destination: str,
        items: Iterable[dict],
        shipment_status: str = STATUS_WORKING,
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

        `MWS docs: CreateInboundShipment
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipment.html>`_
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
        data.update(
            self.from_address_params(
                from_address=from_address,
                prefix="InboundShipmentHeader.ShipFromAddress",
            )
        )
        data.update(
            enumerate_keyed_param(
                "InboundShipmentItems.member",
                parse_shipment_items(items, "CreateInboundShipment"),
            )
        )
        return self.make_request("CreateInboundShipment", data, method="POST")

    def update_inbound_shipment(
        self,
        shipment_id: str,
        shipment_name: str,
        destination: str,
        items: Optional[Iterable[dict]] = None,
        shipment_status: str = "",
        label_preference: str = "",
        case_required: Optional[bool] = False,
        box_contents_source: Optional[str] = None,
        from_address: Optional[Address] = None,
    ):
        """Updates an existing inbound shipment in Amazon FBA.

        ``InboundShipments.from_address`` must be set before using this operation.

        `MWS docs: UpdateInboundShipment
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_UpdateInboundShipment.html>`_
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
        data.update(
            self.from_address_params(
                from_address, "InboundShipmentHeader.ShipFromAddress"
            )
        )
        if items:
            # Update with an items paramater only if they exist.
            data.update(
                enumerate_keyed_param(
                    "InboundShipmentItems.member",
                    parse_shipment_items(items, "UpdateInboundShipment"),
                )
            )
        return self.make_request("UpdateInboundShipment", data, method="POST")

    def get_preorder_info(self, shipment_id: str):
        """Returns pre-order information, including dates, that a seller needs
        before confirming a shipment for pre-order. Also indicates if a shipment has
        already been confirmed for pre-order.

        `MWS docs: GetPreorderInfo
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPreorderInfo.html>`_
        """
        return self.make_request("GetPreorderInfo", {"ShipmentId": shipment_id})

    def confirm_preorder(self, shipment_id: str, need_by_date: datetime.datetime):
        """Confirms a shipment for pre-order.

        `MWS docs: ConfirmPreorder
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmPreorder.html>`_
        """
        return self.make_request(
            "ConfirmPreorder", {"ShipmentId": shipment_id, "NeedByDate": need_by_date}
        )

    def get_prep_instructions_for_sku(
        self, skus: Iterable = None, country_code: str = None
    ):
        """Returns labeling requirements and item preparation instructions
        to help you prepare items for an inbound shipment.

        `MWS docs: GetPrepInstructionsForSKU
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForSKU.html>`_
        """
        country_code = country_code or "US"
        skus = skus or []

        # 'skus' should be a unique list, or there may be an error returned.
        skus = unique_list_order_preserved(skus)

        data = {"ShipToCountryCode": country_code}
        data.update(enumerate_param("SellerSKUList.ID.", skus))
        return self.make_request("GetPrepInstructionsForSKU", data, method="POST")

    def get_prep_instructions_for_asin(
        self, asins: Iterable = None, country_code: str = None
    ):
        """Returns item preparation instructions to help with item sourcing decisions.

        `MWS docs: GetPrepInstructionsForASIN
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForASIN.html>`_
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

    #     `MWS docs: PutTransportContent
    #     <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_PutTransportContent.html>`_
    #     """
    #     data = {
    #         'ShipmentId': shipment_id,
    #         'IsPartnered': is_partnered,
    #         'ShipmentType': shipment_type,
    #     }
    #     data['TransportDetails.NonPartneredSmallParcelData.CarrierName'] = carrier_name
    #     if isinstance(tracking_id, (list, set, tuple)):
    #         count = 0
    #         for track in tracking_id:
    #             data[
    #                 'TransportDetails.NonPartneredSmallParcelData.PackageList.member.{}.TrackingId'.format(count + 1)
    #             ] = track
    #     return self.make_request("PutTransportContent", data)

    def estimate_transport_request(self, shipment_id: str):
        """Requests an estimate of the shipping cost for an inbound shipment.

        `MWS docs: EstimateTransportRequest
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_EstimateTransportRequest.html>`_
        """
        return self.make_request(
            "EstimateTransportRequest", {"ShipmentId": shipment_id}, method="POST"
        )

    def get_transport_content(self, shipment_id: str):
        """Returns current transportation information about an inbound shipment.

        `MWS docs: GetTransportContent
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetTransportContent.html>`_
        """
        return self.make_request(
            "GetTransportContent", {"ShipmentId": shipment_id}, method="POST"
        )

    def confirm_transport_request(self, shipment_id: str):
        """Confirms that you accept the Amazon-partnered shipping estimate and
        you request that the Amazon-partnered carrier ship your inbound shipment.

        `MWS docs: ConfirmTransportRequest
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmTransportRequest.html>`_
        """
        return self.make_request("ConfirmTransportRequest", {"ShipmentId": shipment_id})

    def void_transport_request(self, shipment_id: str):
        """Voids a previously-confirmed request to ship your inbound shipment
        using an Amazon-partnered carrier.

        `MWS docs: VoidTransportRequest
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_VoidTransportRequest.html>`_
        """
        return self.make_request(
            "VoidTransportRequest", {"ShipmentId": shipment_id}, method="POST"
        )

    @kwargs_renamed_for_v11([("num_packages", "num_labels")])
    def get_package_labels(
        self, shipment_id: str, num_labels: int, page_type: Optional[str] = None
    ):
        """Returns PDF document data for printing package labels for an inbound shipment.

        `MWS docs: GetPackageLabels
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPackageLabels.html>`_
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
        self, shipment_id: str, page_type: str, package_ids: Iterable
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

        ``package_ids`` expects a list, set, or tuple of package identifiers,
        specifying for which packages you want package labels printed.
        If any other type of object is passed, it will be treated as a single instance,
        similar to passing ``[package_ids]``.

        `MWS docs: GetUniquePackageLabels
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetUniquePackageLabels.html>`_
        """
        data = {
            "ShipmentId": shipment_id,
            "PageType": page_type,
        }
        if not isinstance(package_ids, (list, set, tuple)):
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

        `MWS docs: GetPalletLabels
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPalletLabels.html>`_
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

        `MWS docs: GetBillOfLading
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetBillOfLading.html>`_
        """
        return self.make_request(
            "GetBillOfLading", {"ShipmentId": shipment_id}, method="POST"
        )

    @next_token_action("ListInboundShipments")
    def list_inbound_shipments(
        self,
        shipment_ids: Optional[Iterable[str]] = None,
        shipment_statuses: Optional[Iterable[str]] = None,
        last_updated_after: Optional[datetime.datetime] = None,
        last_updated_before: Optional[datetime.datetime] = None,
        next_token: str = None,
    ):
        """Returns list of shipments based on statuses, IDs, and/or before/after datetimes.

        Pass `next_token` to call "ListInboundShipmentsByNextToken" instead.

        `MWS docs: ListInboundShipments
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipments.html>`_
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

        `MWS docs: ListInboundShipmentsByNextToken
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentsByNextToken.html>`_
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

        `MWS docs: ListInboundShipmentItems
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItems.html>`_
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

        `MWS docs: ListInboundShipmentItemsByNextToken
        <https://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItemsByNextToken.html>`_
        """
        return self.list_inbound_shipment_items(next_token=token)
