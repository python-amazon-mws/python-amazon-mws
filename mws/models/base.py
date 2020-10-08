"""Base models for datatypes used in MWS."""

from abc import ABCMeta, abstractmethod


class MWSDataType:
    """Abstract base class for data type models used for MWS requests."""

    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a flattened dict of parameters suitable for an MWS request."""
        pass
