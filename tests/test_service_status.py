import mws


def test_get_service_status():
    # we can get the service status without needing API credentials
    # this is a simple smoke test to check that the simplest API request can be successfully made
    orders_api = mws.Orders(access_key='', secret_key='', account_id='')
    r = orders_api.get_service_status()
    assert r.response.status_code == 200
