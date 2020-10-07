"""Base models for datatypes used in MWS."""


class MWSDataType:
    def to_dict(self) -> dict:
        """Must be initialized on subclass."""
        raise NotImplementedError
