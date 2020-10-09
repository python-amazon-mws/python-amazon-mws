"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Union

from mws.utils import flat_param_dict


class MWSDataType(ABC):
    """Base class for data type models used for MWS requests."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns a flattened dict of parameters suitable for an MWS request."""
        pass

    @staticmethod
    def _flatten(value: Union[str, Mapping, Iterable], prefix: str = "") -> dict:
        return flat_param_dict(value, prefix=prefix)
