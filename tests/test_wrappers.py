import pytest
from mws import MWSError
from mws.mws import DataWrapper
from mws.mws import DictWrapper


def test_content_md5_comparison():
    data = b"abc\tdef"
    hash = "Zj+Bh1BJ8HzBb9ToK28qFQ=="
    DataWrapper(data, {"content-md5": hash})


def test_content_md5_check_raises_exception_if_fails():
    data = b"abc\tdef"
    hash = "notthehash"
    with pytest.raises(MWSError):
        DataWrapper(data, {"content-md5": hash})


def test_decode_byte_xml():
    xml = b'<?xml version="1.0"?><ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"><ListMatchingProductsResult><Products xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd"><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8891808660</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Creator Role="Autore">Mizielinska, Aleksandra</ns2:Creator><ns2:Creator Role="Autore">Mizielinski, Daniel</ns2:Creator><ns2:Creator Role="Traduttore">Parisi, V.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">14.80312</ns2:Height><ns2:Length Units="inches">10.86612</ns2:Length><ns2:Width Units="inches">1.06299</ns2:Width><ns2:Weight Units="pounds">3.17</ns2:Weight></ns2:ItemDimensions><ns2:Label>Mondadori Electa</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>25.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Mondadori Electa</ns2:Manufacturer><ns2:NumberOfPages>144</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.8661417314</ns2:Height><ns2:Length Units="inches">14.9606299060</ns2:Length><ns2:Width Units="inches">11.0236220360</ns2:Width><ns2:Weight Units="pounds">3.1746565728</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2016-10-25</ns2:PublicationDate><ns2:Publisher>Mondadori Electa</ns2:Publisher><ns2:ReleaseDate>2016-10-25</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">55</ns2:Width></ns2:SmallImage><ns2:Studio>Mondadori Electa</ns2:Studio><ns2:Title>Mappe. Un atlante per viaggiare tra terra, mari e culture del mondo</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>2843</Rank></SalesRank><SalesRank><ProductCategoryId>13064701031</ProductCategoryId><Rank>2</Rank></SalesRank><SalesRank><ProductCategoryId>13077570031</ProductCategoryId><Rank>2</Rank></SalesRank><SalesRank><ProductCategoryId>13064711031</ProductCategoryId><Rank>15</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8858014308</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>Passioni</ns2:Brand><ns2:Creator Role="Autore">Brotton, Jerry</ns2:Creator><ns2:Creator Role="Traduttore">Fontebuoni, A.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">10.31494</ns2:Height><ns2:Length Units="inches">12.20470</ns2:Length><ns2:Width Units="inches">0.86614</ns2:Width></ns2:ItemDimensions><ns2:Label>Gribaudo</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>24.90</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Gribaudo</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>256</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.1023622036</ns2:Height><ns2:Length Units="inches">12.1653543183</ns2:Length><ns2:Width Units="inches">10.2362204620</ns2:Width><ns2:Weight Units="pounds">3.4392112872</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2015-11-05</ns2:PublicationDate><ns2:Publisher>Gribaudo</ns2:Publisher><ns2:ReleaseDate>2015-11-05</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61UmGSV5reL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">62</ns2:Width></ns2:SmallImage><ns2:Studio>Gribaudo</ns2:Studio><ns2:Title>Le grandi mappe. Oltre 60 capolavori raccontano l\'evoluzione dell\'uomo, la sua storia e la sua cultura. Ediz. illustrata</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>23519</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>40</Rank></SalesRank><SalesRank><ProductCategoryId>508856031</ProductCategoryId><Rank>452</Rank></SalesRank><SalesRank><ProductCategoryId>508758031</ProductCategoryId><Rank>3211</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8807890283</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Brand>UNIVERSALE ECONOMICA. SAGGI</ns2:Brand><ns2:Creator Role="Autore">Brotton, Jerry</ns2:Creator><ns2:Creator Role="Traduttore">Sala, V. B.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">5.47243</ns2:Height><ns2:Length Units="inches">8.77951</ns2:Length><ns2:Width Units="inches">1.49606</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Feltrinelli</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>19.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Feltrinelli</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>526</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.59842519522</ns2:Height><ns2:Length Units="inches">8.7007873927</ns2:Length><ns2:Width Units="inches">5.49999999439</ns2:Width><ns2:Weight Units="pounds">1.6755131912</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2017-11-23</ns2:PublicationDate><ns2:Publisher>Feltrinelli</ns2:Publisher><ns2:ReleaseDate>2017-11-23</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61jo5I7vBjL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">48</ns2:Width></ns2:SmallImage><ns2:Studio>Feltrinelli</ns2:Studio><ns2:Title>La storia del mondo in dodici mappe</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>18925</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>34</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8811149843</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>SAGGI</ns2:Brand><ns2:Creator Role="Autore">Wilford, John Noble</ns2:Creator><ns2:Creator Role="Traduttore">Gianna Lonza</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.97636</ns2:Height><ns2:Length Units="inches">6.69290</ns2:Length><ns2:Width Units="inches">1.41732</ns2:Width></ns2:ItemDimensions><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>30.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>478</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4960629906</ns2:Height><ns2:Length Units="inches">8.7401574714</ns2:Length><ns2:Width Units="inches">6.2992125920</ns2:Width><ns2:Weight Units="pounds">1.4991433816</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2018-11-22</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2018-11-22</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61KTEY8nMgL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">54</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>I signori delle mappe. La storia avventurosa dell\'invenzione della cartografia</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>23845</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>41</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>B084FZWQHD</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Creator Role="Autore">Frasante, Marco</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.5</ns2:Height><ns2:Length Units="inches">5.5</ns2:Length><ns2:Width Units="inches">0.2</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Independently published</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Sconosciuto</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>12.69</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Independently published</ns2:Manufacturer><ns2:NumberOfPages>87</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.2</ns2:Height><ns2:Length Units="inches">8.5</ns2:Length><ns2:Width Units="inches">5.5</ns2:Width><ns2:Weight Units="pounds">0.37</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-02-09</ns2:PublicationDate><ns2:Publisher>Independently published</ns2:Publisher><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51Na9vFKvgL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">49</ns2:Width></ns2:SmallImage><ns2:Studio>Independently published</ns2:Studio><ns2:Title>Mappe Mentali e Mappe Concettuali: La Guida Pi\xc3\xb9 Completa Per Memorizzare e Apprendere Qualsiasi Cosa In Modo Semplice e Veloce</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>2663</Rank></SalesRank><SalesRank><ProductCategoryId>508885031</ProductCategoryId><Rank>192</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>881160771X</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>SAGGI</ns2:Brand><ns2:Creator Role="Autore">Marshall, Tim</ns2:Creator><ns2:Creator Role="Illustratore">Easton, G.</ns2:Creator><ns2:Creator Role="Illustratore">Smith, J.</ns2:Creator><ns2:Creator Role="Illustratore">Hawkins, E.</ns2:Creator><ns2:Creator Role="Illustratore">Crane, P.</ns2:Creator><ns2:Creator Role="Traduttore">Caraffini, S.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">12.40155</ns2:Height><ns2:Length Units="inches">10.03935</ns2:Length><ns2:Width Units="inches">0.59055</ns2:Width></ns2:ItemDimensions><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>20.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>80</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.5511811018</ns2:Height><ns2:Length Units="inches">12.2047243970</ns2:Length><ns2:Width Units="inches">9.8425196750</ns2:Width><ns2:Weight Units="pounds">1.6975594174</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-02-13</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2020-02-13</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/514B0NG7gvL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">57</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>Le 12 mappe che spiegano il mondo ai ragazzi</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>24610</Rank></SalesRank><SalesRank><ProductCategoryId>13064684031</ProductCategoryId><Rank>7</Rank></SalesRank><SalesRank><ProductCategoryId>13064569031</ProductCategoryId><Rank>35</Rank></SalesRank><SalesRank><ProductCategoryId>13077656031</ProductCategoryId><Rank>35</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>881167378X</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Creator Role="Autore">Marshall, Tim</ns2:Creator><ns2:Creator Role="Traduttore">Merlini, R.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.77951</ns2:Height><ns2:Length Units="inches">5.66928</ns2:Length><ns2:Width Units="inches">1.37795</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>19.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>313</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4960629906</ns2:Height><ns2:Length Units="inches">8.5826771566</ns2:Length><ns2:Width Units="inches">5.7086614115</ns2:Width><ns2:Weight Units="pounds">1.1904962148</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2017-06-08</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2017-06-08</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51DYJDPBKmL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">50</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>Le 10 mappe che spiegano il mondo</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>35380</Rank></SalesRank><SalesRank><ProductCategoryId>508819031</ProductCategoryId><Rank>197</Rank></SalesRank><SalesRank><ProductCategoryId>508812031</ProductCategoryId><Rank>678</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8804712279</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>LE SCIE. NUOVA SERIE STRANIERI</ns2:Brand><ns2:Creator Role="Autore">Moller, Violet</ns2:Creator><ns2:Creator Role="Traduttore">Vanni, L.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">9.44880</ns2:Height><ns2:Length Units="inches">6.69290</ns2:Length><ns2:Width Units="inches">1.18110</ns2:Width></ns2:ItemDimensions><ns2:Label>Mondadori</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>22.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Mondadori</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>325</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4173228332</ns2:Height><ns2:Length Units="inches">9.4488188880</ns2:Length><ns2:Width Units="inches">6.4960629855</ns2:Width><ns2:Weight Units="pounds">1.543235834</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2019-05-28</ns2:PublicationDate><ns2:Publisher>Mondadori</ns2:Publisher><ns2:ReleaseDate>2019-05-28</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51ntMunIvhL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">50</ns2:Width></ns2:SmallImage><ns2:Studio>Mondadori</ns2:Studio><ns2:Title>La mappa dei libri perduti. Come la conoscenza antica \xc3\xa8 stata perduta e ritrovata: una storia in sette citt\xc3\xa0</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>63759</Rank></SalesRank><SalesRank><ProductCategoryId>508810031</ProductCategoryId><Rank>692</Rank></SalesRank><SalesRank><ProductCategoryId>508879031</ProductCategoryId><Rank>15957</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>B008RJFRTK</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>App</ns2:Binding><ns2:Brand>MY.COM</ns2:Brand><ns2:HardwarePlatform>Android</ns2:HardwarePlatform><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>MY.COM</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>arabic</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>chinese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>czech</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>dutch</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>english</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>french</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>german</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>japanese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>korean</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>polish</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>portuguese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>russian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>spanish</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>vietnamese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>0.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>MY.COM</ns2:Manufacturer><ns2:OperatingSystem>Android</ns2:OperatingSystem><ns2:PartNumber>com.mapswithme.maps.pro</ns2:PartNumber><ns2:ProductGroup>Mobile Application</ns2:ProductGroup><ns2:ProductTypeName>MOBILE_APPLICATION</ns2:ProductTypeName><ns2:Publisher>MY.COM</ns2:Publisher><ns2:ReleaseDate>2016-01-14</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61KevuswqEL._SL75_.png</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">75</ns2:Width></ns2:SmallImage><ns2:Studio>MY.COM</ns2:Studio><ns2:Title>MAPS.ME \xe2\x80\x94 Mappe Offline</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings/></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8832706571</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Creator Role="Autore">aa.vv.</ns2:Creator><ns2:Genre>Diritto</ns2:Genre><ns2:Label>Neldiritto Editore</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>90.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Neldiritto Editore</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>1200</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">3.0708661386</ns2:Height><ns2:Length Units="inches">9.8425196750</ns2:Length><ns2:Width Units="inches">6.7716535364</ns2:Width><ns2:Weight Units="pounds">5.291094288000000881849048</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-01-24</ns2:PublicationDate><ns2:Publisher>Neldiritto Editore</ns2:Publisher><ns2:ReleaseDate>2020-01-24</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">53</ns2:Width></ns2:SmallImage><ns2:Studio>Neldiritto Editore</ns2:Studio><ns2:Title>Concorso Magistratura 2020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>62044</Rank></SalesRank><SalesRank><ProductCategoryId>1346646031</ProductCategoryId><Rank>617</Rank></SalesRank><SalesRank><ProductCategoryId>1346648031</ProductCategoryId><Rank>754</Rank></SalesRank></SalesRankings></Product></Products></ListMatchingProductsResult><ResponseMetadata><RequestId>d384713e-7c79-4a6d-81cd-d0aa68c7b409</RequestId></ResponseMetadata></ListMatchingProductsResponse>'
    expected_json = {
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
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "2843"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064701031"},
                                    "Rank": {"value": "2"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13077570031"},
                                    "Rank": {"value": "2"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064711031"},
                                    "Rank": {"value": "15"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8858014308"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "Passioni"},
                                "Creator": [
                                    {
                                        "value": "Brotton, Jerry",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Fontebuoni, A.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "10.31494",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.20470",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.86614",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Gribaudo"},
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
                                    "Amount": {"value": "24.90"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Gribaudo"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "256"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.1023622036",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.1653543183",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "10.2362204620",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.4392112872",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2015-11-05"},
                                "Publisher": {"value": "Gribaudo"},
                                "ReleaseDate": {"value": "2015-11-05"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61UmGSV5reL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "62",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Gribaudo"},
                                "Title": {
                                    "value": "Le grandi mappe. Oltre 60 capolavori raccontano l'evoluzione dell'uomo, la sua storia e la sua cultura. Ediz. illustrata"
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
                                    "Rank": {"value": "23519"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "40"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508856031"},
                                    "Rank": {"value": "452"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508758031"},
                                    "Rank": {"value": "3211"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8807890283"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Brand": {"value": "UNIVERSALE ECONOMICA. SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Brotton, Jerry",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Sala, V. B.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "5.47243",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.77951",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.49606",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Feltrinelli"},
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
                                    "Amount": {"value": "19.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Feltrinelli"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "526"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.59842519522",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.7007873927",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.49999999439",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.6755131912",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2017-11-23"},
                                "Publisher": {"value": "Feltrinelli"},
                                "ReleaseDate": {"value": "2017-11-23"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61jo5I7vBjL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "48",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Feltrinelli"},
                                "Title": {
                                    "value": "La storia del mondo in dodici mappe"
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
                                    "Rank": {"value": "18925"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "34"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8811149843"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Wilford, John Noble",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Gianna Lonza",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.97636",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "6.69290",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.41732",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Garzanti"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "30.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "478"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4960629906",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.7401574714",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.2992125920",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.4991433816",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2018-11-22"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2018-11-22"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61KTEY8nMgL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "54",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {
                                    "value": "I signori delle mappe. La storia avventurosa dell'invenzione della cartografia"
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
                                    "Rank": {"value": "23845"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "41"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "B084FZWQHD"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Creator": {
                                    "value": "Frasante, Marco",
                                    "Role": {"value": "Autore"},
                                },
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "5.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.2",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Independently published"},
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
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Sconosciuto"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "12.69"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Independently published"},
                                "NumberOfPages": {"value": "87"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.2",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "0.37",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-02-09"},
                                "Publisher": {"value": "Independently published"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51Na9vFKvgL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "49",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Independently published"},
                                "Title": {
                                    "value": "Mappe Mentali e Mappe Concettuali: La Guida Pi\u00f9 Completa Per Memorizzare e Apprendere Qualsiasi Cosa In Modo Semplice e Veloce"
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
                                    "Rank": {"value": "2663"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508885031"},
                                    "Rank": {"value": "192"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "881160771X"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Marshall, Tim",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Easton, G.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Smith, J.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Hawkins, E.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Crane, P.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Caraffini, S.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "12.40155",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "10.03935",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.59055",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Garzanti"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "20.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "80"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.5511811018",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.2047243970",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "9.8425196750",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.6975594174",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-02-13"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2020-02-13"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/514B0NG7gvL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "57",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {
                                    "value": "Le 12 mappe che spiegano il mondo ai ragazzi"
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
                                    "Rank": {"value": "24610"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064684031"},
                                    "Rank": {"value": "7"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064569031"},
                                    "Rank": {"value": "35"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13077656031"},
                                    "Rank": {"value": "35"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "881167378X"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Creator": [
                                    {
                                        "value": "Marshall, Tim",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Merlini, R.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.77951",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "5.66928",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.37795",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Garzanti"},
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
                                    "Amount": {"value": "19.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "313"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4960629906",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.5826771566",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.7086614115",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.1904962148",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2017-06-08"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2017-06-08"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51DYJDPBKmL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "50",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {"value": "Le 10 mappe che spiegano il mondo"},
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "35380"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508819031"},
                                    "Rank": {"value": "197"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508812031"},
                                    "Rank": {"value": "678"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8804712279"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "LE SCIE. NUOVA SERIE STRANIERI"},
                                "Creator": [
                                    {
                                        "value": "Moller, Violet",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Vanni, L.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "9.44880",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "6.69290",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.18110",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Mondadori"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "22.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Mondadori"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "325"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4173228332",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "9.4488188880",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.4960629855",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.543235834",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2019-05-28"},
                                "Publisher": {"value": "Mondadori"},
                                "ReleaseDate": {"value": "2019-05-28"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51ntMunIvhL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "50",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Mondadori"},
                                "Title": {
                                    "value": "La mappa dei libri perduti. Come la conoscenza antica \u00e8 stata perduta e ritrovata: una storia in sette citt\u00e0"
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
                                    "Rank": {"value": "63759"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508810031"},
                                    "Rank": {"value": "692"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508879031"},
                                    "Rank": {"value": "15957"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "B008RJFRTK"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "App"},
                                "Brand": {"value": "MY.COM"},
                                "HardwarePlatform": {"value": "Android"},
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "MY.COM"},
                                "Languages": {
                                    "Language": [
                                        {
                                            "Name": {"value": "arabic"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "chinese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "czech"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "dutch"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "english"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "french"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "german"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "japanese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "korean"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "polish"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "portuguese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "russian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "spanish"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "vietnamese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "0.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "MY.COM"},
                                "OperatingSystem": {"value": "Android"},
                                "PartNumber": {"value": "com.mapswithme.maps.pro"},
                                "ProductGroup": {"value": "Mobile Application"},
                                "ProductTypeName": {"value": "MOBILE_APPLICATION"},
                                "Publisher": {"value": "MY.COM"},
                                "ReleaseDate": {"value": "2016-01-14"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61KevuswqEL._SL75_.png"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "MY.COM"},
                                "Title": {"value": "MAPS.ME \u2014 Mappe Offline"},
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {},
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
    parsed_json = DictWrapper(xml).parsed
    assert parsed_json == expected_json


def test_decode_byte_xml_x94():
    """Same test as test_decode_byte_xml but now with \x94 in the <title> tag"""
    xml = b'<?xml version="1.0"?><ListMatchingProductsResponse xmlns="http://mws.amazonservices.com/schema/Products/2011-10-01"><ListMatchingProductsResult><Products xmlns:ns2="http://mws.amazonservices.com/schema/Products/2011-10-01/default.xsd"><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8891808660</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Creator Role="Autore">Mizielinska, Aleksandra</ns2:Creator><ns2:Creator Role="Autore">Mizielinski, Daniel</ns2:Creator><ns2:Creator Role="Traduttore">Parisi, V.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">14.80312</ns2:Height><ns2:Length Units="inches">10.86612</ns2:Length><ns2:Width Units="inches">1.06299</ns2:Width><ns2:Weight Units="pounds">3.17</ns2:Weight></ns2:ItemDimensions><ns2:Label>Mondadori Electa</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>25.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Mondadori Electa</ns2:Manufacturer><ns2:NumberOfPages>144</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.8661417314</ns2:Height><ns2:Length Units="inches">14.9606299060</ns2:Length><ns2:Width Units="inches">11.0236220360</ns2:Width><ns2:Weight Units="pounds">3.1746565728</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2016-10-25</ns2:PublicationDate><ns2:Publisher>Mondadori Electa</ns2:Publisher><ns2:ReleaseDate>2016-10-25</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61K2xircqJL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">55</ns2:Width></ns2:SmallImage><ns2:Studio>Mondadori Electa</ns2:Studio><ns2:Title>Mappe. Un atlante per viaggiare tra terra, mari e culture del mondo\x94</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>2843</Rank></SalesRank><SalesRank><ProductCategoryId>13064701031</ProductCategoryId><Rank>2</Rank></SalesRank><SalesRank><ProductCategoryId>13077570031</ProductCategoryId><Rank>2</Rank></SalesRank><SalesRank><ProductCategoryId>13064711031</ProductCategoryId><Rank>15</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8858014308</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>Passioni</ns2:Brand><ns2:Creator Role="Autore">Brotton, Jerry</ns2:Creator><ns2:Creator Role="Traduttore">Fontebuoni, A.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">10.31494</ns2:Height><ns2:Length Units="inches">12.20470</ns2:Length><ns2:Width Units="inches">0.86614</ns2:Width></ns2:ItemDimensions><ns2:Label>Gribaudo</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>24.90</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Gribaudo</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>256</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.1023622036</ns2:Height><ns2:Length Units="inches">12.1653543183</ns2:Length><ns2:Width Units="inches">10.2362204620</ns2:Width><ns2:Weight Units="pounds">3.4392112872</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2015-11-05</ns2:PublicationDate><ns2:Publisher>Gribaudo</ns2:Publisher><ns2:ReleaseDate>2015-11-05</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61UmGSV5reL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">62</ns2:Width></ns2:SmallImage><ns2:Studio>Gribaudo</ns2:Studio><ns2:Title>Le grandi mappe. Oltre 60 capolavori raccontano l\'evoluzione dell\'uomo, la sua storia e la sua cultura. Ediz. illustrata</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>23519</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>40</Rank></SalesRank><SalesRank><ProductCategoryId>508856031</ProductCategoryId><Rank>452</Rank></SalesRank><SalesRank><ProductCategoryId>508758031</ProductCategoryId><Rank>3211</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8807890283</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Brand>UNIVERSALE ECONOMICA. SAGGI</ns2:Brand><ns2:Creator Role="Autore">Brotton, Jerry</ns2:Creator><ns2:Creator Role="Traduttore">Sala, V. B.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">5.47243</ns2:Height><ns2:Length Units="inches">8.77951</ns2:Length><ns2:Width Units="inches">1.49606</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Feltrinelli</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>19.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Feltrinelli</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>526</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.59842519522</ns2:Height><ns2:Length Units="inches">8.7007873927</ns2:Length><ns2:Width Units="inches">5.49999999439</ns2:Width><ns2:Weight Units="pounds">1.6755131912</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2017-11-23</ns2:PublicationDate><ns2:Publisher>Feltrinelli</ns2:Publisher><ns2:ReleaseDate>2017-11-23</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61jo5I7vBjL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">48</ns2:Width></ns2:SmallImage><ns2:Studio>Feltrinelli</ns2:Studio><ns2:Title>La storia del mondo in dodici mappe</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>18925</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>34</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8811149843</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>SAGGI</ns2:Brand><ns2:Creator Role="Autore">Wilford, John Noble</ns2:Creator><ns2:Creator Role="Traduttore">Gianna Lonza</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.97636</ns2:Height><ns2:Length Units="inches">6.69290</ns2:Length><ns2:Width Units="inches">1.41732</ns2:Width></ns2:ItemDimensions><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>30.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>478</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4960629906</ns2:Height><ns2:Length Units="inches">8.7401574714</ns2:Length><ns2:Width Units="inches">6.2992125920</ns2:Width><ns2:Weight Units="pounds">1.4991433816</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2018-11-22</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2018-11-22</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61KTEY8nMgL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">54</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>I signori delle mappe. La storia avventurosa dell\'invenzione della cartografia</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>23845</Rank></SalesRank><SalesRank><ProductCategoryId>508875031</ProductCategoryId><Rank>41</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>B084FZWQHD</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Creator Role="Autore">Frasante, Marco</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.5</ns2:Height><ns2:Length Units="inches">5.5</ns2:Length><ns2:Width Units="inches">0.2</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Independently published</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Sconosciuto</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>12.69</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Independently published</ns2:Manufacturer><ns2:NumberOfPages>87</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.2</ns2:Height><ns2:Length Units="inches">8.5</ns2:Length><ns2:Width Units="inches">5.5</ns2:Width><ns2:Weight Units="pounds">0.37</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-02-09</ns2:PublicationDate><ns2:Publisher>Independently published</ns2:Publisher><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51Na9vFKvgL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">49</ns2:Width></ns2:SmallImage><ns2:Studio>Independently published</ns2:Studio><ns2:Title>Mappe Mentali e Mappe Concettuali: La Guida Pi\xc3\xb9 Completa Per Memorizzare e Apprendere Qualsiasi Cosa In Modo Semplice e Veloce</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>2663</Rank></SalesRank><SalesRank><ProductCategoryId>508885031</ProductCategoryId><Rank>192</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>881160771X</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>SAGGI</ns2:Brand><ns2:Creator Role="Autore">Marshall, Tim</ns2:Creator><ns2:Creator Role="Illustratore">Easton, G.</ns2:Creator><ns2:Creator Role="Illustratore">Smith, J.</ns2:Creator><ns2:Creator Role="Illustratore">Hawkins, E.</ns2:Creator><ns2:Creator Role="Illustratore">Crane, P.</ns2:Creator><ns2:Creator Role="Traduttore">Caraffini, S.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">12.40155</ns2:Height><ns2:Length Units="inches">10.03935</ns2:Length><ns2:Width Units="inches">0.59055</ns2:Width></ns2:ItemDimensions><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>20.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>80</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">0.5511811018</ns2:Height><ns2:Length Units="inches">12.2047243970</ns2:Length><ns2:Width Units="inches">9.8425196750</ns2:Width><ns2:Weight Units="pounds">1.6975594174</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-02-13</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2020-02-13</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/514B0NG7gvL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">57</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>Le 12 mappe che spiegano il mondo ai ragazzi</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>24610</Rank></SalesRank><SalesRank><ProductCategoryId>13064684031</ProductCategoryId><Rank>7</Rank></SalesRank><SalesRank><ProductCategoryId>13064569031</ProductCategoryId><Rank>35</Rank></SalesRank><SalesRank><ProductCategoryId>13077656031</ProductCategoryId><Rank>35</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>881167378X</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Creator Role="Autore">Marshall, Tim</ns2:Creator><ns2:Creator Role="Traduttore">Merlini, R.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">8.77951</ns2:Height><ns2:Length Units="inches">5.66928</ns2:Length><ns2:Width Units="inches">1.37795</ns2:Width></ns2:ItemDimensions><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>Garzanti</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Lingua originale</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>19.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Garzanti</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>313</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4960629906</ns2:Height><ns2:Length Units="inches">8.5826771566</ns2:Length><ns2:Width Units="inches">5.7086614115</ns2:Width><ns2:Weight Units="pounds">1.1904962148</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2017-06-08</ns2:PublicationDate><ns2:Publisher>Garzanti</ns2:Publisher><ns2:ReleaseDate>2017-06-08</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51DYJDPBKmL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">50</ns2:Width></ns2:SmallImage><ns2:Studio>Garzanti</ns2:Studio><ns2:Title>Le 10 mappe che spiegano il mondo</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>35380</Rank></SalesRank><SalesRank><ProductCategoryId>508819031</ProductCategoryId><Rank>197</Rank></SalesRank><SalesRank><ProductCategoryId>508812031</ProductCategoryId><Rank>678</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8804712279</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina rigida</ns2:Binding><ns2:Brand>LE SCIE. NUOVA SERIE STRANIERI</ns2:Brand><ns2:Creator Role="Autore">Moller, Violet</ns2:Creator><ns2:Creator Role="Traduttore">Vanni, L.</ns2:Creator><ns2:ItemDimensions><ns2:Height Units="inches">9.44880</ns2:Height><ns2:Length Units="inches">6.69290</ns2:Length><ns2:Width Units="inches">1.18110</ns2:Width></ns2:ItemDimensions><ns2:Label>Mondadori</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>22.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Mondadori</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>325</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">1.4173228332</ns2:Height><ns2:Length Units="inches">9.4488188880</ns2:Length><ns2:Width Units="inches">6.4960629855</ns2:Width><ns2:Weight Units="pounds">1.543235834</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2019-05-28</ns2:PublicationDate><ns2:Publisher>Mondadori</ns2:Publisher><ns2:ReleaseDate>2019-05-28</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/51ntMunIvhL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">50</ns2:Width></ns2:SmallImage><ns2:Studio>Mondadori</ns2:Studio><ns2:Title>La mappa dei libri perduti. Come la conoscenza antica \xc3\xa8 stata perduta e ritrovata: una storia in sette citt\xc3\xa0</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>63759</Rank></SalesRank><SalesRank><ProductCategoryId>508810031</ProductCategoryId><Rank>692</Rank></SalesRank><SalesRank><ProductCategoryId>508879031</ProductCategoryId><Rank>15957</Rank></SalesRank></SalesRankings></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>B008RJFRTK</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>App</ns2:Binding><ns2:Brand>MY.COM</ns2:Brand><ns2:HardwarePlatform>Android</ns2:HardwarePlatform><ns2:IsAdultProduct>false</ns2:IsAdultProduct><ns2:Label>MY.COM</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>arabic</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>chinese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>czech</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>dutch</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>english</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>french</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>german</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>japanese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>korean</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>polish</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>portuguese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>russian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>spanish</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language><ns2:Language><ns2:Name>vietnamese</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>0.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>MY.COM</ns2:Manufacturer><ns2:OperatingSystem>Android</ns2:OperatingSystem><ns2:PartNumber>com.mapswithme.maps.pro</ns2:PartNumber><ns2:ProductGroup>Mobile Application</ns2:ProductGroup><ns2:ProductTypeName>MOBILE_APPLICATION</ns2:ProductTypeName><ns2:Publisher>MY.COM</ns2:Publisher><ns2:ReleaseDate>2016-01-14</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/61KevuswqEL._SL75_.png</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">75</ns2:Width></ns2:SmallImage><ns2:Studio>MY.COM</ns2:Studio><ns2:Title>MAPS.ME \xe2\x80\x94 Mappe Offline</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings/></Product><Product><Identifiers><MarketplaceASIN><MarketplaceId>APJ6JRA9NG5V4</MarketplaceId><ASIN>8832706571</ASIN></MarketplaceASIN></Identifiers><AttributeSets><ns2:ItemAttributes xml:lang="it-IT"><ns2:Binding>Copertina flessibile</ns2:Binding><ns2:Creator Role="Autore">aa.vv.</ns2:Creator><ns2:Genre>Diritto</ns2:Genre><ns2:Label>Neldiritto Editore</ns2:Label><ns2:Languages><ns2:Language><ns2:Name>italian</ns2:Name><ns2:Type>Pubblicato</ns2:Type></ns2:Language></ns2:Languages><ns2:ListPrice><ns2:Amount>90.00</ns2:Amount><ns2:CurrencyCode>EUR</ns2:CurrencyCode></ns2:ListPrice><ns2:Manufacturer>Neldiritto Editore</ns2:Manufacturer><ns2:NumberOfItems>1</ns2:NumberOfItems><ns2:NumberOfPages>1200</ns2:NumberOfPages><ns2:PackageDimensions><ns2:Height Units="inches">3.0708661386</ns2:Height><ns2:Length Units="inches">9.8425196750</ns2:Length><ns2:Width Units="inches">6.7716535364</ns2:Width><ns2:Weight Units="pounds">5.291094288000000881849048</ns2:Weight></ns2:PackageDimensions><ns2:ProductGroup>Libro</ns2:ProductGroup><ns2:ProductTypeName>ABIS_BOOK</ns2:ProductTypeName><ns2:PublicationDate>2020-01-24</ns2:PublicationDate><ns2:Publisher>Neldiritto Editore</ns2:Publisher><ns2:ReleaseDate>2020-01-24</ns2:ReleaseDate><ns2:SmallImage><ns2:URL>http://ecx.images-amazon.com/images/I/41HeNbq4xKL._SL75_.jpg</ns2:URL><ns2:Height Units="pixels">75</ns2:Height><ns2:Width Units="pixels">53</ns2:Width></ns2:SmallImage><ns2:Studio>Neldiritto Editore</ns2:Studio><ns2:Title>Concorso Magistratura 2020: Mappe e schemi di Diritto civile-Diritto penale-Diritto amministrativo</ns2:Title></ns2:ItemAttributes></AttributeSets><Relationships/><SalesRankings><SalesRank><ProductCategoryId>book_display_on_website</ProductCategoryId><Rank>62044</Rank></SalesRank><SalesRank><ProductCategoryId>1346646031</ProductCategoryId><Rank>617</Rank></SalesRank><SalesRank><ProductCategoryId>1346648031</ProductCategoryId><Rank>754</Rank></SalesRank></SalesRankings></Product></Products></ListMatchingProductsResult><ResponseMetadata><RequestId>d384713e-7c79-4a6d-81cd-d0aa68c7b409</RequestId></ResponseMetadata></ListMatchingProductsResponse>'
    expected_json = {
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
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "2843"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064701031"},
                                    "Rank": {"value": "2"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13077570031"},
                                    "Rank": {"value": "2"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064711031"},
                                    "Rank": {"value": "15"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8858014308"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "Passioni"},
                                "Creator": [
                                    {
                                        "value": "Brotton, Jerry",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Fontebuoni, A.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "10.31494",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.20470",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.86614",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Gribaudo"},
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
                                    "Amount": {"value": "24.90"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Gribaudo"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "256"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.1023622036",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.1653543183",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "10.2362204620",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "3.4392112872",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2015-11-05"},
                                "Publisher": {"value": "Gribaudo"},
                                "ReleaseDate": {"value": "2015-11-05"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61UmGSV5reL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "62",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Gribaudo"},
                                "Title": {
                                    "value": "Le grandi mappe. Oltre 60 capolavori raccontano l'evoluzione dell'uomo, la sua storia e la sua cultura. Ediz. illustrata"
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
                                    "Rank": {"value": "23519"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "40"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508856031"},
                                    "Rank": {"value": "452"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508758031"},
                                    "Rank": {"value": "3211"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8807890283"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Brand": {"value": "UNIVERSALE ECONOMICA. SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Brotton, Jerry",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Sala, V. B.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "5.47243",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.77951",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.49606",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Feltrinelli"},
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
                                    "Amount": {"value": "19.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Feltrinelli"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "526"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.59842519522",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.7007873927",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.49999999439",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.6755131912",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2017-11-23"},
                                "Publisher": {"value": "Feltrinelli"},
                                "ReleaseDate": {"value": "2017-11-23"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61jo5I7vBjL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "48",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Feltrinelli"},
                                "Title": {
                                    "value": "La storia del mondo in dodici mappe"
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
                                    "Rank": {"value": "18925"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "34"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8811149843"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Wilford, John Noble",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Gianna Lonza",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.97636",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "6.69290",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.41732",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Garzanti"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "30.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "478"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4960629906",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.7401574714",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.2992125920",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.4991433816",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2018-11-22"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2018-11-22"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61KTEY8nMgL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "54",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {
                                    "value": "I signori delle mappe. La storia avventurosa dell'invenzione della cartografia"
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
                                    "Rank": {"value": "23845"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508875031"},
                                    "Rank": {"value": "41"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "B084FZWQHD"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina flessibile"},
                                "Creator": {
                                    "value": "Frasante, Marco",
                                    "Role": {"value": "Autore"},
                                },
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "5.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.2",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Independently published"},
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
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Sconosciuto"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "12.69"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Independently published"},
                                "NumberOfPages": {"value": "87"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.2",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.5",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "0.37",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-02-09"},
                                "Publisher": {"value": "Independently published"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51Na9vFKvgL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "49",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Independently published"},
                                "Title": {
                                    "value": "Mappe Mentali e Mappe Concettuali: La Guida Pi\u00f9 Completa Per Memorizzare e Apprendere Qualsiasi Cosa In Modo Semplice e Veloce"
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
                                    "Rank": {"value": "2663"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508885031"},
                                    "Rank": {"value": "192"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "881160771X"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "SAGGI"},
                                "Creator": [
                                    {
                                        "value": "Marshall, Tim",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Easton, G.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Smith, J.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Hawkins, E.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Crane, P.",
                                        "Role": {"value": "Illustratore"},
                                    },
                                    {
                                        "value": "Caraffini, S.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "12.40155",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "10.03935",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "0.59055",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Garzanti"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "20.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "80"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "0.5511811018",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "12.2047243970",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "9.8425196750",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.6975594174",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2020-02-13"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2020-02-13"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/514B0NG7gvL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "57",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {
                                    "value": "Le 12 mappe che spiegano il mondo ai ragazzi"
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
                                    "Rank": {"value": "24610"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064684031"},
                                    "Rank": {"value": "7"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13064569031"},
                                    "Rank": {"value": "35"},
                                },
                                {
                                    "ProductCategoryId": {"value": "13077656031"},
                                    "Rank": {"value": "35"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "881167378X"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Creator": [
                                    {
                                        "value": "Marshall, Tim",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Merlini, R.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "8.77951",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "5.66928",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.37795",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "Garzanti"},
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
                                    "Amount": {"value": "19.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Garzanti"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "313"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4960629906",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "8.5826771566",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "5.7086614115",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.1904962148",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2017-06-08"},
                                "Publisher": {"value": "Garzanti"},
                                "ReleaseDate": {"value": "2017-06-08"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51DYJDPBKmL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "50",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Garzanti"},
                                "Title": {"value": "Le 10 mappe che spiegano il mondo"},
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {
                            "SalesRank": [
                                {
                                    "ProductCategoryId": {
                                        "value": "book_display_on_website"
                                    },
                                    "Rank": {"value": "35380"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508819031"},
                                    "Rank": {"value": "197"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508812031"},
                                    "Rank": {"value": "678"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "8804712279"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "Copertina rigida"},
                                "Brand": {"value": "LE SCIE. NUOVA SERIE STRANIERI"},
                                "Creator": [
                                    {
                                        "value": "Moller, Violet",
                                        "Role": {"value": "Autore"},
                                    },
                                    {
                                        "value": "Vanni, L.",
                                        "Role": {"value": "Traduttore"},
                                    },
                                ],
                                "ItemDimensions": {
                                    "Height": {
                                        "value": "9.44880",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "6.69290",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "1.18110",
                                        "Units": {"value": "inches"},
                                    },
                                },
                                "Label": {"value": "Mondadori"},
                                "Languages": {
                                    "Language": {
                                        "Name": {"value": "italian"},
                                        "Type": {"value": "Pubblicato"},
                                    }
                                },
                                "ListPrice": {
                                    "Amount": {"value": "22.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "Mondadori"},
                                "NumberOfItems": {"value": "1"},
                                "NumberOfPages": {"value": "325"},
                                "PackageDimensions": {
                                    "Height": {
                                        "value": "1.4173228332",
                                        "Units": {"value": "inches"},
                                    },
                                    "Length": {
                                        "value": "9.4488188880",
                                        "Units": {"value": "inches"},
                                    },
                                    "Width": {
                                        "value": "6.4960629855",
                                        "Units": {"value": "inches"},
                                    },
                                    "Weight": {
                                        "value": "1.543235834",
                                        "Units": {"value": "pounds"},
                                    },
                                },
                                "ProductGroup": {"value": "Libro"},
                                "ProductTypeName": {"value": "ABIS_BOOK"},
                                "PublicationDate": {"value": "2019-05-28"},
                                "Publisher": {"value": "Mondadori"},
                                "ReleaseDate": {"value": "2019-05-28"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/51ntMunIvhL._SL75_.jpg"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "50",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "Mondadori"},
                                "Title": {
                                    "value": "La mappa dei libri perduti. Come la conoscenza antica \u00e8 stata perduta e ritrovata: una storia in sette citt\u00e0"
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
                                    "Rank": {"value": "63759"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508810031"},
                                    "Rank": {"value": "692"},
                                },
                                {
                                    "ProductCategoryId": {"value": "508879031"},
                                    "Rank": {"value": "15957"},
                                },
                            ]
                        },
                    },
                    {
                        "Identifiers": {
                            "MarketplaceASIN": {
                                "MarketplaceId": {"value": "APJ6JRA9NG5V4"},
                                "ASIN": {"value": "B008RJFRTK"},
                            }
                        },
                        "AttributeSets": {
                            "ItemAttributes": {
                                "lang": {"value": "it-IT"},
                                "Binding": {"value": "App"},
                                "Brand": {"value": "MY.COM"},
                                "HardwarePlatform": {"value": "Android"},
                                "IsAdultProduct": {"value": "false"},
                                "Label": {"value": "MY.COM"},
                                "Languages": {
                                    "Language": [
                                        {
                                            "Name": {"value": "arabic"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "chinese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "czech"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "dutch"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "english"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "french"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "german"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "italian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "japanese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "korean"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "polish"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "portuguese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "russian"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "spanish"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                        {
                                            "Name": {"value": "vietnamese"},
                                            "Type": {"value": "Pubblicato"},
                                        },
                                    ]
                                },
                                "ListPrice": {
                                    "Amount": {"value": "0.00"},
                                    "CurrencyCode": {"value": "EUR"},
                                },
                                "Manufacturer": {"value": "MY.COM"},
                                "OperatingSystem": {"value": "Android"},
                                "PartNumber": {"value": "com.mapswithme.maps.pro"},
                                "ProductGroup": {"value": "Mobile Application"},
                                "ProductTypeName": {"value": "MOBILE_APPLICATION"},
                                "Publisher": {"value": "MY.COM"},
                                "ReleaseDate": {"value": "2016-01-14"},
                                "SmallImage": {
                                    "URL": {
                                        "value": "http://ecx.images-amazon.com/images/I/61KevuswqEL._SL75_.png"
                                    },
                                    "Height": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                    "Width": {
                                        "value": "75",
                                        "Units": {"value": "pixels"},
                                    },
                                },
                                "Studio": {"value": "MY.COM"},
                                "Title": {"value": "MAPS.ME \u2014 Mappe Offline"},
                            }
                        },
                        "Relationships": {},
                        "SalesRankings": {},
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
    parsed_json = DictWrapper(xml).parsed
    assert parsed_json == expected_json


