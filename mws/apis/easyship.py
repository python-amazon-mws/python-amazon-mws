"""
Amazon Easyship API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils


class EasyShip(MWS):
    """
        Amazon EasyShip API
        docs: http://docs.developer.amazonservices.com/en_IN/easy_ship/EasyShip_Overview.html
    """
    URI = "/EasyShip/2018-09-01"
    VERSION = "2018-09-01"
    NAMESPACE = '{https://mws.amazonservices.in/EasyShip/2018-09-01}'

    def list_pickup_slots(self, marketplace_id=None, amazon_order_id=None, package_width=0,
                          package_height=0, package_length=0, package_dimensions_uom='cm',
                          package_weight=0, package_weight_uom='g'):
        data = {
            'Action': 'ListPickupSlots',
            'MarketplaceId': marketplace_id,
            'AmazonOrderId': amazon_order_id,
            'PackageDimensions.Width': str(package_width),
            'PackageDimensions.Length': str(package_length),
            'PackageDimensions.Height': str(package_height),
            'PackageDimensions.Unit': package_dimensions_uom,
            'PackageWeight.Unit': package_weight_uom,
            'PackageWeight.Value': str(package_weight)
        }
        return self.make_request(data)

    def create_scheduled_package(self, marketplace_id=None, amazon_order_id=None, package_width=0,
                                 package_height=0, package_length=0, package_dimensions_uom='cm',
                                 package_weight=0, package_weight_uom='g',
                                 slot_id=None, slot_start_time=None,
                                 slot_end_time=None, package_identifier=None):
        data = {
            'Action': 'CreateScheduledPackage',
            'MarketplaceId': marketplace_id,
            'AmazonOrderId': amazon_order_id,
            'PackageRequestDetails.PackageDimensions.Length': str(package_length),
            'PackageRequestDetails.PackageDimensions.Width': str(package_width),
            'PackageRequestDetails.PackageDimensions.Height': str(package_height),
            'PackageRequestDetails.PackageDimensions.Unit': package_dimensions_uom,
            'PackageRequestDetails.PackageWeight.Unit': package_weight_uom,
            'PackageRequestDetails.PackageWeight.Value': str(package_weight),
            'PackageRequestDetails.PackagePickupSlot.SlotId': slot_id,
            'PackageRequestDetails.PackagePickupSlot.PickupTimeStart': slot_start_time,
            'PackageRequestDetails.PackagePickupSlot.PickupTimeEnd': slot_end_time,
            'PackageRequestDetails.PackageIdentifier': package_identifier

        }
        return self.make_request(data)

    def update_scheduled_packages(self, marketplace_id=None, package_update_details=None):
        data = {
            'Action': 'UpdateScheduledPackages',
            'MarketplaceId': marketplace_id
        }
        package_update_details = package_update_details or []
        for detail in package_update_details:
            detail['ScheduledPackageId.AmazonOrderId'] = detail.pop('amazon_order_id')
            detail['ScheduledPackageId.PackageId'] = detail.pop('package_id')
            detail['PackagePickupSlot.SlotId'] = detail.pop('slot_id')
            detail['PackagePickupSlot.PickupTimeStart'] = detail.pop('slot_start_time', None)
            detail['PackagePickupSlot.PickupTimeEnd'] = detail.pop('slot_end_time', None)

        data.update(utils.enumerate_keyed_param('ScheduledPackageUpdateDetailsList.PackageUpdateDetails',
                                                package_update_details))
        return self.make_request(data)

    def get_scheduled_package(self, marketplace_id=None, amazon_order_id=None,
                              package_id=None):
        data = {
            'Action': 'GetScheduledPackage',
            'MarketplaceId': marketplace_id,
            'ScheduledPackageId.AmazonOrderId': amazon_order_id,
            'ScheduledPackageId.PackageId': package_id,
        }
        return self.make_request(data)
