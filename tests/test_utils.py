from mws.mws import calc_md5


def test_calc_md5():
    assert calc_md5(b'mws') == b'mA5nPbh1CSx9M3dbkr3Cyg=='
