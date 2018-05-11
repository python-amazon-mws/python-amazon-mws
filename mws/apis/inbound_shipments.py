"""
Amazon MWS FulfillmentInboundShipment API
"""
from __future__ import absolute_import

from ..mws import MWS, MWSError
from .. import utils
from ..decorators import next_token_action

# TODO Add label type enumeration
# TODO Add helper method for extracting PDF file object from label requests


def parse_item_args(item_args, operation):
    """
    Parses item arguments sent to create_inbound_shipment_plan, create_inbound_shipment,
    and update_inbound_shipment methods.

    `item_args` is expected as an iterable containing dicts.
    Each dict should have the following keys:
        For `create_inbound_shipment_plan`:
        REQUIRED: 'sku', 'quantity'
        OPTIONAL: 'quantity_in_case', 'asin', 'condition'
        Other operations:
        REQUIRED: 'sku', 'quantity'
        OPTIONAL: 'quantity_in_case'
    If a required key is missing, throws MWSError.
    All extra keys are ignored.

    Keys (above) are converted to the appropriate MWS key according to `key_config` (below)
    based on the particular operation required.
    """
    if not item_args:
        raise MWSError("One or more `item` dict arguments required.")

    if operation == 'CreateInboundShipmentPlan':
        # `key_config` composed of list of tuples, each tuple compose of:
        # (input_key, output_key, is_required, default_value)
        key_config = [
            ('sku', 'SellerSKU', True, None),
            ('quantity', 'Quantity', True, None),
            ('quantity_in_case', 'QuantityInCase', False, None),
            ('asin', 'ASIN', False, None),
            ('condition', 'Condition', False, None),
        ]
        # The expected MWS key for quantity is different for this operation.
        # This ensures we use the right key later on.
        quantity_key = 'Quantity'
    else:
        key_config = [
            ('sku', 'SellerSKU', True, None),
            ('quantity', 'QuantityShipped', True, None),
            ('quantity_in_case', 'QuantityInCase', False, None),
        ]
        quantity_key = 'QuantityShipped'

    items = []
    for item in item_args:
        if not isinstance(item, dict):
            raise MWSError("`item` argument must be a dict.")
        if not all(k in item for k in [c[0] for c in key_config if c[2]]):
            # Required keys of an item line missing
            raise MWSError((
                "`item` dict missing required keys: {required}."
                "\n- Optional keys: {optional}."
            ).format(
                required=', '.join([c[0] for c in key_config if c[2]]),
                optional=', '.join([c[0] for c in key_config if not c[2]]),
            ))

        item_dict = {
            'SellerSKU': item.get('sku'),
            quantity_key: item.get('quantity'),
            'QuantityInCase': item.get('quantity_in_case'),
        }
        item_dict.update({
            c[1]: item.get(c[0], c[3])
            for c in key_config
            if c[0] not in ['sku', 'quantity', 'quantity_in_case']
        })
        items.append(item_dict)

    return items


class InboundShipments(MWS):
    """
    Amazon MWS FulfillmentInboundShipment API

    Docs:
    http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Overview.html
    """
    URI = "/FulfillmentInboundShipment/2010-10-01"
    VERSION = '2010-10-01'
    NAMESPACE = '{http://mws.amazonaws.com/FulfillmentInboundShipment/2010-10-01/}'
    NEXT_TOKEN_OPERATIONS = [
        'ListInboundShipments',
        'ListInboundShipmentItems',
    ]

    # # HELPER METHODS # #
    def __init__(self, *args, **kwargs):
        """
        Allow the addition of a from_address dict during object initialization.
        kwarg "from_address" is caught and popped here,
        then calls set_ship_from_address.
        If empty or left out, empty dict is set by default.
        """
        self.from_address = {}
        addr = kwargs.pop('from_address', None)
        if addr is not None:
            self.set_ship_from_address(addr)
        super(InboundShipments, self).__init__(*args, **kwargs)

    def set_ship_from_address(self, address):
        """
        Verifies the structure of an address dictionary.
        Once verified against the KEY_CONFIG, saves a parsed version
        of that dictionary, ready to send to requests.
        """
        # Clear existing
        self.from_address = None

        if not address:
            raise MWSError('Missing required `address` dict.')
        if not isinstance(address, dict):
            raise MWSError("`address` must be a dict")

        key_config = [
            # Tuples composed of:
            # (input_key, output_key, is_required, default_value)
            ('name', 'Name', True, None),
            ('address_1', 'AddressLine1', True, None),
            ('address_2', 'AddressLine2', False, None),
            ('city', 'City', True, None),
            ('district_or_county', 'DistrictOrCounty', False, None),
            ('state_or_province', 'StateOrProvinceCode', False, None),
            ('postal_code', 'PostalCode', False, None),
            ('country', 'CountryCode', False, 'US'),
        ]

        # Check if all REQUIRED keys in address exist:
        if not all(k in address for k in
                   [c[0] for c in key_config if c[2]]):
            # Required parts of address missing
            raise MWSError((
                "`address` dict missing required keys: {required}."
                "\n- Optional keys: {optional}."
            ).format(
                required=", ".join([c[0] for c in key_config if c[2]]),
                optional=", ".join([c[0] for c in key_config if not c[2]]),
            ))

        # Passed tests. Assign values
        addr = {'ShipFromAddress.{}'.format(c[1]): address.get(c[0], c[3])
                for c in key_config}
        self.from_address = addr

    # # REQUEST METHODS # #
    def get_inbound_guidance_for_sku(self, skus, marketplace_id):
        """
        Returns inbound guidance for a list of items by Seller SKU.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForSKU.html
        """
        if not isinstance(skus, (list, tuple, set)):
            skus = [skus]
        data = {
            'Action': 'GetInboundGuidanceForSKU',
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('SellerSKUList.Id', skus))
        return self.make_request(data)

    def get_inbound_guidance_for_asin(self, asins, marketplace_id):
        """
        Returns inbound guidance for a list of items by ASIN.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetInboundGuidanceForASIN.html
        """
        if not isinstance(asins, (list, tuple, set)):
            asins = [asins]
        data = {
            'Action': 'GetInboundGuidanceForASIN',
            'MarketplaceId': marketplace_id,
        }
        data.update(utils.enumerate_param('ASINList.Id', asins))
        return self.make_request(data)

    def create_inbound_shipment_plan(self, items, country_code='US', subdivision_code='', label_preference=''):
        """
        Returns one or more inbound shipment plans, which provide the
        information you need to create inbound shipments.

        At least one dictionary must be passed as `args`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'asin', 'condition', 'quantity_in_case'

        'from_address' is required. Call 'set_ship_from_address' first before
        using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipmentPlan.html
        """
        if not items:
            raise MWSError("One or more `item` dict arguments required.")
        subdivision_code = subdivision_code or None
        label_preference = label_preference or None

        items = parse_item_args(items, 'CreateInboundShipmentPlan')
        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))

        data = {
            'Action': 'CreateInboundShipmentPlan',
            'ShipToCountryCode': country_code,
            'ShipToCountrySubdivisionCode': subdivision_code,
            'LabelPrepPreference': label_preference,
        }
        data.update(self.from_address)
        data.update(utils.enumerate_keyed_param(
            'InboundShipmentPlanRequestItems.member', items,
        ))
        return self.make_request(data, method="POST")

    def create_inbound_shipment(self, shipment_id, shipment_name, destination, items, shipment_status='',
                                label_preference='', case_required=False, box_contents_source=None):
        """
        Creates an inbound shipment to Amazon's fulfillment network.

        At least one dictionary must be passed as `items`. Each dictionary
        should contain the following keys:
          REQUIRED: 'sku', 'quantity'
          OPTIONAL: 'quantity_in_case'

        'from_address' is required. Call 'set_ship_from_address' first before
        using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_CreateInboundShipment.html
        """
        assert isinstance(shipment_id, str), "`shipment_id` must be a string."
        assert isinstance(shipment_name, str), "`shipment_name` must be a string."
        assert isinstance(destination, str), "`destination` must be a string."

        if not items:
            raise MWSError("One or more `item` dict arguments required.")

        items = parse_item_args(items, 'CreateInboundShipment')

        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))
        from_address = self.from_address
        from_address = {'InboundShipmentHeader.{}'.format(k): v
                        for k, v in from_address.items()}

        data = {
            'Action': 'CreateInboundShipment',
            'ShipmentId': shipment_id,
            'InboundShipmentHeader.ShipmentName': shipment_name,
            'InboundShipmentHeader.DestinationFulfillmentCenterId': destination,
            'InboundShipmentHeader.LabelPrepPreference': label_preference,
            'InboundShipmentHeader.AreCasesRequired': case_required,
            'InboundShipmentHeader.ShipmentStatus': shipment_status,
            'InboundShipmentHeader.IntendedBoxContentsSource': box_contents_source,
        }
        data.update(from_address)
        data.update(utils.enumerate_keyed_param(
            'InboundShipmentItems.member', items,
        ))
        return self.make_request(data, method="POST")

    def update_inbound_shipment(self, shipment_id, shipment_name,
                                destination, items=None, shipment_status='',
                                label_preference='', case_required=False,
                                box_contents_source=None):
        """
        Updates an existing inbound shipment in Amazon FBA.
        'from_address' is required. Call 'set_ship_from_address' first before using this operation.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_UpdateInboundShipment.html
        """
        # Assert these are strings, error out if not.
        assert isinstance(shipment_id, str), "`shipment_id` must be a string."
        assert isinstance(shipment_name, str), "`shipment_name` must be a string."
        assert isinstance(destination, str), "`destination` must be a string."

        # Parse item args
        if items:
            items = parse_item_args(items, 'UpdateInboundShipment')
        else:
            items = None

        # Raise exception if no from_address has been set prior to calling
        if not self.from_address:
            raise MWSError((
                "ShipFromAddress has not been set. "
                "Please use `.set_ship_from_address()` first."
            ))
        # Assemble the from_address using operation-specific header
        from_address = self.from_address
        from_address = {'InboundShipmentHeader.{}'.format(k): v
                        for k, v in from_address.items()}

        data = {
            'Action': 'UpdateInboundShipment',
            'ShipmentId': shipment_id,
            'InboundShipmentHeader.ShipmentName': shipment_name,
            'InboundShipmentHeader.DestinationFulfillmentCenterId': destination,
            'InboundShipmentHeader.LabelPrepPreference': label_preference,
            'InboundShipmentHeader.AreCasesRequired': case_required,
            'InboundShipmentHeader.ShipmentStatus': shipment_status,
            'InboundShipmentHeader.IntendedBoxContentsSource': box_contents_source,
        }
        data.update(from_address)
        if items:
            # Update with an items paramater only if they exist.
            data.update(utils.enumerate_keyed_param(
                'InboundShipmentItems.member', items,
            ))
        return self.make_request(data, method="POST")

    def get_preorder_info(self, shipment_id):
        """
        Returns pre-order information, including dates, that a seller needs before confirming a shipment for pre-order.
        Also indicates if a shipment has already been confirmed for pre-order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPreorderInfo.html
        """
        data = {
            'Action': 'GetPreorderInfo',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data)

    def confirm_preorder(self, shipment_id, need_by_date):
        """
        Confirms a shipment for pre-order.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmPreorder.html
        """
        data = {
            'Action': 'ConfirmPreorder',
            'ShipmentId': shipment_id,
            'NeedByDate': need_by_date,
        }
        return self.make_request(data)

    def get_prep_instructions_for_sku(self, skus=None, country_code=None):
        """
        Returns labeling requirements and item preparation instructions
        to help you prepare items for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForSKU.html
        """
        country_code = country_code or 'US'
        skus = skus or []

        # 'skus' should be a unique list, or there may be an error returned.
        skus = utils.unique_list_order_preserved(skus)

        data = {
            'Action': 'GetPrepInstructionsForSKU',
            'ShipToCountryCode': country_code,
        }
        data.update(utils.enumerate_params({
            'SellerSKUList.ID.': skus,
        }))
        return self.make_request(data, method="POST")

    def get_prep_instructions_for_asin(self, asins=None, country_code=None):
        """
        Returns item preparation instructions to help with item sourcing decisions.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPrepInstructionsForASIN.html
        """
        country_code = country_code or 'US'
        asins = asins or []

        # 'asins' should be a unique list, or there may be an error returned.
        asins = utils.unique_list_order_preserved(asins)

        data = {
            'Action': 'GetPrepInstructionsForASIN',
            'ShipToCountryCode': country_code,
        }
        data.update(utils.enumerate_params({
            'ASINList.ID.': asins,
        }))
        return self.make_request(data, method="POST")

    # # TODO this method is incomplete: it should be able to account for all TransportDetailInput types
    # def put_transport_content(self, shipment_id, is_partnered, shipment_type, carrier_name, tracking_id):
    #     """
    #     Sends transportation information to Amazon about an inbound shipment.

    #     Docs:
    #     http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_Datatypes.html#TransportDetailInput
    #     """
    #     data = {
    #         'Action': 'PutTransportContent',
    #         'ShipmentId': shipment_id,
    #         'IsPartnered': is_partnered,
    #         'ShipmentType': shipment_type,
    #     }
    #     data['TransportDetails.NonPartneredSmallParcelData.CarrierName'] = carrier_name
    #     if isinstance(tracking_id, tuple):
    #         count = 0
    #         for track in tracking_id:
    #             data[
    #                 'TransportDetails.NonPartneredSmallParcelData.PackageList.member.{}.TrackingId'.format(count + 1)
    #             ] = track
    #     return self.make_request(data)

    def estimate_transport_request(self, shipment_id):
        """
        Requests an estimate of the shipping cost for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_EstimateTransportRequest.html
        """
        data = {
            'Action': 'EstimateTransportRequest',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data, method="POST")

    def get_transport_content(self, shipment_id):
        """
        Returns current transportation information about an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetTransportContent.html
        """
        data = {
            'Action': 'GetTransportContent',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data, method="POST")

    def confirm_transport_request(self, shipment_id):
        """
        Confirms that you accept the Amazon-partnered shipping estimate and you request that the
        Amazon-partnered carrier ship your inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ConfirmTransportRequest.html
        """
        data = {
            'Action': 'ConfirmTransportRequest',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data)

    def void_transport_request(self, shipment_id):
        """
        Voids a previously-confirmed request to ship your inbound shipment
        using an Amazon-partnered carrier.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_VoidTransportRequest.html
        """
        data = {
            'Action': 'VoidTransportRequest',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data, method="POST")

    def get_package_labels(self, shipment_id, num_labels, page_type=None):
        """
        Returns PDF document data for printing package labels for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPackageLabels.html
        """
        data = {
            'Action': 'GetPackageLabels',
            'ShipmentId': shipment_id,
            'PageType': page_type,
            'NumberOfPackages': num_labels,
        }
        return self.make_request(data, method="POST")

    def get_unique_package_labels(self, shipment_id, page_type, package_ids):
        """
        Returns unique package labels for faster and more accurate shipment processing at the Amazon fulfillment center.

        `shipment_id` must match a valid, current shipment.
        `page_type` expected to be string matching one of following (not checked, in case Amazon requirements change):
            PackageLabel_Letter_2
            PackageLabel_Letter_6
            PackageLabel_A4_2
            PackageLabel_A4_4
            PackageLabel_Plain_Pape
        `package_ids` a single package identifier, or a list/tuple/set of identifiers, specifying for which package(s)
            you want package labels printed.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetUniquePackageLabels.html
        """
        data = {
            'Action': 'GetUniquePackageLabels',
            'ShipmentId': shipment_id,
            'PageType': page_type,
        }
        if not isinstance(package_ids, (list, tuple, set)):
            package_ids = [package_ids]
        data.update(utils.enumerate_param('PackageLabelsToPrint.member.', package_ids))
        return self.make_request(data)

    def get_pallet_labels(self, shipment_id, page_type, num_labels):
        """
        Returns pallet labels.
        `shipment_id` must match a valid, current shipment.
        `page_type` expected to be string matching one of following (not checked, in case Amazon requirements change):
            PackageLabel_Letter_2
            PackageLabel_Letter_6
            PackageLabel_A4_2
            PackageLabel_A4_4
            PackageLabel_Plain_Pape
        `num_labels` is integer, number of labels to create.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetPalletLabels.html
        """
        data = {
            'Action': 'GetPalletLabels',
            'ShipmentId': shipment_id,
            'PageType': page_type,
            'NumberOfPallets': num_labels,
        }
        return self.make_request(data)

    def get_bill_of_lading(self, shipment_id):
        """
        Returns PDF document data for printing a bill of lading for an inbound shipment.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_GetBillOfLading.html
        """
        data = {
            'Action': 'GetBillOfLading',
            'ShipmentId': shipment_id,
        }
        return self.make_request(data, "POST")

    @next_token_action('ListInboundShipments')
    def list_inbound_shipments(self, shipment_ids=None, shipment_statuses=None,
                               last_updated_after=None, last_updated_before=None, next_token=None):
        """
        Returns list of shipments based on statuses, IDs, and/or
        before/after datetimes.

        Pass `next_token` to call "ListInboundShipmentsByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipments.html
        """
        data = {
            'Action': 'ListInboundShipments',
            'LastUpdatedAfter': last_updated_after,
            'LastUpdatedBefore': last_updated_before,
        }
        data.update(utils.enumerate_params({
            'ShipmentStatusList.member.': shipment_statuses,
            'ShipmentIdList.member.': shipment_ids,
        }))
        return self.make_request(data, method="POST")

    def list_inbound_shipments_by_next_token(self, token):
        """
        Alias for `list_inbound_shipments(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentsByNextToken.html
        """
        return self.list_inbound_shipments(next_token=token)

    @next_token_action('ListInboundShipmentItems')
    def list_inbound_shipment_items(self, shipment_id=None, last_updated_after=None,
                                    last_updated_before=None, next_token=None):
        """
        Returns list of items within inbound shipments and/or
        before/after datetimes.

        Pass `next_token` to call "ListInboundShipmentItemsByNextToken" instead.

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItems.html
        """
        data = {
            'Action': 'ListInboundShipmentItems',
            'ShipmentId': shipment_id,
            'LastUpdatedAfter': last_updated_after,
            'LastUpdatedBefore': last_updated_before,
        }
        return self.make_request(data, method="POST")

    def list_inbound_shipment_items_by_next_token(self, token):
        """
        Alias for `list_inbound_shipment_items(next_token=token)`

        Docs:
        http://docs.developer.amazonservices.com/en_US/fba_inbound/FBAInbound_ListInboundShipmentItemsByNextToken.html
        """
        return self.list_inbound_shipment_items(next_token=token)
