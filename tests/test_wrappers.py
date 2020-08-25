import pytest
from mws.mws import DataWrapper, DictWrapper, MWSError


def test_content_md5_comparison():
    data = b'abc\tdef'
    hash = 'Zj+Bh1BJ8HzBb9ToK28qFQ=='
    DataWrapper(data, {'content-md5': hash})


def test_content_md5_check_raises_exception_if_fails():
    data = b'abc\tdef'
    hash = 'notthehash'
    with pytest.raises(MWSError):
        DataWrapper(data, {'content-md5': hash})


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

    # Clean out the spacing used above, matching the output we expected from MWS
    intermediate = original.decode("iso-8859-1").split("\n")
    stripped = "".join([x.strip() for x in intermediate])
    stripped_original = stripped.encode("iso-8859-1")

    # We expect the following dict output from `.parsed`
    expected = {
        "ListMatchingProductsResult": {
            "Products": {
                "Product": [
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8891808660"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Creator": [
                                    {
                                        "value": "Mizielinska, Aleksandra",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Mizielinski, Daniel",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Parisi, V.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "14.80312",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "10.86612",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.06299",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.17",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "Label": {"value": "Mondadori Electa"},
                                "Languages": {
                                    "Language": [
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Lingua originale"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "25.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Mondadori Electa"},
                                "NumberOfPages": {"value": "144"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.8661417314",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "14.9606299060",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "11.0236220360",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.1746565728",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2016-10-25"},
                                "Publisher": {"value": "Mondadori Electa"},
                                "ReleaseDate": {"value": "2016-10-25"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "55",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Mondadori Electa"},
                                "Title": {
                                    "value": "Mappe. Un atlante per viaggiare tra terra, mari e culture del mondo"
                                },
                            }
                        },
                        "Relationships": {},
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8832706571"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Creator": {
                                    "value": "aa.vv.",
                                    "Role": {"value": "Autore"},
                                },
                                "Genre": {"value": "Diritto"},
                                "Label": {"value": "Neldiritto Editore"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "90.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Neldiritto Editore"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "1200"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "3.0708661386",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "9.8425196750",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.7716535364",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "5.291094288000000881849048",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-01-24"},
                                "Publisher": {"value": "Neldiritto Editore"},
                                "ReleaseDate": {"value": "2020-01-24"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "53",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Neldiritto Editore"},
                                "Title": {
                                    "value": "Concorso Magistratura 2020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo"
                                },
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "62044"},
                                },
                                {
                                    "ProductCategoryId": {"value": "1346646031"},
                                    "Rank": {"value": "617"},
                                },
                                {
                                    "ProductCategoryId": {"value": "1346648031"},
                                    "Rank": {"value": "754"},
                                },
                            ]
                        },
                    },
                ]
            }
        },
        "ResponseMetadata": {
            "RequestId": {"value": "d384713e-7c79-4a6d-81cd-d0aa68c7b409"}
        },
    }

    # Process and assert
    output = DictWrapper(stripped_original)
    assert output.parsed == expected


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

    # Clean out the spacing used above, matching the output we expected from MWS
    intermediate = original.decode("iso-8859-1").split("\n")
    stripped = "".join([x.strip() for x in intermediate])
    stripped_original = stripped.encode("iso-8859-1")

    # We expect the following dict output from `.parsed`
    # Note the \x94 control characters are still present.
    expected = {
        "ListMatchingProductsResult": {
            "Products": {
                "Product": [
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8891808660"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Creator": [
                                    {
                                        "value": "Mizielinska, Aleksandra",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Mizielinski, Daniel",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Parisi, V.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "14.80312",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "10.86612",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.06299",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.17",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "Label": {"value": "Mondadori Electa"},
                                "Languages": {
                                    "Language": [
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Lingua originale"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "25.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Mondadori Electa"},
                                "NumberOfPages": {"value": "144"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.8661417314",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "14.9606299060",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "11.0236220360",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.1746565728",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2016-10-25"},
                                "Publisher": {"value": "Mondadori Electa"},
                                "ReleaseDate": {"value": "2016-10-25"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "55",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Mondadori Electa"},
                                "Title": {
                                    "value": "Mappe.\x94Un atlante per viaggiare tra terra, mari e culture del mondo"
                                },
                            }
                        },
                        "Relationships": {},
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8832706571"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Creator": {
                                    "value": "aa.vv.",
                                    "Role": {"value": "Autore"},
                                },
                                "Genre": {"value": "Diritto"},
                                "Label": {"value": "Neldiritto Editore"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "90.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Neldiritto Editore"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "1200"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "3.0708661386",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "9.8425196750",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.7716535364",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "5.291094288000000881849048",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-01-24"},
                                "Publisher": {"value": "Neldiritto Editore"},
                                "ReleaseDate": {"value": "2020-01-24"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "53",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Neldiritto Editore"},
                                "Title": {
                                    "value": "Concorso Magistratura\x942020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo"
                                },
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "62044"},
                                },
                                {
                                    "ProductCategoryId": {"value": "1346646031"},
                                    "Rank": {"value": "617"},
                                },
                                {
                                    "ProductCategoryId": {"value": "1346648031"},
                                    "Rank": {"value": "754"},
                                },
                            ]
                        },
                    },
                ]
            }
        },
        "ResponseMetadata": {
            "RequestId": {"value": "d384713e-7c79-4a6d-81cd-d0aa68c7b409"}
        },
    }

    # Process and assert
    output = DictWrapper(stripped_original)
    assert output.parsed == expected
