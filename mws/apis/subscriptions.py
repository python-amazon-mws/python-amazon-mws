"""Amazon MWS Subscriptions API."""

from mws import MWS
from mws.utils.params import coerce_to_bool
from mws.utils.params import enumerate_keyed_param

# TODO include NotificationType enumeration
# TODO set up a basic object for Subscription and Destination types?


class Subscriptions(MWS):
    """Amazon MWS Subscriptions API

    Docs:
    https://docs.developer.amazonservices.com/en_US/subscriptions/index.html
    """

    URI = "/Subscriptions/2013-07-01"
    VERSION = "2013-07-01"
    NAMESPACE = "{http://mws.amazonaws.com/Subscriptions/2013-07-01}"

    # TODO include a helper method for configuring and saving a destination to the object with a keyname
    # This might cut down on some time setting up all the values for the destination for each call,
    # particularly if someone needs to make several calls at once for the same destination.

    def _parse_attributes(self, attributes):
        if not attributes or not isinstance(attributes, dict):
            # Return empty dict so it can easily pass to `data.update()`
            return {}
        attribute_list = []
        for key, val in attributes.items():
            attribute_list.append({"Key": key, "Value": val})
        return attribute_list

    def register_destination(
        self, marketplace_id, attributes=None, delivery_channel="SQS"
    ):
        """Specifies a new destination where you want to receive notifications.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_RegisterDestination.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        if attributes is None:
            raise ValueError("attributes cannot be None")

        data = {
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel,
        }
        data.update(
            enumerate_keyed_param(
                "Destination.AttributeList.member", self._parse_attributes(attributes)
            )
        )
        return self.make_request("RegisterDestination", data, method="POST")

    def deregister_destination(
        self, marketplace_id, attributes=None, delivery_channel="SQS"
    ):
        """Removes an existing destination from the list of registered destinations.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeregisterDestination.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        if attributes is None:
            raise ValueError("attributes cannot be None")

        data = {
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel,
        }
        data.update(
            enumerate_keyed_param(
                "Destination.AttributeList.member", self._parse_attributes(attributes)
            )
        )
        return self.make_request("DeregisterDestination", data, method="POST")

    def list_registered_destinations(self, marketplace_id):
        """Lists all current destinations that you have registered.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListRegisteredDestinations.html
        """
        return self.make_request(
            "ListRegisteredDestinations",
            {"MarketplaceId": marketplace_id},
            method="POST",
        )

    def send_test_notification_to_destination(
        self, marketplace_id, attributes, delivery_channel="SQS"
    ):
        """Sends a test notification to an existing destination.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_SendTestNotificationToDestination.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        data = {
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel,
        }
        data.update(
            enumerate_keyed_param(
                "Destination.AttributeList.member", self._parse_attributes(attributes)
            )
        )
        return self.make_request(
            "SendTestNotificationToDestination", data, method="POST"
        )

    def create_subscription(
        self,
        marketplace_id,
        attributes,
        notification_type,
        is_enabled=True,
        delivery_channel="SQS",
    ):
        """Creates a new subscription for the specified notification type and destination.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_CreateSubscription.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        if is_enabled is not None:
            is_enabled = coerce_to_bool(is_enabled)
        data = {
            "MarketplaceId": marketplace_id,
            "Subscription.Destination.DeliveryChannel": delivery_channel,
            "Subscription.IsEnabled": is_enabled,
            "Subscription.NotificationType": notification_type,
        }
        data.update(
            enumerate_keyed_param(
                "Subscription.Destination.AttributeList.member",
                self._parse_attributes(attributes),
            )
        )
        return self.make_request("CreateSubscription", data, method="POST")

    def get_subscription(
        self,
        marketplace_id,
        attributes,
        notification_type,
        delivery_channel="SQS",
    ):
        """Gets the subscription for the specified notification type and destination.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_GetSubscription.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        data = {
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel,
            "NotificationType": notification_type,
        }
        data.update(
            enumerate_keyed_param(
                "Destination.AttributeList.member", self._parse_attributes(attributes)
            )
        )
        return self.make_request("GetSubscription", data, method="POST")

    def delete_subscription(
        self,
        marketplace_id,
        attributes,
        notification_type,
        delivery_channel="SQS",
    ):
        """Deletes the subscription for the specified notification type and destination.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeleteSubscription.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        data = {
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel,
            "NotificationType": notification_type,
        }
        data.update(
            enumerate_keyed_param(
                "Destination.AttributeList.member", self._parse_attributes(attributes)
            )
        )
        return self.make_request("DeleteSubscription", data, method="POST")

    def list_subscriptions(self, marketplace_id):
        """Returns a list of all your current subscriptions.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListSubscriptions.html
        """
        return self.make_request(
            "ListSubscriptions", {"MarketplaceId": marketplace_id}, method="POST"
        )

    def update_subscription(
        self,
        marketplace_id,
        attributes,
        notification_type,
        is_enabled=True,
        delivery_channel="SQS",
    ):
        """Updates the subscription for the specified notification type and destination.

        Docs:
        https://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_UpdateSubscription.html

        delivery_channel: Currently only supports SQS
        attributes: example {"sqsQueueUrl": "https://sqs.eu-west-2.amazonaws.com/378051892504/Amazon_MWS_Notify"}
        """
        if is_enabled is not None:
            is_enabled = coerce_to_bool(is_enabled)
        data = {
            "MarketplaceId": marketplace_id,
            "Subscription.Destination.DeliveryChannel": delivery_channel,
            "Subscription.IsEnabled": is_enabled,
            "Subscription.NotificationType": notification_type,
        }
        data.update(
            enumerate_keyed_param(
                "Subscription.Destination.AttributeList.member",
                self._parse_attributes(attributes),
            )
        )
        return self.make_request("UpdateSubscription", data, method="POST")
