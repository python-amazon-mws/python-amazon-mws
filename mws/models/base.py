"""Base models for datatypes used in MWS."""

from abc import ABC, abstractmethod
from typing import Any, Iterable, List, Mapping, Union
from enum import Enum

from mws.errors import MWSError
from mws.utils import flat_param_dict


class MWSDataType(ABC):
    """Base class for data type models used for MWS requests."""

    operations_permitted = []
    """List containing Action names of operations this model is intended to be used for.
    Request methods that use this model can opt-in to check that the operation they use
    is permitted by running `self.raise_for_operation_mismatch` with the "Action" name
    of that operation.
    """

    def __repr__(self):
        values = ", ".join(f"{k}={repr(v)}" for k, v in self.__dict__.items())

        return f"<{self.__class__.__name__}({values})>"

    @abstractmethod
    def params_dict(self) -> dict:
        """Returns a dict of this model's parameters suitable for an MWS request.

        :meta private:
        """
        pass

    def to_params(self, prefix: str = "") -> dict:
        """Flattens all parameters and values of this model into a single key-value
        dictionary, suitable for use in a request to MWS.
        """
        params_dict = self.params_dict()
        return flat_param_dict(params_dict, prefix=prefix)

    @property
    def operations_permitted_lower(self) -> List[str]:
        """Returns list of permitted ops, all lowercase for case-insensitive testing.

        :meta private:
        """
        return [x.lower() for x in self.operations_permitted]

    def raise_for_operation_mismatch(self, operation: str = None):
        """Check that ``operation`` matches one of the Actions permitted for this model.

        This check will pass silently if:

        1. The operation is found in this model's ``operations_permitted`` list,
           as a case-insensitive string matching the Action name of the operation,
           i.e. "SubmitFeed" (NOT the name of the Python method, i.e. "submit_feed");
        2. This model's ``operations_permitted`` list is empty; OR
        3. ``operation`` is ``None``.

        For any other scenario - where ``operations_permitted`` contains at least
        one operation name and ``operation`` does not match any of its members -
        raises MWSError.

        :meta private:
        """
        if not self.operations_permitted or operation is None:
            # Silent pass; undefined list of ops or no op given
            return
        if operation.lower() not in self.operations_permitted_lower:
            op_list_str = ", ".join(self.operations_permitted)
            raise MWSError(
                ("Model %s not permitted for operation %s (allowed in operations: %s)")
                % (self.__class__.__name__, operation, op_list_str)
            )

    @staticmethod
    def flat_param_dict(value: Union[str, Mapping, Iterable], prefix: str = "") -> dict:
        """Simple access to ``flat_param_dict`` from any subclass of this model base.

        :meta private:
        """
        return flat_param_dict(value, prefix=prefix)
