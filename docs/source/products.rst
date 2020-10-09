############
Products
############


Here is a very simple example of how to retrieve a products from Amazon


.. code-block:: Python

    from mws import mws

    access_key = 'accesskey' #replace with your access key
    seller_id = 'merchantid' #replace with your seller id
    secret_key = 'secretkey' #replace with your secret key
    marketplace_usa = 'ATVPDKIKX0DER'

    products_api = mws.Products(access_key, secret_key, seller_id, region='US')
    products = products_api.list_matching_products(marketplaceid=marketplace_usa, query='*')
