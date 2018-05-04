############
Feeds
############

There are several types of feeds and some of them are used to send product data. Here is a example of how to send product basic data, inventory data and product images.

To build your own XML data you should use Amazon documentation about feed types that you can find here: http://docs.developer.amazonservices.com/en_US/feeds/Feeds_FeedType.html#FeedType_Enumeration__ProductInventoryFeeds. Also Python xml.etree.ElementTree module can be very useful.

.. code-block:: Python

    import mws

    access_key = 'accesskey' #replace with your access key
    seller_id = 'merchantid' #replace with your seller id
    secret_key = 'secretkey' #replace with your secret key
    MWS_MARKETPLACE_ID = 'ATVPDKIKX0DER'

    feed = mws.Feeds(access_key, secret_key, seller_id, region='US')
    
    print("### Product feed ###")
    xml = """<?xml version='1.0' encoding='iso-8859-1'?>
                <AmazonEnvelope xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance' xsi:noNamespaceSchemaLocation='amzn-envelope.xsd'>
                  <Header>
                    <DocumentVersion>1.01</DocumentVersion>
                    <MerchantIdentifier>merchantid</MerchantIdentifier>
                  </Header>
                  <MessageType>Product</MessageType>
                  <Message>
                    <MessageID>1</MessageID>
                    <OperationType>Update</OperationType>
                    <Product>
                      <SKU>153024</SKU>
                      <StandardProductID>
                        <Type>EAN</Type>
                        <Value>8427426004696</Value>
                      </StandardProductID>
                      <DescriptionData>
                        <Title>DENTAID Interprox Micro 18 units</Title>
                        <Brand>Dentaid</Brand>
                        <Description>Interprox Plus Micro is designed to remove oral biofilm (bacterial plaque) build-up from 0.9 mm* interproximal spaces, particularly in the premolar and molar areas.</Description>
                        <MSRP currency="EUR">15.76</MSRP>
                        <Manufacturer>Dentaid</Manufacturer>
                        <MfrPartNumber>8427426004696</MfrPartNumber>
                      </DescriptionData>
                      <ProductData>
                        <Beauty>
                          <ProductType>
                            <BeautyMisc>
                              <Language>English</Language>
                            </BeautyMisc>
                          </ProductType>
                        </Beauty>
                      </ProductData>
                    </Product>
                  </Message>
                </AmazonEnvelope>"""
    response = feed.submit_feed(xml, "_POST_PRODUCT_DATA_", MWS_MARKETPLACE_ID)
    print(response.parsed)


    print("### Inventory feed ###")
    xml = """<?xml version='1.0' encoding='iso-8859-1'?>
                <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
                  <Header>
                    <DocumentVersion>1.01</DocumentVersion>
                    <MerchantIdentifier>merchantid</MerchantIdentifier>
                  </Header>
                  <MessageType>Inventory</MessageType>
                  <Message>
                    <MessageID>1</MessageID>
                    <OperationType>Update</OperationType>
                    <Inventory>
                      <SKU>153024</SKU>
                      <Quantity>2</Quantity>
                    </Inventory>
                  </Message>
                </AmazonEnvelope>"""
    response = feed.submit_feed(xml, "_POST_INVENTORY_AVAILABILITY_DATA_", MWS_MARKETPLACE_ID)
    print(response.parsed)


    print("### Product image feed ###")
    xml = """<?xml version='1.0' encoding='iso-8859-1'?>
                <AmazonEnvelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="amzn-envelope.xsd">
                  <Header>
                    <DocumentVersion>1.01</DocumentVersion>
                    <MerchantIdentifier>merchantid</MerchantIdentifier>
                  </Header>
                  <MessageType>ProductImage</MessageType>
                  <Message>
                    <MessageID>1</MessageID>
                    <OperationType>Update</OperationType>
                    <ProductImage>
                      <SKU>235609</SKU>
                      <ImageType>Main</ImageType>
                      <ImageLocation>http://your-domain.org/235609.JPG</ImageLocation>
                    </ProductImage>
                  </Message>
                </AmazonEnvelope>"""
    response = feed.submit_feed(xml, "_POST_PRODUCT_IMAGE_DATA_", MWS_MARKETPLACE_ID)
    print(response.parsed)
