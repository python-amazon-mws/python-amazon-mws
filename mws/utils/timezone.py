"""Datetime, TZ, and other related utilities."""

import datetime


def utc_timestamp():
    """Returns the current UTC timestamp in ISO-8601 format."""
    return datetime.datetime.utcnow().replace(microsecond=0).isoformat()
