"""Amazon Easyship API."""

from mws import MWS, utils


def validate_package_update_details(package_update_details):
    """
    raises error if the package_update_details is not valid
    used in the easyship api function update_scheduled_packages
    """
    error_msg = (
        "package_update_details must be a list of dicts, each with "
        "required keys `amazon_order_id`, `package_id`, and `slot_id` "
        "(optional keys: `slot_start_time` and `slot_end_time`)"
    )
    required_keys = {"amazon_order_id", "package_id", "slot_id"}
    if not isinstance(package_update_details, list):
        raise TypeError(error_msg)
    if not all(isinstance(i, dict) for i in package_update_details):
        raise TypeError(error_msg)
    if not all(required_keys.issubset(set(i.keys())) for i in package_update_details):
        raise KeyError(error_msg)


class EasyShip(MWS):
    """
        Amazon EasyShip API
        docs: http://docs.developer.amazonservices.com/en_IN/easy_ship/EasyShip_Overview.html
    """

    URI = "/EasyShip/2018-09-01"
    VERSION = "2018-09-01"
    NAMESPACE = "{https://mws.amazonservices.in/EasyShip/2018-09-01}"

    def list_pickup_slots(
        self,
        marketplace_id=None,
        amazon_order_id=None,
        package_width=0,
        package_height=0,
        package_length=0,
        package_dimensions_uom="cm",
        package_weight=0,
        package_weight_uom="g",
    ):
        data = {
            "Action": "ListPickupSlots",
            "MarketplaceId": marketplace_id,
            "AmazonOrderId": amazon_order_id,
            "PackageDimensions.Width": str(package_width),
            "PackageDimensions.Length": str(package_length),
            "PackageDimensions.Height": str(package_height),
            "PackageDimensions.Unit": package_dimensions_uom,
            "PackageWeight.Unit": package_weight_uom,
            "PackageWeight.Value": str(package_weight),
        }
        return self.make_request(data)

    def create_scheduled_package(
        self,
        marketplace_id=None,
        amazon_order_id=None,
        package_width=0,
        package_height=0,
        package_length=0,
        package_dimensions_uom="cm",
        package_weight=0,
        package_weight_uom="g",
        slot_id=None,
        slot_start_time=None,
        slot_end_time=None,
        package_identifier=None,
    ):
        data = {
            "Action": "CreateScheduledPackage",
            "MarketplaceId": marketplace_id,
            "AmazonOrderId": amazon_order_id,
            "PackageRequestDetails.PackageDimensions.Length": str(package_length),
            "PackageRequestDetails.PackageDimensions.Width": str(package_width),
            "PackageRequestDetails.PackageDimensions.Height": str(package_height),
            "PackageRequestDetails.PackageDimensions.Unit": package_dimensions_uom,
            "PackageRequestDetails.PackageWeight.Unit": package_weight_uom,
            "PackageRequestDetails.PackageWeight.Value": str(package_weight),
            "PackageRequestDetails.PackagePickupSlot.SlotId": slot_id,
            "PackageRequestDetails.PackagePickupSlot.PickupTimeStart": slot_start_time,
            "PackageRequestDetails.PackagePickupSlot.PickupTimeEnd": slot_end_time,
            "PackageRequestDetails.PackageIdentifier": package_identifier,
        }
        return self.make_request(data)

    def update_scheduled_packages(
        self, marketplace_id=None, package_update_details=None
    ):
        data = {"Action": "UpdateScheduledPackages", "MarketplaceId": marketplace_id}
        package_update_data_list = []
        package_update_details = package_update_details or []
        if package_update_details:
            validate_package_update_details(package_update_details)
        for detail in package_update_details:
            package_update_data = dict()
            package_update_data["ScheduledPackageId.AmazonOrderId"] = detail.get(
                "amazon_order_id"
            )
            package_update_data["ScheduledPackageId.PackageId"] = detail.get(
                "package_id"
            )
            package_update_data["PackagePickupSlot.SlotId"] = detail.get("slot_id")
            package_update_data["PackagePickupSlot.PickupTimeStart"] = detail.get(
                "slot_start_time"
            )
            package_update_data["PackagePickupSlot.PickupTimeEnd"] = detail.get(
                "slot_end_time"
            )
            package_update_data_list.append(package_update_data)

        data.update(
            utils.enumerate_keyed_param(
                "ScheduledPackageUpdateDetailsList.PackageUpdateDetails",
                package_update_data_list,
            )
        )
        return self.make_request(data)

    def get_scheduled_package(
        self, marketplace_id=None, amazon_order_id=None, package_id=None
    ):
        data = {
            "Action": "GetScheduledPackage",
            "MarketplaceId": marketplace_id,
            "ScheduledPackageId.AmazonOrderId": amazon_order_id,
            "ScheduledPackageId.PackageId": package_id,
        }
        return self.make_request(data)
