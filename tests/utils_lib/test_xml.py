"""Tests for ``utils.xml`` module."""

import pytest

from mws.utils.xml import mws_xml_to_dict
from mws.utils.xml import mws_xml_to_dotdict
from mws.utils.collections import DotDict


def test_mws_xml_to_dict_method(simple_xml_response_str):
    output = mws_xml_to_dict(simple_xml_response_str)
    assert isinstance(output, dict)
    product = output["ListMatchingProductsResult"]["Products"]["Product"]
    asin_identifier = product[0]["Identifiers"]["MarketplaceASIN"]
    assert asin_identifier["MarketplaceId"] == "APJ6JRA9NG5V4"
    assert asin_identifier["ASIN"] == "8891808660"

    request_id = output["ResponseMetadata"]["RequestId"]
    assert request_id == "d384713e-7c79-4a6d-81cd-d0aa68c7b409"


def test_mws_xml_to_dotdict_method(simple_xml_response_str):
    output = mws_xml_to_dotdict(simple_xml_response_str)
    assert isinstance(output, DotDict)
    assert isinstance(output, dict)
    identifiers = output.ListMatchingProductsResult.Products.Product[0].Identifiers
    assert identifiers.MarketplaceASIN.MarketplaceId == "APJ6JRA9NG5V4"
    assert identifiers.MarketplaceASIN.ASIN == "8891808660"

    request_id = output.ResponseMetadata.RequestId
    assert request_id == "d384713e-7c79-4a6d-81cd-d0aa68c7b409"


def test_mws_xml_to_dotdict_resultkey(simple_xml_response_str):
    output = mws_xml_to_dotdict(
        simple_xml_response_str, result_key="ListMatchingProductsResult"
    )
    assert isinstance(output, DotDict)
    assert isinstance(output, dict)

    assert "ListMatchingProductsResult" not in output
    assert "ResponseMetadata" not in output

    identifiers = output.Products.Product[0].Identifiers
    assert identifiers.MarketplaceASIN.MarketplaceId == "APJ6JRA9NG5V4"
    assert identifiers.MarketplaceASIN.ASIN == "8891808660"
