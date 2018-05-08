"""
Amazon MWS Subscriptions API
"""
from __future__ import absolute_import

from ..mws import MWS
from .. import utils
# from .. import utils

# TODO include NotificationType enumeration
# TODO set up a basic object for Subscription and Destination types?


class Subscriptions(MWS):
    """
    Amazon MWS Subscriptions API

    Docs:
    http://docs.developer.amazonservices.com/en_US/subscriptions/index.html
    """
    URI = "/Subscriptions/2013-07-01"
    VERSION = "2013-07-01"
    NAMESPACE = "{http://mws.amazonaws.com/Subscriptions/2013-07-01}"

    # TODO include a helper method for configuring and saving a destination to the object with a keyname
    # This might cut down on some time setting up all the values for the destination for each call,
    # particularly if someone needs to make several calls at once for the same destination.

    def register_destination(self, marketplace_id, delivery_channel="SQS", attribute_list=None):
        """
        Specifies a new destination where you want to receive notifications.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_RegisterDestination.html

        delivery_channel: Currently only supports SQS
        attribute_list: example [{"sqsQueueUrl" : "https://sqs.us-east-1.amazonaws.com/51471EXAMPLE/mws_notifications"}]

        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")

        data = {
            "Action": "RegisterDestination",
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel
        }
        data.update(utils.enumerate_keyed_param("Destination.AttributeList.member", attribute_list))

        return self.make_request(data, "POST")

    def deregister_destination(self, marketplace_id, delivery_channel="SQS", attribute_list=None):
        """
        Removes an existing destination from the list of registered destinations.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeregisterDestination.html
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")

        data = {
            "Action": "DeregisterDestination",
            "MarketplaceId": marketplace_id,
            "Destination.DeliveryChannel": delivery_channel
        }
        data.update(utils.enumerate_keyed_param("Destination.AttributeList.member", attribute_list))

        return self.make_request(data, "POST")

    def list_registered_destinations(self, marketplace_id):
        """
        Lists all current destinations that you have registered.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListRegisteredDestinations.html
        """
        data = {"Action": "ListRegisteredDestinations",
                "MarketplaceId": marketplace_id}

        return self.make_request(data, "POST")

    def send_test_notification_to_destination(self, marketplace_id, delivery_channel="SQS", attribute_list=None):
        """
        Sends a test notification to an existing destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_SendTestNotificationToDestination.html

        destination_list ={ "Key": "sqsQueueUrl",
         "Value": "destination" }
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")

        data = {"Action": "SendTestNotificationToDestination",
                "MarketplaceId": marketplace_id,
                "Destination.DeliveryChannel": delivery_channel}
        data.update(utils.enumerate_keyed_param("Destination.AttributeList.member", attribute_list))

        return self.make_request(data, method="POST")

    def create_subscription(self, marketplace_id, delivery_channel="SQS", attribute_list=None,
                            _type=None, is_enabled=True):
        """
        Creates a new subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_CreateSubscription.html
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")
        if _type is None:
            raise ValueError("_type cannot be None")
        data = {"Action": "CreateSubscription",
                "MarketplaceId": marketplace_id,
                "Subscription.Destination.DeliveryChannel": delivery_channel,
                "Subscription.IsEnabled": str(is_enabled).lower(),
                "Subscription.NotificationType": _type}
        data.update(utils.enumerate_keyed_param("Subscription.Destination.AttributeList.member", attribute_list))

        return self.make_request(data, "POST")

    def get_subscription(self, marketplace_id, delivery_channel="SQS", attribute_list=None, _type=None):
        """
        Gets the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_GetSubscription.html
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")
        if _type is None:
            raise ValueError("_type cannot be None")
        data = {"Action": "GetSubscription",
                "MarketplaceId": marketplace_id,
                "Subscription.Destination.DeliveryChannel": delivery_channel,
                "Subscription.NotificationType": _type}

        return self.make_request(data, "POST")

    def delete_subscription(self, marketplace_id, delivery_channel="SQS", attribute_list=None, _type=None):
        """
        Deletes the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeleteSubscription.html
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")
        if _type is None:
            raise ValueError("_type cannot be None")
        data = {"Action": "DeleteSubscription",
                "MarketplaceId": marketplace_id,
                "Destination.DeliveryChannel": delivery_channel,
                "NotificationType": _type}
        data.update(utils.enumerate_keyed_param("Destination.AttributeList.member", attribute_list))

        return self.make_request(data, "POST")

    def list_subscriptions(self, marketplace_id):
        """
        Returns a list of all your current subscriptions.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListSubscriptions.html
        """
        data = {
            "Action": "ListSubscriptions",
            "MarketplaceId": marketplace_id,
        }

        return self.make_request(data, "POST")

    def update_subscription(self, marketplace_id, delivery_channel="SQS", attribute_list=None,
                            _type=None, is_enabled=True):
        """
        Updates the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_UpdateSubscription.html
        """
        if attribute_list is None:
            raise ValueError("Attribute_list cannot be None")
        if _type is None:
            raise ValueError("_type cannot be None")
        data = {"Action": "UpdateSubscription",
                "MarketplaceId": marketplace_id,
                "Subscription.Destination.DeliveryChannel": delivery_channel,
                "Subscription.IsEnabled": str(is_enabled).lower(),
                "Subscription.NotificationType": _type}

        data.update(utils.enumerate_keyed_param("Subscription.Destination.AttributeList.member", attribute_list))
        return self.make_request(data, "POST")
