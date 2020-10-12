"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod
from os import stat
from typing import Any, Iterable, Mapping, Union
from enum import Enum

from mws.utils import flat_param_dict


class MWSDataType(ABC):
    """Base class for data type models used for MWS requests."""

    @abstractmethod
    def params_dict(self) -> dict:
        """Returns a dict of this model's parameters suitable for an MWS request."""
        pass

    def to_params(self, prefix: str = "") -> dict:
        params_dict = self.params_dict()
        return flat_param_dict(params_dict, prefix=prefix)

    @staticmethod
    def flat_param_dict(value: Union[str, Mapping, Iterable], prefix: str = "") -> dict:
        return flat_param_dict(value, prefix=prefix)

    @staticmethod
    def clean_enum_val(data: Any):
        """Checks if ``data`` is an ``Enum`` instance, returning its value.
        Otherwise, returns ``data`` unchanged.
        """
        if isinstance(data, Enum):
            return data.value
        return data
