"""Base models for datatypes used in MWS."""

from abc import ABCMeta, abstractmethod


class MWSDataType:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a flattened dict of parameters suitable for an MWS request."""
        pass
