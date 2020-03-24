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

    def get_pickup_slots(self, marketplaceid=None, amazon_order_id=None, package_width=0,
                         package_height=0, package_length=0, package_dimensions_uom='cm',
                         package_weight=0, package_weight_uom='g'):
        data = {
            'Action': 'ListPickupSlots',
            'MarketplaceId': marketplaceid,
            'AmazonOrderId': amazon_order_id,
            'PackageDimensions.Width': str(package_width),
            'PackageDimensions.Length': str(package_length),
            'PackageDimensions.Height': str(package_height),
            'PackageDimensions.Unit': package_dimensions_uom,
            'PackageWeight.Unit': package_weight_uom,
            'PackageWeight.Value': str(package_weight)
        }
        return self.make_request(data)

    def create_scheduled_package(self, marketplaceid=None, amazon_order_id=None, package_width=0,
                                 package_height=0, package_length=0, package_dimensions_uom='cm',
                                 package_weight=0, package_weight_uom='g',
                                 package_slot_id=None, package_slot_start_time=None,
                                 package_slot_end_time=None):
        data = {
            'Action': 'CreateScheduledPackage',
            'MarketplaceId': marketplaceid,
            'AmazonOrderId': amazon_order_id,
            'PackageRequestDetails.PackageDimensions.Length': str(package_length),
            'PackageRequestDetails.PackageDimensions.Width': str(package_width),
            'PackageRequestDetails.PackageDimensions.Height': str(package_height),
            'PackageRequestDetails.PackageDimensions.Unit': package_dimensions_uom,
            'PackageRequestDetails.PackageWeight.Unit': package_weight_uom,
            'PackageRequestDetails.PackageWeight.Value': str(package_weight),
            'PackageRequestDetails.PackagePickupSlot.SlotId': package_slot_id,
            'PackageRequestDetails.PackagePickupSlot.PickupTimeStart': package_slot_start_time,
            'PackageRequestDetails.PackagePickupSlot.PickupTimeEnd': package_slot_end_time
        }
        return self.make_request(data)

    def update_scheduled_package(self, marketplaceid=None, amazon_order_id=None, package_id=None,
                                 slot_id=None, package_slot_start_time=None, package_slot_end_time=None):
        data = {
            'Action': 'UpdateScheduledPackages',
            'MarketplaceId': marketplaceid
        }
        scheduled_packages = [{
            'ScheduledPackageId.AmazonOrderId': amazon_order_id,
            'ScheduledPackageId.PackageId': package_id
        }]
        data.update(utils.enumerate_keyed_param('ScheduledPackageUpdateDetailsList.PackageUpdateDetails',
                                                scheduled_packages))
        pickup_slots = [{
            'PackagePickupSlot.SlotId': slot_id,
            'PackagePickupSlot.PickupTimeStart': package_slot_start_time,
            'PackagePickupSlot.PickupTimeEnd': package_slot_end_time
        }]
        data.update(utils.enumerate_keyed_param('ScheduledPackageUpdateDetailsList.PackageUpdateDetails',
                                                pickup_slots))
        return self.make_request(data)

    def get_scheduled_package(self, marketplaceid=None, amazon_order_id=None,
                              scheduled_package_id=None):
        data = {
            'Action': 'GetScheduledPackage',
            'MarketplaceId': marketplaceid,
            'ScheduledPackageId.AmazonOrderId': amazon_order_id,
            'ScheduledPackageId.PackageId': scheduled_package_id,
        }
        return self.make_request(data)
