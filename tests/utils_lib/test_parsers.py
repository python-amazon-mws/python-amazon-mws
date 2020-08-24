"""Testing for parsing wrappers, typically those in ``mws.utils.parsers``."""

import pytest

from requests import Response

from mws import MWSError
from mws.utils import DataWrapper
from mws.utils import DictWrapper
from mws.utils.parsers import MWSResponse, DotDict
from mws.utils.xml import MWS_ENCODING


def mock_mws_response(content):
    response = Response()
    response._content = content
    response.encoding = MWS_ENCODING
    response.status_code = 200
    return response


def test_content_md5_comparison():
    correct_hash = "Zj+Bh1BJ8HzBb9ToK28qFQ=="
    response = Response()
    response._content = b"abc\tdef"
    response.headers["content-md5"] = correct_hash
    # Should raise no error
    MWSResponse(response)


def test_content_md5_check_raises_exception_if_fails():
    incorrect_hash = "notthehash"
    response = Response()
    response._content = b"abc\tdef"
    response.headers["content-md5"] = incorrect_hash
    # Should raise an error due to incorrect hash value.
    with pytest.raises(MWSError):
        MWSResponse(response)


def test_decode_byte_xml():
    """Test that XML decoding works for DictWrapper."""
    # Original XML.
    # Some products and sales rankings removed from the response this originally came from.
    original = b"""<?xml version="1.0"?>
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
                    <AttributeSets>
                        <ns2:ItemAttributes xml:lang="it-IT">
                            <ns2:Binding>Copertina rigida</ns2:Binding>
                            <ns2:Creator Role="Autore">Mizielinska, Aleksandra</ns2:Creator>
                            <ns2:Creator Role="Autore">Mizielinski, Daniel</ns2:Creator>
                            <ns2:Creator Role="Traduttore">Parisi, V.</ns2:Creator>
                            <ns2:ItemDimensions>
                                <ns2:Height Units="inches">14.80312</ns2:Height>
                                <ns2:Length Units="inches">10.86612</ns2:Length>
                                <ns2:Width Units="inches">1.06299</ns2:Width>
                                <ns2:Weight Units="pounds">3.17</ns2:Weight>
                            </ns2:ItemDimensions>
                            <ns2:Label>Mondadori Electa</ns2:Label>
                            <ns2:Languages>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Pubblicato</ns2:Type>
                                </ns2:Language>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Lingua originale</ns2:Type>
                                </ns2:Language>
                            </ns2:Languages>
                            <ns2:ListPrice>
                                <ns2:Amount>25.00</ns2:Amount>
                                <ns2:CurrencyCode>EUR</ns2:CurrencyCode>
                            </ns2:ListPrice>
                            <ns2:Manufacturer>Mondadori Electa</ns2:Manufacturer>
                            <ns2:NumberOfPages>144</ns2:NumberOfPages>
                            <ns2:PackageDimensions>
                                <ns2:Height Units="inches">0.8661417314</ns2:Height>
                                <ns2:Length Units="inches">14.9606299060</ns2:Length>
                                <ns2:Width Units="inches">11.0236220360</ns2:Width>
                                <ns2:Weight Units="pounds">3.1746565728</ns2:Weight>
                            </ns2:PackageDimensions>
                            <ns2:ProductGroup>Libro</ns2:ProductGroup>
                            <ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName>
                            <ns2:PublicationDate>2016-10-25</ns2:PublicationDate>
                            <ns2:Publisher>Mondadori Electa</ns2:Publisher>
                            <ns2:ReleaseDate>2016-10-25</ns2:ReleaseDate>
                            <ns2:SmallImage>
                                <ns2:URL>http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg</ns2:URL>
                                <ns2:Height Units="pixels">75</ns2:Height>
                                <ns2:Width Units="pixels">55</ns2:Width>
                            </ns2:SmallImage>
                            <ns2:Studio>Mondadori Electa</ns2:Studio>
                            <ns2:Title>Mappe. Un atlante per viaggiare tra terra, mari e culture del mondo</ns2:Title>
                        </ns2:ItemAttributes>
                    </AttributeSets>
                    <Relationships/>
                </Product>
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>APJ6JRA9NG5V4</MarketplaceId>
                            <ASIN>8832706571</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                    <AttributeSets>
                        <ns2:ItemAttributes xml:lang="it-IT">
                            <ns2:Binding>Copertina flessibile</ns2:Binding>
                            <ns2:Creator Role="Autore">aa.vv.</ns2:Creator>
                            <ns2:Genre>Diritto</ns2:Genre>
                            <ns2:Label>Neldiritto Editore</ns2:Label>
                            <ns2:Languages>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Pubblicato</ns2:Type>
                                </ns2:Language>
                            </ns2:Languages>
                            <ns2:ListPrice>
                                <ns2:Amount>90.00</ns2:Amount>
                                <ns2:CurrencyCode>EUR</ns2:CurrencyCode>
                            </ns2:ListPrice>
                            <ns2:Manufacturer>Neldiritto Editore</ns2:Manufacturer>
                            <ns2:NumberOfItems>1</ns2:NumberOfItems>
                            <ns2:NumberOfPages>1200</ns2:NumberOfPages>
                            <ns2:PackageDimensions>
                                <ns2:Height Units="inches">3.0708661386</ns2:Height>
                                <ns2:Length Units="inches">9.8425196750</ns2:Length>
                                <ns2:Width Units="inches">6.7716535364</ns2:Width>
                                <ns2:Weight Units="pounds">5.291094288000000881849048</ns2:Weight>
                            </ns2:PackageDimensions>
                            <ns2:ProductGroup>Libro</ns2:ProductGroup>
                            <ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName>
                            <ns2:PublicationDate>2020-01-24</ns2:PublicationDate>
                            <ns2:Publisher>Neldiritto Editore</ns2:Publisher>
                            <ns2:ReleaseDate>2020-01-24</ns2:ReleaseDate>
                            <ns2:SmallImage>
                                <ns2:URL>http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg</ns2:URL>
                                <ns2:Height Units="pixels">75</ns2:Height>
                                <ns2:Width Units="pixels">53</ns2:Width>
                            </ns2:SmallImage>
                            <ns2:Studio>Neldiritto Editore</ns2:Studio>
                            <ns2:Title>Concorso Magistratura 2020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo</ns2:Title>
                        </ns2:ItemAttributes>
                    </AttributeSets>
                    <Relationships/>
                    <SalesRankings>
                        <SalesRank>
                            <ProductCategoryId>book_display_on_website</ProductCategoryId>
                            <Rank>62044</Rank>
                        </SalesRank>
                        <SalesRank>
                            <ProductCategoryId>1346646031</ProductCategoryId>
                            <Rank>617</Rank>
                        </SalesRank>
                        <SalesRank>
                            <ProductCategoryId>1346648031</ProductCategoryId>
                            <Rank>754</Rank>
                        </SalesRank>
                    </SalesRankings>
                </Product>
            </Products>
        </ListMatchingProductsResult>
        <ResponseMetadata>
            <RequestId>d384713e-7c79-4a6d-81cd-d0aa68c7b409</RequestId>
        </ResponseMetadata>
    </ListMatchingProductsResponse>
    """

    # We expect the following DotDict output from `.parsed`
    expected = DotDict(
        {
            "ListMatchingProductsResult": {
                "Products": {
                    "Product": [
                        {
                            "Identifiers": {
                                "MarketplaceASIN": {
                                    "MarketplaceId": "APJ6JRA9NG5V4",
                                    "ASIN": "8891808660",
                                }
                            },
                            "AttributeSets": {
                                "ItemAttributes": {
                                    "@lang": "it-IT",
                                    "Binding": "Copertina rigida",
                                    "Creator": [
                                        {
                                            "#text": "Mizielinska, Aleksandra",
                                            "@Role": "Autore",
                                        },
                                        {
                                            "#text": "Mizielinski, Daniel",
                                            "@Role": "Autore",
                                        },
                                        {"#text": "Parisi, V.", "@Role": "Traduttore"},
                                    ],
                                    "ItemDimensions": {
                                        "Height": {
                                            "#text": "14.80312",
                                            "@Units": "inches",
                                        },
                                        "Length": {
                                            "#text": "10.86612",
                                            "@Units": "inches",
                                        },
                                        "Width": {
                                            "#text": "1.06299",
                                            "@Units": "inches",
                                        },
                                        "Weight": {"#text": "3.17", "@Units": "pounds"},
                                    },
                                    "Label": "Mondadori Electa",
                                    "Languages": {
                                        "Language": [
                                            {"Name": "italian", "Type": "Pubblicato"},
                                            {
                                                "Name": "italian",
                                                "Type": "Lingua originale",
                                            },
                                        ]
                                    },
                                    "ListPrice": {
                                        "Amount": "25.00",
                                        "CurrencyCode": "EUR",
                                    },
                                    "Manufacturer": "Mondadori Electa",
                                    "NumberOfPages": "144",
                                    "PackageDimensions": {
                                        "Height": {
                                            "#text": "0.8661417314",
                                            "@Units": "inches",
                                        },
                                        "Length": {
                                            "#text": "14.9606299060",
                                            "@Units": "inches",
                                        },
                                        "Width": {
                                            "#text": "11.0236220360",
                                            "@Units": "inches",
                                        },
                                        "Weight": {
                                            "#text": "3.1746565728",
                                            "@Units": "pounds",
                                        },
                                    },
                                    "ProductGroup": "Libro",
                                    "ProductTypeName": "ABIS_BOOK",
                                    "PublicationDate": "2016-10-25",
                                    "Publisher": "Mondadori Electa",
                                    "ReleaseDate": "2016-10-25",
                                    "SmallImage": {
                                        "URL": "http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg",
                                        "Height": {"#text": "75", "@Units": "pixels"},
                                        "Width": {"#text": "55", "@Units": "pixels"},
                                    },
                                    "Studio": "Mondadori Electa",
                                    "Title": "Mappe. Un atlante per viaggiare tra terra, mari e culture del mondo",
                                }
                            },
                            "Relationships": None,
                        },
                        {
                            "Identifiers": {
                                "MarketplaceASIN": {
                                    "MarketplaceId": "APJ6JRA9NG5V4",
                                    "ASIN": "8832706571",
                                }
                            },
                            "AttributeSets": {
                                "ItemAttributes": {
                                    "@lang": "it-IT",
                                    "Binding": "Copertina flessibile",
                                    "Creator": {"#text": "aa.vv.", "@Role": "Autore"},
                                    "Genre": "Diritto",
                                    "Label": "Neldiritto Editore",
                                    "Languages": {
                                        "Language": {
                                            "Name": "italian",
                                            "Type": "Pubblicato",
                                        }
                                    },
                                    "ListPrice": {
                                        "Amount": "90.00",
                                        "CurrencyCode": "EUR",
                                    },
                                    "Manufacturer": "Neldiritto Editore",
                                    "NumberOfItems": "1",
                                    "NumberOfPages": "1200",
                                    "PackageDimensions": {
                                        "Height": {
                                            "#text": "3.0708661386",
                                            "@Units": "inches",
                                        },
                                        "Length": {
                                            "#text": "9.8425196750",
                                            "@Units": "inches",
                                        },
                                        "Width": {
                                            "#text": "6.7716535364",
                                            "@Units": "inches",
                                        },
                                        "Weight": {
                                            "#text": "5.291094288000000881849048",
                                            "@Units": "pounds",
                                        },
                                    },
                                    "ProductGroup": "Libro",
                                    "ProductTypeName": "ABIS_BOOK",
                                    "PublicationDate": "2020-01-24",
                                    "Publisher": "Neldiritto Editore",
                                    "ReleaseDate": "2020-01-24",
                                    "SmallImage": {
                                        "URL": "http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg",
                                        "Height": {"#text": "75", "@Units": "pixels"},
                                        "Width": {"#text": "53", "@Units": "pixels"},
                                    },
                                    "Studio": "Neldiritto Editore",
                                    "Title": "Concorso Magistratura 2020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo",
                                }
                            },
                            "Relationships": None,
                            "SalesRankings": {
                                "SalesRank": [
                                    {
                                        "ProductCategoryId": "book_display_on_website",
                                        "Rank": "62044",
                                    },
                                    {"ProductCategoryId": "1346646031", "Rank": "617"},
                                    {"ProductCategoryId": "1346648031", "Rank": "754"},
                                ]
                            },
                        },
                    ]
                }
            },
            "ResponseMetadata": {"RequestId": "d384713e-7c79-4a6d-81cd-d0aa68c7b409"},
        }
    )

    # Get a mock requests.Response object wrapping the content
    response = mock_mws_response(original)

    # Process in our target object
    resp = MWSResponse(response)

    # You may be tempted to test the equality of `.parsed`
    # and wrap `expected` in `DotDict`; but that way lies ruin, I'm afraid.
    # In our current implementation, an equality check using `DotDict` will always
    # return True, even when the results are way off.

    # The easiest method (for now) to compare results is to use the `_dict` attr
    # of our response, which is the native Python dictionary content.
    assert resp.parsed == expected


def test_decode_byte_xml_x94():
    """Check that decoding works with \x94 control characters in output."""

    # Find \x94 control characters hiding in <title> tags
    original = b"""<?xml version="1.0"?>
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
                    <AttributeSets>
                        <ns2:ItemAttributes xml:lang="it-IT">
                            <ns2:Binding>Copertina rigida</ns2:Binding>
                            <ns2:Creator Role="Autore">Mizielinska, Aleksandra</ns2:Creator>
                            <ns2:Creator Role="Autore">Mizielinski, Daniel</ns2:Creator>
                            <ns2:Creator Role="Traduttore">Parisi, V.</ns2:Creator>
                            <ns2:ItemDimensions>
                                <ns2:Height Units="inches">14.80312</ns2:Height>
                                <ns2:Length Units="inches">10.86612</ns2:Length>
                                <ns2:Width Units="inches">1.06299</ns2:Width>
                                <ns2:Weight Units="pounds">3.17</ns2:Weight>
                            </ns2:ItemDimensions>
                            <ns2:Label>Mondadori Electa</ns2:Label>
                            <ns2:Languages>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Pubblicato</ns2:Type>
                                </ns2:Language>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Lingua originale</ns2:Type>
                                </ns2:Language>
                            </ns2:Languages>
                            <ns2:ListPrice>
                                <ns2:Amount>25.00</ns2:Amount>
                                <ns2:CurrencyCode>EUR</ns2:CurrencyCode>
                            </ns2:ListPrice>
                            <ns2:Manufacturer>Mondadori Electa</ns2:Manufacturer>
                            <ns2:NumberOfPages>144</ns2:NumberOfPages>
                            <ns2:PackageDimensions>
                                <ns2:Height Units="inches">0.8661417314</ns2:Height>
                                <ns2:Length Units="inches">14.9606299060</ns2:Length>
                                <ns2:Width Units="inches">11.0236220360</ns2:Width>
                                <ns2:Weight Units="pounds">3.1746565728</ns2:Weight>
                            </ns2:PackageDimensions>
                            <ns2:ProductGroup>Libro</ns2:ProductGroup>
                            <ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName>
                            <ns2:PublicationDate>2016-10-25</ns2:PublicationDate>
                            <ns2:Publisher>Mondadori Electa</ns2:Publisher>
                            <ns2:ReleaseDate>2016-10-25</ns2:ReleaseDate>
                            <ns2:SmallImage>
                                <ns2:URL>http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg</ns2:URL>
                                <ns2:Height Units="pixels">75</ns2:Height>
                                <ns2:Width Units="pixels">55</ns2:Width>
                            </ns2:SmallImage>
                            <ns2:Studio>Mondadori Electa</ns2:Studio>
                            <ns2:Title>Mappe.\x94Un atlante per viaggiare tra terra, mari e culture del mondo</ns2:Title>
                        </ns2:ItemAttributes>
                    </AttributeSets>
                    <Relationships/>
                </Product>
                <Product>
                    <Identifiers>
                        <MarketplaceASIN>
                            <MarketplaceId>APJ6JRA9NG5V4</MarketplaceId>
                            <ASIN>8832706571</ASIN>
                        </MarketplaceASIN>
                    </Identifiers>
                    <AttributeSets>
                        <ns2:ItemAttributes xml:lang="it-IT">
                            <ns2:Binding>Copertina flessibile</ns2:Binding>
                            <ns2:Creator Role="Autore">aa.vv.</ns2:Creator>
                            <ns2:Genre>Diritto</ns2:Genre>
                            <ns2:Label>Neldiritto Editore</ns2:Label>
                            <ns2:Languages>
                                <ns2:Language>
                                    <ns2:Name>italian</ns2:Name>
                                    <ns2:Type>Pubblicato</ns2:Type>
                                </ns2:Language>
                            </ns2:Languages>
                            <ns2:ListPrice>
                                <ns2:Amount>90.00</ns2:Amount>
                                <ns2:CurrencyCode>EUR</ns2:CurrencyCode>
                            </ns2:ListPrice>
                            <ns2:Manufacturer>Neldiritto Editore</ns2:Manufacturer>
                            <ns2:NumberOfItems>1</ns2:NumberOfItems>
                            <ns2:NumberOfPages>1200</ns2:NumberOfPages>
                            <ns2:PackageDimensions>
                                <ns2:Height Units="inches">3.0708661386</ns2:Height>
                                <ns2:Length Units="inches">9.8425196750</ns2:Length>
                                <ns2:Width Units="inches">6.7716535364</ns2:Width>
                                <ns2:Weight Units="pounds">5.291094288000000881849048</ns2:Weight>
                            </ns2:PackageDimensions>
                            <ns2:ProductGroup>Libro</ns2:ProductGroup>
                            <ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName>
                            <ns2:PublicationDate>2020-01-24</ns2:PublicationDate>
                            <ns2:Publisher>Neldiritto Editore</ns2:Publisher>
                            <ns2:ReleaseDate>2020-01-24</ns2:ReleaseDate>
                            <ns2:SmallImage>
                                <ns2:URL>http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg</ns2:URL>
                                <ns2:Height Units="pixels">75</ns2:Height>
                                <ns2:Width Units="pixels">53</ns2:Width>
                            </ns2:SmallImage>
                            <ns2:Studio>Neldiritto Editore</ns2:Studio>
                            <ns2:Title>Concorso Magistratura\x942020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo</ns2:Title>
                        </ns2:ItemAttributes>
                    </AttributeSets>
                    <Relationships/>
                    <SalesRankings>
                        <SalesRank>
                            <ProductCategoryId>book_display_on_website</ProductCategoryId>
                            <Rank>62044</Rank>
                        </SalesRank>
                        <SalesRank>
                            <ProductCategoryId>1346646031</ProductCategoryId>
                            <Rank>617</Rank>
                        </SalesRank>
                        <SalesRank>
                            <ProductCategoryId>1346648031</ProductCategoryId>
                            <Rank>754</Rank>
                        </SalesRank>
                    </SalesRankings>
                </Product>
            </Products>
        </ListMatchingProductsResult>
        <ResponseMetadata>
            <RequestId>d384713e-7c79-4a6d-81cd-d0aa68c7b409</RequestId>
        </ResponseMetadata>
    </ListMatchingProductsResponse>
    """

    # We expect the following dict output from `.parsed`
    # Note the \x94 control characters are still present.
    expected = DotDict(
        {
            "ListMatchingProductsResult": {
                "Products": {
                    "Product": [
                        {
                            "Identifiers": {
                                "MarketplaceASIN": {
                                    "MarketplaceId": "APJ6JRA9NG5V4",
                                    "ASIN": "8891808660",
                                }
                            },
                            "AttributeSets": {
                                "ItemAttributes": {
                                    "@lang": "it-IT",
                                    "Binding": "Copertina rigida",
                                    "Creator": [
                                        {
                                            "@Role": "Autore",
                                            "#text": "Mizielinska, Aleksandra",
                                        },
                                        {
                                            "@Role": "Autore",
                                            "#text": "Mizielinski, Daniel",
                                        },
                                        {"@Role": "Traduttore", "#text": "Parisi, V."},
                                    ],
                                    "ItemDimensions": {
                                        "Height": {
                                            "@Units": "inches",
                                            "#text": "14.80312",
                                        },
                                        "Length": {
                                            "@Units": "inches",
                                            "#text": "10.86612",
                                        },
                                        "Width": {
                                            "@Units": "inches",
                                            "#text": "1.06299",
                                        },
                                        "Weight": {"@Units": "pounds", "#text": "3.17"},
                                    },
                                    "Label": "Mondadori Electa",
                                    "Languages": {
                                        "Language": [
                                            {"Name": "italian", "Type": "Pubblicato"},
                                            {
                                                "Name": "italian",
                                                "Type": "Lingua originale",
                                            },
                                        ]
                                    },
                                    "ListPrice": {
                                        "Amount": "25.00",
                                        "CurrencyCode": "EUR",
                                    },
                                    "Manufacturer": "Mondadori Electa",
                                    "NumberOfPages": "144",
                                    "PackageDimensions": {
                                        "Height": {
                                            "@Units": "inches",
                                            "#text": "0.8661417314",
                                        },
                                        "Length": {
                                            "@Units": "inches",
                                            "#text": "14.9606299060",
                                        },
                                        "Width": {
                                            "@Units": "inches",
                                            "#text": "11.0236220360",
                                        },
                                        "Weight": {
                                            "@Units": "pounds",
                                            "#text": "3.1746565728",
                                        },
                                    },
                                    "ProductGroup": "Libro",
                                    "ProductTypeName": "ABIS_BOOK",
                                    "PublicationDate": "2016-10-25",
                                    "Publisher": "Mondadori Electa",
                                    "ReleaseDate": "2016-10-25",
                                    "SmallImage": {
                                        "URL": "http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg",
                                        "Height": {"@Units": "pixels", "#text": "75"},
                                        "Width": {"@Units": "pixels", "#text": "55"},
                                    },
                                    "Studio": "Mondadori Electa",
                                    "Title": "Mappe.\x94Un atlante per viaggiare tra terra, mari e culture del mondo",
                                }
                            },
                            "Relationships": None,
                        },
                        {
                            "Identifiers": {
                                "MarketplaceASIN": {
                                    "MarketplaceId": "APJ6JRA9NG5V4",
                                    "ASIN": "8832706571",
                                }
                            },
                            "AttributeSets": {
                                "ItemAttributes": {
                                    "@lang": "it-IT",
                                    "Binding": "Copertina flessibile",
                                    "Creator": {"@Role": "Autore", "#text": "aa.vv."},
                                    "Genre": "Diritto",
                                    "Label": "Neldiritto Editore",
                                    "Languages": {
                                        "Language": {
                                            "Name": "italian",
                                            "Type": "Pubblicato",
                                        }
                                    },
                                    "ListPrice": {
                                        "Amount": "90.00",
                                        "CurrencyCode": "EUR",
                                    },
                                    "Manufacturer": "Neldiritto Editore",
                                    "NumberOfItems": "1",
                                    "NumberOfPages": "1200",
                                    "PackageDimensions": {
                                        "Height": {
                                            "@Units": "inches",
                                            "#text": "3.0708661386",
                                        },
                                        "Length": {
                                            "@Units": "inches",
                                            "#text": "9.8425196750",
                                        },
                                        "Width": {
                                            "@Units": "inches",
                                            "#text": "6.7716535364",
                                        },
                                        "Weight": {
                                            "@Units": "pounds",
                                            "#text": "5.291094288000000881849048",
                                        },
                                    },
                                    "ProductGroup": "Libro",
                                    "ProductTypeName": "ABIS_BOOK",
                                    "PublicationDate": "2020-01-24",
                                    "Publisher": "Neldiritto Editore",
                                    "ReleaseDate": "2020-01-24",
                                    "SmallImage": {
                                        "URL": "http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg",
                                        "Height": {"@Units": "pixels", "#text": "75"},
                                        "Width": {"@Units": "pixels", "#text": "53"},
                                    },
                                    "Studio": "Neldiritto Editore",
                                    "Title": "Concorso Magistratura\x942020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo",
                                }
                            },
                            "Relationships": None,
                            "SalesRankings": {
                                "SalesRank": [
                                    {
                                        "ProductCategoryId": "book_display_on_website",
                                        "Rank": "62044",
                                    },
                                    {"ProductCategoryId": "1346646031", "Rank": "617"},
                                    {"ProductCategoryId": "1346648031", "Rank": "754"},
                                ]
                            },
                        },
                    ]
                }
            },
            "ResponseMetadata": {"RequestId": "d384713e-7c79-4a6d-81cd-d0aa68c7b409"},
        }
    )

    # Get a mock requests.Response object wrapping the content
    response = mock_mws_response(original)

    # Process in our target object
    resp = MWSResponse(response)

    # You may be tempted to test the equality of `.parsed`
    # and wrap `expected` in `DotDict`; but that way lies ruin, I'm afraid.
    # In our current implementation, an equality check using `DotDict` will always
    # return True, even when the results are way off.

    # The easiest method (for now) to compare results is to use the `_dict` attr
    # of our response, which is the native Python dictionary content.
    assert resp.parsed == expected


def test_dotdict_assignment():
    """Tests for constructors of DotDict, attr assignment, and updating."""
    dot_dict = DotDict()

    assert bool(dot_dict) is False

    dot_dict.a = "a"
    assert dot_dict["a"] == "a"
    dot_dict["a"] = "b"
    assert dot_dict.a == "b"

    # Assignment of a standard dict should return nested DotDicts,
    # so sub-keys should be accessible with attrs
    dot_dict.b = {"c": {"d": "e"}}
    assert dot_dict.b.c.d == "e"

    # Assigning an empty dict will also convert to a DotDict
    dot_dict.c = {}
    assert isinstance(dot_dict.c, DotDict)
    # by the way, is also an instance of dict
    assert isinstance(dot_dict.c, dict)


def test_dotdict_constructor():
    """The constructor for a ``DotDict`` object."""
    # Update method should work similar to the above
    dot_dict = DotDict(a=3, b=4, c={"d": "e"}, d=DotDict(a=3))
    assert dot_dict.a == 3
    assert dot_dict.b == 4
    assert isinstance(dot_dict.c, DotDict)
    assert isinstance(dot_dict.c, dict)
    assert dot_dict.c.d == "e"
    assert isinstance(dot_dict.d, DotDict)
    assert isinstance(dot_dict.d, dict)
    assert dot_dict.d.a == 3


def test_dotdict_mapping_constructor():
    dot_dict = DotDict({"a": 3, "b": 4, "c": {"d": "e"}, "d": DotDict(a=3)})
    assert dot_dict.a == 3
    assert dot_dict.b == 4
    assert isinstance(dot_dict.c, DotDict)
    assert isinstance(dot_dict.c, dict)
    assert dot_dict.c.d == "e"
    assert isinstance(dot_dict.d, DotDict)
    assert isinstance(dot_dict.d, dict)
    assert dot_dict.d.a == 3


def test_dotdict_item_deletion():
    """Testing of the delattr method in particular."""
    dot_dict = DotDict(a=3)
    assert dot_dict.a == 3
    del dot_dict.a
    assert "a" not in dot_dict

    dot_dict["b"] = 4
    assert dot_dict["b"] == 4
    del dot_dict["b"]
    assert "b" not in dot_dict

    with pytest.raises(KeyError):
        dot_dict.b


def test_dotdict_repr():
    content = {
        "Content": {
            "Item1": "spam",
            "Item2": {"Details": "ham", "Inner": {"Something": "eggs"}},
        }
    }

    dot_dict = DotDict(content)

    dot_dict_repr = repr(dot_dict)
    expected = (
        "DotDict({'Content': DotDict({'Item1': 'spam', 'Item2': "
        "DotDict({'Details': 'ham', 'Inner': DotDict({'Something': 'eggs'})})})})"
    )
    assert expected == dot_dict_repr


def test_dotdict_iteration():
    # Iteration of a single item:
    # fmt: off
    dot_dict1 = DotDict({
        "Products": {
            "Product": {"Name": "foo"}
        }
    })
    # fmt: on

    for product in dot_dict1.Products.Product:
        assert isinstance(product, DotDict)
        assert "Name" in product

    # The above should be an identical interface to the below,
    # in which ``Product`` is a list of DotDicts with the same
    # type of content.
    # This matches up with how ``xmltodict`` might process a response
    # that may have one or more sibling tags of the same names (``Product``).
    # fmt: off
    dot_dict2 = DotDict({
        "Products": {
            "Product": [
                {"Name": "bar"},
                {"Name": "baz"}
            ]
        }
    })
    # fmt: on

    for product in dot_dict2.Products.Product:
        assert isinstance(product, DotDict)
        assert "Name" in product


def test_dotdict_update():
    """``DotDict.update`` method."""
    dot_dict = DotDict()
    dot_dict.update(a=3, b=4, c={"d": "e"}, d=DotDict(a=3))
    assert dot_dict.a == 3
    assert dot_dict.b == 4
    assert isinstance(dot_dict.c, DotDict)
    assert isinstance(dot_dict.c, dict)
    assert dot_dict.c.d == "e"
    assert isinstance(dot_dict.d, DotDict)
    assert isinstance(dot_dict.d, dict)
    assert dot_dict.d.a == 3


def test_dotdict_attr_key_access_methods():
    """Various methods for accessing contents of a parsed XML response
    should all return the same way.

    - dotted attribute access
    - using dict keys
    - using `DotDict.get` (an overwrite of `dict.get`)
    - `values` containing just newlines and spaces ('\n    ') should be stripped
      and not exist at all.
    """

    content = {
        "Content": {
            "Item1": "spam",
            "Item2": {"Details": "ham", "Inner": {"Something": "eggs"}},
        }
    }

    dot_dict = DotDict(content)

    # The `in` operator should work.
    assert "Content" in dot_dict
    # Access to the attr should be the same as access to the key
    assert dot_dict.Content is dot_dict.get("Content")
    assert dot_dict.Content is dot_dict["Content"]

    # The type of a child mapping should also be DotDict
    assert isinstance(dot_dict.Content.Item2, DotDict)

    # `.keys` should work similar to a standard dict
    assert isinstance(dot_dict.Content.keys(), type(dict().keys()))

    # as should `.values()`
    assert isinstance(dot_dict.Content.values(), type(dict().values()))

    # Contents of `.items()` should work similar to a standard dict
    for key, val in dot_dict.Content.items():
        assert dot_dict.Content[key] == getattr(dot_dict.Content, key)
        assert val == dot_dict.Content[key]
        # Values should be returned as the same type as accessing them from the dict
        assert isinstance(val, type(dot_dict.Content[key]))
        assert isinstance(val, type(getattr(dot_dict.Content, key)))

    # Accessing deeper contents should work just the same
    assert dot_dict.Content.Item1 == "spam"
    assert dot_dict.Content.get("Item1") == "spam"
    assert dot_dict.Content["Item1"] == "spam"

    # .get with a default should work the same as with a dict
    assert dot_dict.Content.Item2.get("NotHere") is None
    assert dot_dict.Content.Item2.get("NotHere", "what") == "what"

    # looking for an attr not existing will pass to getitem, so will raise KeyError
    with pytest.raises(KeyError):
        dot_dict.Content.Item2.NotHere


def test_dotdict_attr_fallback_keys():
    """Checks our special case fallback methods for accessing keys in DotDict.

    ``xmltodict`` converts tag attributes to a key starting with ``@``.
    Further, tags with attributes and no child tags present their text content
    as a new key, ``#text``.

    These types of keys cannot be accessed directly as attrs due to Python syntax,
    so we provide a fallback that tries to access those key names without
    ``@`` or ``#`` included.
    """
    content = {
        "Something": {
            "@Attr1": "spam",
            "ChildTag": {"@Attr2": "ham", "#text": "eggs"},
            "Conflicting": "foo",
            "@Conflicting": "bar",
            "#Conflicting": "baz",
        }
    }

    dot_dict = DotDict(content)

    # The special key ``@Attr1`` should be accessible as an attribute without ``@``
    assert dot_dict.Something.Attr1 == "spam"
    assert dot_dict.Something["@Attr1"] == "spam"
    assert dot_dict.Something.get("@Attr1") == "spam"

    # Same for the child node's attr.
    assert dot_dict.Something.ChildTag.Attr2 == "ham"
    assert dot_dict.Something.ChildTag["@Attr2"] == "ham"
    assert dot_dict.Something.ChildTag.get("@Attr2") == "ham"

    # and for the child node's text content.
    assert dot_dict.Something.ChildTag.text == "eggs"
    assert dot_dict.Something.ChildTag["#text"] == "eggs"
    assert dot_dict.Something.ChildTag.get("#text") == "eggs"

    # In the case of a conflict, a key with no '@' or '#' takes precedence
    assert dot_dict.Something.Conflicting == "foo"
    assert dot_dict.Something["@Conflicting"] == "bar"
    assert dot_dict.Something["#Conflicting"] == "baz"

    # As expected without this fallback, a missing key raises KeyError
    with pytest.raises(KeyError):
        dot_dict.Something.NonExistent
