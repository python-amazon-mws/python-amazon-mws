import pytest

from mws.mws import MWS
from mws.utils.deprecation import RemovedInPAM10Warning


def test_mws_enumerate_params_method_removed(mws_credentials):
    mws = MWS(**mws_credentials)
    with pytest.warns(RemovedInPAM10Warning):
        mws.enumerate_param("Something", [1, 2, 3])
