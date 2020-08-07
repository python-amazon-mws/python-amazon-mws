"""Tests for the Subscriptions API class."""

import unittest
import mws
from .utils import CommonAPIRequestTools


class SubscriptionsTestCase(CommonAPIRequestTools, unittest.TestCase):
    """Test cases for Subscriptions."""

    api_class = mws.Subscriptions

    # TODO: Add remaining methods for Subscriptions
