"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod
from typing import Iterable, Mapping, Union

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
