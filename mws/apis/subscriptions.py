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
    URI = '/Subscriptions/2013-07-01'
    VERSION = '2013-07-01'
    NAMESPACE = "{http://mws.amazonaws.com/Subscriptions/2013-07-01}"

    # TODO include a helper method for configuring and saving a destination to the object with a keyname
    # This might cut down on some time setting up all the values for the destination for each call,
    # particularly if someone needs to make several calls at once for the same destination.

    def register_destination(self, marketplace_id, delivery_channel='SQS', attribute_list=None):
        """
        Specifies a new destination where you want to receive notifications.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_RegisterDestination.html

        delivery_channel: Currently only supports SQS
        attribute_list: example [{"sqsQueueUrl" : "https://sqs.us-east-1.amazonaws.com/51471EXAMPLE/mws_notifications"}]

        """
        if attribute_list is None:
            raise ValueError('attribute_list cannot be None')
        data = {
            'Action': 'RegisterDestination',
            'MarketplaceId': marketplace_id,
            'Destination.DeliveryChannel': delivery_channel
        }
        data.update(utils.enumerate_keyed_param('Destination.AttributeList.member', attribute_list))
        return self.make_request(data,'POST')

    def deregister_destination(self, marketplace_id, delivery_channel='SQS', attribute_list=None):
        """
        Removes an existing destination from the list of registered destinations.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeregisterDestination.html
        """
        if attribute_list is None:
            raise ValueError('attribute_list cannot be None')
        data = {
            'Action': 'DeregisterDestination',
            'MarketplaceId': marketplace_id,
            'Destination.DeliveryChannel': delivery_channel
        }
        data.update(utils.enumerate_keyed_param('Destination.AttributeList.member', attribute_list))
        return self.make_request(data,'POST')


    def list_registered_destinations(self, marketplace_id):
        """
        Lists all current destinations that you have registered.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListRegisteredDestinations.html
        """
        data = {
            'Action': 'ListRegisteredDestinations',
            'MarketplaceId': marketplace_id
        }
        return self.make_request(data,'POST')

    def send_test_notification_to_destination(self):
        """
        Sends a test notification to an existing destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_SendTestNotificationToDestination.html
        """
        raise NotImplementedError

    def create_subscription(self):
        """
        Creates a new subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_CreateSubscription.html
        """
        raise NotImplementedError

    def get_subscription(self):
        """
        Gets the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_GetSubscription.html
        """
        raise NotImplementedError

    def delete_subscription(self):
        """
        Deletes the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_DeleteSubscription.html
        """
        raise NotImplementedError

    def list_subscriptions(self, marketplace_id):
        """
        Returns a list of all your current subscriptions.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_ListSubscriptions.html
        """
        data = {
            'Action': 'ListSubscriptions',
            'MarketplaceId': marketplace_id,
        }
        return self.make_request(data, 'POST')

    def update_subscription(self):
        """
        Updates the subscription for the specified notification type and destination.

        Docs:
        http://docs.developer.amazonservices.com/en_US/subscriptions/Subscriptions_UpdateSubscription.html
        """
        raise NotImplementedError
