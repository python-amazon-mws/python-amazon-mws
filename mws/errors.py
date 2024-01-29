"""Error classes particular to MWS."""

from requests import HTTPError


class MWSError(Exception):
    """Main MWS Exception class"""

    pass


class MWSRequestError(MWSError, HTTPError):
    """Main MWS Request Exception class"""

    def __init__(self, err):
        args = err.args
        kwargs = vars(err)

        super().__init__(*args, **kwargs)

        if self.response is not None:
            headers = self.response.headers
            self.request_id = headers.get("x-mws-request-id")
            self.timestamp = headers.get("x-mws-timestamp")
