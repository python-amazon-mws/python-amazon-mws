"""Error classes particular to MWS."""


class MWSError(Exception):
    """Main MWS Exception class"""

    # Allows quick access to the response object.
    # Do not rely on this attribute, always check if `is None`.
    response = None
