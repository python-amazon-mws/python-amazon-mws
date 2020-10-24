import datetime

import pytest

from requests import Response

from mws.mws import MWS
from mws.utils.xml import MWS_ENCODING
from mws.response import MWSResponse


TEST_MWS_ACCESS_KEY = "my_access_key"
TEST_MWS_SECRET_KEY = "my_secret_key"
TEST_MWS_ACCOUNT_ID = "my_account_id"
TEST_MWS_AUTH_TOKEN = "my_auth_token"


@pytest.fixture
def mws_credentials():
    """Fake set of MWS credentials"""
    return {
        "access_key": TEST_MWS_ACCESS_KEY,
        "secret_key": TEST_MWS_SECRET_KEY,
        "account_id": TEST_MWS_ACCOUNT_ID,
        "auth_token": TEST_MWS_AUTH_TOKEN,
    }


@pytest.fixture
def api_instance(request, mws_credentials):
    """Create an API instance ready for request param testing.
    If called in a class that includes an `api_class` attribute,
    uses the class defined there.
    Otherwise defaults to MWS base class.
    """
    klass = getattr(request.cls, "api_class", MWS)
    instance = klass(**mws_credentials)
    instance._test_request_params = True
    return instance


@pytest.fixture
def simple_xml_response_str():
    return """<?xml version="1.0"?>
    <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <ListMatchingProductsResult>
            <Products xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>APJ6JRA9NG5V4</MarketplaceId>
                            <ASIN>8891808660</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                </Product>
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>SomeOtherMarketplaceId</MarketplaceId>
                            <ASIN>7780797559</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                </Product>
            </Products>
        </ListMatchingProductsResult>
        <ResponseMetadata>
            <RequestId>d384713e-7c79-4a6d-81cd-d0aa68c7b409</RequestId>
        </ResponseMetadata>
    </ListMatchingProductsResponse>
    """


@pytest.fixture
def simple_xml_response_no_meta():
    return """<?xml version="1.0"?>
    <ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01">
        <ListMatchingProductsResult>
            <Products xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd">
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>APJ6JRA9NG5V4</MarketplaceId>
                            <ASIN>8891808660</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                </Product>
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>SomeOtherMarketplaceId</MarketplaceId>
                            <ASIN>7780797559</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                </Product>
            </Products>
        </ListMatchingProductsResult>
    </ListMatchingProductsResponse>
    """


def mock_response(content):
    response = Response()
    response._content = content
    response.encoding = MWS_ENCODING
    response.status_code = 200
    return response


@pytest.fixture
def simple_mwsresponse(simple_xml_response_str):
    content = simple_xml_response_str.encode(MWS_ENCODING)
    response = mock_response(content)
    return MWSResponse(response)


@pytest.fixture
def simple_mwsresponse_with_resultkey(simple_xml_response_str):
    content = simple_xml_response_str.encode(MWS_ENCODING)
    response = mock_response(content)
    return MWSResponse(response, result_key="ListMatchingProductsResult")


@pytest.fixture
def simple_mwsresponse_no_metadata(simple_xml_response_no_meta):
    content = simple_xml_response_no_meta.encode(MWS_ENCODING)
    response = mock_response(content)
    return MWSResponse(response)


@pytest.fixture
def simple_mwsresponse_with_timestamp(simple_mwsresponse_with_resultkey):
    timestamp = datetime.datetime(2020, 8, 24, 16, 30)  # 4:30PM (naive), 2020-08-24
    mws_response = simple_mwsresponse_with_resultkey
    mws_response.timestamp = timestamp
    return mws_response
