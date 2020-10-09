"""Datetime, TZ, and other related utilities."""

import datetime


def mws_utc_now():
    """Returns the current UTC time, as expected by MWS.
    Note that we set microseconds to 0 automatically with this method:
    if you want the true UTC datetime, just run `datetime.datetime.utcnow()`.
    """
    return datetime.datetime.utcnow().replace(microsecond=0)
