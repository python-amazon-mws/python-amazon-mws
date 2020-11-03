"""Utilities for deprecations in the project."""
from functools import wraps
import warnings


class RemovedInPAM10Warning(DeprecationWarning):
    pass


class RemovedInPAM11Warning(PendingDeprecationWarning):
    pass


def kwargs_renamed_for_v11(kwarg_map):
    """Warns of old kwargs from pre-1.0 being used. Notifies the user to call
    the method using new kwargs, and that the old will be removed in v1.1.
    """

    def _decorator(request_func):
        @wraps(request_func)
        def _wrapped_func(self, *args, **kwargs):
            for old, new in kwarg_map:
                if old in kwargs:
                    # An old argument was found; replace it with the new one, warn
                    warnings.warn(
                        (
                            "Argument '%s' in method '%s' has been renamed to '%s'. "
                            "The old name will be removed in v1.1."
                        )
                        % (old, request_func.__name__, new),
                        RemovedInPAM11Warning,
                    )
                    kwargs[new] = kwargs.pop(old)
            return request_func(self, *args, **kwargs)

        return _wrapped_func

    return _decorator
