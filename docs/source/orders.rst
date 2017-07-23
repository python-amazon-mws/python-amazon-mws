############
Orders
############


Here is a very simple example of how to retrieve a orders from Amazon


.. code-block:: Python

    from mws import mws

    access_key = 'accesskey' #replace with your access key
    seller_id = 'merchantid' #replace with your seller id
    secret_key = 'secretkey' #replace with your secret key
    marketplace_usa = 'ATVPDKIKX0DER'

    orders_api = mws.Orders(access_key, secret_key, seller_id, region='US')
    orders = orders_api.list_orders(marketplaceids=[marketplace_usa], created_after='2017-07-07')
