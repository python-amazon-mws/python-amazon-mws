"""Decorator methods for MWS module."""
from functools import wraps


def next_token_action(action_name):
    """Decorator that designates an action as having a "...ByNextToken" associated request.
    Checks for a `next_token` kwargs in the request and, if present, redirects the call
    to `action_by_next_token` using the given `action_name`.

    Only the `next_token` kwarg is consumed by the "next" call:
    all other args and kwargs are ignored and not required.
    """

    def _decorator(request_func):
        @wraps(request_func)
        def _wrapped_func(self, *args, **kwargs):
            next_token = kwargs.pop("next_token", None)
            if next_token is not None:
                # Token captured: run the "next" action.
                return self.action_by_next_token(action_name, next_token)
            return request_func(self, *args, **kwargs)

        return _wrapped_func

    return _decorator
