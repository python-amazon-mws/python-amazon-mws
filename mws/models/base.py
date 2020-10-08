"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod


class MWSDataType(ABC):
    """Base class for data type models used for MWS requests."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a flattened dict of parameters suitable for an MWS request."""
        pass
