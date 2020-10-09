"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod

from mws.utils import flat_param_dict


class MWSDataType(ABC):
    """Base class for data type models used for MWS requests."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a flattened dict of parameters suitable for an MWS request."""
        pass

    @staticmethod
    def _flatten(value, prefix=""):
        """Returns a flattened params dictionary by collapsing nested dicts and non-string iterables.

        Refer to ``mws.utils.flat_param_dict`` for details.
        """
        return flat_param_dict(value, prefix=prefix)
