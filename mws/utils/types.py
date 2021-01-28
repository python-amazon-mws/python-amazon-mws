"""Helpers for complex types used throughout MWS package."""

from typing import List, Union

import mws

MarketplaceEnumOrStr = Union[mws.Marketplaces, str]
StrOrListStr = Union[List[str], str]
