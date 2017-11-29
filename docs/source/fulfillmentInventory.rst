############################
Fulfillment Inventory
############################

Here is a very simple example of how to retrieve a inventory from Amazon
(assuming you already have a sku)
using the python-amazon-mws wrapper.

.. code-block:: Python

    from mws import mws

    access_key = 'accesskey' #replace with your access key
    merchant_id = 'merchantid' #replace with your merchant id
    secret_key = 'secretkey' #replace with your secret key

    sku = 'sku id' #replace with sku id

    inventory = mws.Inventory(access_key=access_key, secret_key=secret_key, account_id=merchant_id)
    result = inventory.list_inventory_supply(skus=[sku])
    response_data = result.original
    print response_data
