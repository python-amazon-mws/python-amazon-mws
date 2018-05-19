import mws


def test_get_service_status(credentials):
    # we can get the service status without needing API credentials
    # this is a simple smoke test to check that the simplest API request can be successfully made
    orders_api = mws.Orders(**credentials)
    r = orders_api.get_service_status()
    assert r.response.status_code == 200
